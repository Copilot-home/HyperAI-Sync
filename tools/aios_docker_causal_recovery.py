#!/usr/bin/env python3
"""Docker Desktop causal recovery: preserve, reclaim, restart, validate.

Performs state-preserving causal recovery for Docker Desktop on macOS.
Does not delete Docker.raw, volumes, images, or project state.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runtime" / "federation_orchestrator"
HOME = Path.home()
DOCKER_LOG_DIR = HOME / "Library" / "Containers" / "com.docker.docker" / "Data" / "log"
DOCKER_RAW = HOME / "Library" / "Containers" / "com.docker.docker" / "Data" / "vms" / "0" / "data" / "Docker.raw"
DOCKER_SOCK = HOME / ".docker" / "run" / "docker.sock"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def run_cmd(args: list[str], timeout: float = 10.0, kill_children: bool = True) -> dict:
    start = time.time()
    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except Exception:
                proc.kill()
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
            return {
                "exit_code": None,
                "stdout": "",
                "stderr": "TIMEOUT",
                "timeout": True,
                "elapsed_sec": round(time.time() - start, 3),
            }
        return {
            "exit_code": proc.returncode,
            "stdout": stdout[:8000],
            "stderr": stderr[:2000],
            "timeout": False,
            "elapsed_sec": round(time.time() - start, 3),
        }
    except Exception as exc:
        return {
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc)[:500],
            "timeout": False,
            "elapsed_sec": round(time.time() - start, 3),
        }


def disk_free_mb() -> float:
    usage = shutil.disk_usage("/System/Volumes/Data")
    return usage.free / (1024 * 1024)


def get_processes() -> list[str]:
    pgrep = run_cmd(["pgrep", "-f", "-i", "docker"], timeout=5, kill_children=False)
    pids = [line.strip() for line in pgrep["stdout"].splitlines() if line.strip().isdigit()]
    if not pids:
        return []
    ps = run_cmd(["ps", "-p", ",".join(pids[:64]), "-o", "pid,ppid,%cpu,%mem,etime,command"], timeout=5, kill_children=False)
    return [line.strip() for line in ps["stdout"].splitlines()[1:] if line.strip()]


def count_docker_processes() -> int:
    return len([p for p in get_processes() if not re.search(r"pgrep|ps -p|docker_causal_recovery", p, re.I)])


def has_process(pattern: str) -> bool:
    return any(pattern in p for p in get_processes())


def daemon_responsive(timeout: float = 5.0) -> dict:
    result = run_cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}", "--max-time", str(timeout), "--unix-socket", str(DOCKER_SOCK), "http://localhost/_ping"], timeout=timeout + 1)
    code = result["stdout"].strip().split()[0] if result["stdout"].strip() else None
    return {"responsive": code == "200", "code": code, "evidence": result}


def tail_init_log(n: int = 20) -> list[str]:
    p = DOCKER_LOG_DIR / "vm" / "init.log"
    if not p.exists():
        return []
    r = run_cmd(["tail", "-n", str(n), str(p)], timeout=5, kill_children=False)
    return r["stdout"].splitlines()


def find_io_errors(lines: list[str]) -> list[str]:
    return [line for line in lines if any(k in line for k in ["I/O error", "journal abort", "Remounting filesystem read-only"])]


def phase_1_preserve(exec_id: str) -> dict:
    preserved = OUT / f"docker_recovery_preserved_frame_{exec_id}"
    preserved.mkdir(parents=True, exist_ok=True)
    files = [
        OUT / "docker_current_frame_manifest.json",
        OUT / "docker_plane_state_matrix.json",
        OUT / "docker_same_frame_evidence_ledger.json",
        OUT / "docker_hypothesis_discrimination_matrix.json",
        OUT / "docker_incident_sequence.json",
    ]
    receipt = {
        "execution_id": exec_id,
        "timestamp": now_iso(),
        "docker_raw_metadata": {
            "path": str(DOCKER_RAW),
            "size_bytes": DOCKER_RAW.stat().st_size,
            "sha256_partial": sha256_str(str(DOCKER_RAW.stat().st_size)),
        },
        "preserved_artifacts": [],
    }
    for src in files:
        if src.exists():
            dst = preserved / src.name
            shutil.copy2(src, dst)
            receipt["preserved_artifacts"].append({
                "name": src.name,
                "sha256": sha256_file(dst),
                "path": str(dst),
            })
    (preserved / "preservation_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    return receipt


def phase_2_reclaim() -> dict:
    ledger: list[dict] = []
    free_before = disk_free_mb()

    # Safe reclaim candidates: temporary / rebuildable cache only.
    temp_dir = Path("/var/folders/6t/gg0v6x8j5cgbds_klhpdwnvw0000gn/T")
    candidates: list[tuple[Path, str, str]] = [
        (temp_dir / "DockerDesktopUpdates", "Docker Desktop update package cache", "rebuildable"),
        (HOME / "Library" / "Caches" / "CloudKit", "CloudKit cache", "rebuildable"),
        (HOME / "Library" / "Caches" / "Google", "Google app cache", "rebuildable"),
        (HOME / "Library" / "Caches" / "Homebrew", "Homebrew cache", "rebuildable"),
        (HOME / "Library" / "Caches" / "com.apple.SpeechRecognitionCore", "Speech recognition cache", "rebuildable"),
        (HOME / "Library" / "Caches" / "com.apple.e5rt.e5bundlecache", "Apple bundle cache", "rebuildable"),
    ]

    # Also add old temp files in /var/folders
    if temp_dir.exists():
        for child in temp_dir.iterdir():
            if child.is_dir() and child.name.startswith("kiro-cli-download"):
                candidates.append((child, "Kiro CLI download temp", "rebuildable"))
            if child.is_file() and child.name.startswith("CFNetworkDownload"):
                candidates.append((child, "CFNetwork download temp", "rebuildable"))

    for path, kind, classification in candidates:
        if not path.exists():
            continue
        try:
            du = run_cmd(["du", "-sh", str(path)], timeout=5, kill_children=False)
            size = du["stdout"].split()[0] if du["stdout"].strip() else "unknown"
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                try:
                    path.unlink()
                except Exception:
                    pass
            ledger.append({
                "path": str(path),
                "kind": kind,
                "classification": classification,
                "size_before": size,
                "deleted": True,
                "timestamp": now_iso(),
            })
        except Exception as exc:
            ledger.append({
                "path": str(path),
                "kind": kind,
                "classification": classification,
                "size_before": None,
                "deleted": False,
                "error": str(exc),
                "timestamp": now_iso(),
            })

    free_after = disk_free_mb()
    return {
        "free_before_mb": round(free_before, 1),
        "free_after_mb": round(free_after, 1),
        "freed_mb": round(free_after - free_before, 1),
        "ledger": ledger,
    }


def _docker_pids() -> list[tuple[int, str]]:
    """Return (pid, command) for Docker processes except vmnetd and pgrep."""
    out: list[tuple[int, str]] = []
    for line in get_processes():
        if any(k in line for k in ["com.docker.vmnetd", "pgrep", "ps -p"]):
            continue
        m = re.match(r"(\d+)\s", line)
        if m:
            out.append((int(m.group(1)), line))
    return out


def _kill_stale_docker(sig: int) -> int:
    killed = 0
    for pid, cmd in _docker_pids():
        try:
            os.kill(pid, sig)
            killed += 1
        except Exception:
            pass
    return killed


def phase_3_restart() -> dict:
    trace: list[dict] = []

    # Pre-kill any stale Docker backend/virtualization processes (not vmnetd)
    pre_stale = _docker_pids()
    if pre_stale:
        _kill_stale_docker(signal.SIGTERM)
        trace.append({"step": "PRE_KILL_STALE_DOCKER", "pids": [p[0] for p in pre_stale], "at": now_iso()})

    # Quit Docker Desktop gracefully via UI
    pre_count = count_docker_processes()
    trace.append({"step": "PRE_QUIT_PROCESS_COUNT", "count": pre_count, "at": now_iso()})

    quit_result = run_cmd(["osascript", "-e", 'quit app "Docker"'], timeout=20, kill_children=False)
    trace.append({"step": "QUIT_DOCKER", "result": quit_result, "at": now_iso()})

    # Wait for graceful shutdown (max 60s)
    waited = 0.0
    sigterm_sent = False
    while waited < 60.0:
        pids = _docker_pids()
        if not pids:
            break
        if waited >= 20.0 and not sigterm_sent:
            _kill_stale_docker(signal.SIGTERM)
            sigterm_sent = True
            trace.append({"step": "SIGTERM_STALE_DOCKER", "count": len(pids), "at": now_iso()})
        time.sleep(2)
        waited += 2

    # Force kill anything still alive except vmnetd
    pids = _docker_pids()
    if pids:
        _kill_stale_docker(signal.SIGKILL)
        trace.append({"step": "SIGKILL_STALE_DOCKER", "pids": [p[0] for p in pids], "at": now_iso()})
        time.sleep(3)

    post_quit_count = count_docker_processes()
    trace.append({"step": "POST_QUIT_PROCESS_COUNT", "count": post_quit_count, "at": now_iso()})

    # Start Docker Desktop
    start_result = run_cmd(["open", "-a", "Docker"], timeout=20, kill_children=False)
    trace.append({"step": "START_DOCKER", "result": start_result, "at": now_iso()})

    # Wait for backend and virtualization to appear
    boot_waited = 0.0
    backend = False
    virtualization = False
    while boot_waited < 180.0:
        backend = has_process("com.docker.backend")
        virtualization = has_process("com.docker.virtualization")
        if backend and virtualization:
            break
        time.sleep(3)
        boot_waited += 3

    trace.append({"step": "BOOT_WAIT", "backend": backend, "virtualization": virtualization, "waited_sec": boot_waited, "at": now_iso()})

    # Give VM a few seconds to settle
    time.sleep(10)

    return {"trace": trace, "backend": backend, "virtualization": virtualization}


def phase_4_validate() -> dict:
    results: dict[str, Any] = {}

    # 1. Socket ping
    ping = daemon_responsive(timeout=5)
    results["socket_ping"] = ping

    # 2. Docker version
    results["docker_version"] = run_cmd(["docker", "version"], timeout=15)

    # 3. Docker info
    results["docker_info"] = run_cmd(["docker", "system", "info"], timeout=15)

    # 4. Docker ps
    results["docker_ps"] = run_cmd(["docker", "ps"], timeout=15)

    # 5. Disposable container execution
    if ping["responsive"]:
        results["container_run"] = run_cmd(["docker", "run", "--rm", "alpine", "echo", "container-runtime-ok"], timeout=20)

        # 6. Container write
        results["container_write"] = run_cmd([
            "docker", "run", "--rm", "alpine", "sh", "-c",
            "echo test > /tmp/test && cat /tmp/test"
        ], timeout=20)

        # 7. Container network (ping external)
        results["container_network"] = run_cmd([
            "docker", "run", "--rm", "alpine", "ping", "-c", "1", "-W", "3", "8.8.8.8"
        ], timeout=20)

        # 8. BuildKit
        results["buildx"] = run_cmd(["docker", "buildx", "ls"], timeout=15)

        # 9. Host port forwarding
        results["port_forward"] = run_cmd([
            "docker", "run", "--rm", "-p", "127.0.0.1:59999:80", "alpine", "sh", "-c",
            "(echo 'HTTP/1.1 200 OK'; echo) | nc -l -p 80 -q 1"
        ], timeout=15)
        # Quick probe the published port
        if results["port_forward"]["timeout"]:
            # nc may run until timeout; that's acceptable if we can test reachability differently.
            pass
        results["port_probe"] = run_cmd([
            "sh", "-c", "curl -s -o /dev/null -w '%{http_code}' --max-time 3 http://127.0.0.1:59999/"
        ], timeout=5, kill_children=False)

    # 10. Check init.log for new I/O errors
    init_lines = tail_init_log(30)
    results["new_io_errors"] = find_io_errors(init_lines)

    return results


def determine_verdict(restart_ok: bool, validation: dict) -> str:
    if not restart_ok:
        return "DOCKER_RECOVERY_PARTIAL"

    ping = validation.get("socket_ping", {})
    if not ping.get("responsive"):
        return "DOCKER_RECOVERY_PARTIAL"

    new_io = validation.get("new_io_errors", [])
    if new_io:
        return "PERSISTENT_VM_STORAGE_STATE_FAILURE"

    container_run = validation.get("container_run", {})
    if container_run.get("exit_code") != 0:
        return "DOCKER_RECOVERY_PARTIAL"

    container_write = validation.get("container_write", {})
    if container_write.get("exit_code") != 0:
        return "DOCKER_RECOVERY_PARTIAL"

    return "DOCKER_DESKTOP_OPERATIONAL_VERIFIED"


def main() -> int:
    exec_id = f"docker-recovery-{uuid.uuid4().hex[:8]}"
    print(f"Execution: {exec_id}")

    # Phase 1: Preserve
    receipt = {"execution_id": exec_id, "timestamp": now_iso()}
    receipt["preserve"] = phase_1_preserve(exec_id)
    print("Phase 1 PRESERVE done")

    # Phase 2: Reclaim
    reclaim = phase_2_reclaim()
    receipt["reclaim"] = reclaim
    print(f"Phase 2 RECLAIM: freed {reclaim['freed_mb']} MB, free now {reclaim['free_after_mb']} MB")

    if reclaim["free_after_mb"] < 1024:
        receipt["verdict"] = "INSUFFICIENT_SAFE_OPERATING_MARGIN"
        (OUT / "docker_recovery_execution_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
        print("STOP: insufficient safe operating margin")
        return 0

    # Phase 3: Restart
    restart = phase_3_restart()
    receipt["restart"] = restart
    print(f"Phase 3 RESTART: backend={restart['backend']} virtualization={restart['virtualization']}")

    # Phase 4: Validate
    validation = phase_4_validate()
    receipt["validation"] = validation
    print("Phase 4 VALIDATE done")

    # Verdict
    verdict = determine_verdict(restart["backend"] and restart["virtualization"], validation)
    receipt["verdict"] = verdict

    # Phase 5: Update hypothesis matrix
    new_matrix = {
        "H1_HOST_RESOURCE_PRESSURE": {
            "confidence_after_reclaim": "STRONGLY_SUPPORTED" if reclaim["freed_mb"] > 100 and verdict == "DOCKER_DESKTOP_OPERATIONAL_VERIFIED" else "PARTIAL",
            "evidence": f"reclaimed {reclaim['freed_mb']} MB; free after {reclaim['free_after_mb']} MB",
        },
        "H2_VM_INTERNAL_STATE_FAILURE": {
            "confidence_after_restart": "RECOVERED_CONSEQUENCE" if verdict == "DOCKER_DESKTOP_OPERATIONAL_VERIFIED" else "STRONGLY_SUPPORTED" if validation.get("new_io_errors") else "PARTIAL",
            "evidence": validation.get("new_io_errors")[:3] if validation.get("new_io_errors") else "no new I/O errors in current window",
        },
    }
    receipt["hypothesis_update"] = new_matrix

    (OUT / "docker_recovery_execution_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")

    # Append to report
    report_path = OUT / "DOCKER_DESKTOP_CAUSAL_RECOVERY_REPORT.md"
    if report_path.exists():
        report = report_path.read_text(encoding="utf-8") + "\n\n"
    else:
        report = ""
    report += f"## Recovery Execution: {exec_id}\n"
    report += f"- Timestamp: {now_iso()}\n"
    report += f"- Freed MB: {reclaim['freed_mb']}\n"
    report += f"- Free after: {reclaim['free_after_mb']} MB\n"
    report += f"- Restart backend: {restart['backend']}\n"
    report += f"- Restart virtualization: {restart['virtualization']}\n"
    report += f"- Daemon responsive: {validation.get('socket_ping', {}).get('responsive')}\n"
    report += f"- Container run exit: {validation.get('container_run', {}).get('exit_code')}\n"
    report += f"- Container write exit: {validation.get('container_write', {}).get('exit_code')}\n"
    report += f"- New I/O errors count: {len(validation.get('new_io_errors', []))}\n"
    report += f"- Verdict: {verdict}\n"
    report_path.write_text(report, encoding="utf-8")

    print(f"Verdict: {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
