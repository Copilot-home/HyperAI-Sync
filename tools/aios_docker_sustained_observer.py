#!/usr/bin/env python3
"""Bounded sustained Docker Desktop validation observer.

Runs for a fixed duration, sampling daemon responsiveness, container runtime,
host port forwarding, and vm/init.log I/O errors. No destructive actions.
"""

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
OUT = Path(__file__).resolve().parents[1] / "runtime" / "federation_orchestrator"
DOCKER_SOCK = HOME / ".docker" / "run" / "docker.sock"
INIT_LOG = HOME / "Library" / "Containers" / "com.docker.docker" / "Data" / "log" / "vm" / "init.log"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_cmd(args: list[str], timeout: float = 10.0) -> dict:
    start = time.time()
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout[:1000],
            "stderr": proc.stderr[:500],
            "elapsed_sec": round(time.time() - start, 3),
        }
    except Exception as exc:
        return {"exit_code": None, "stdout": "", "stderr": str(exc)[:500], "elapsed_sec": round(time.time() - start, 3)}


def socket_ping() -> dict:
    r = run_cmd([
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}",
        "--max-time", "5", "--unix-socket", str(DOCKER_SOCK),
        "http://localhost/_ping"
    ], timeout=6)
    parts = r["stdout"].strip().split()
    code = parts[0] if parts else None
    return {"responsive": code == "200", "code": code, **r}


def docker_ps() -> dict:
    return run_cmd(["docker", "ps"], timeout=10)


def host_port_forward() -> dict:
    # Run a disposable container that exposes port 59998 to host
    run = run_cmd([
        "docker", "run", "-d", "--name", "sustained_porttest",
        "-p", "127.0.0.1:59998:80",
        "alpine", "sh", "-c",
        "while true; do (echo 'HTTP/1.1 200 OK'; echo) | nc -l -p 80; done"
    ], timeout=15)
    time.sleep(1)
    probe = run_cmd([
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "--max-time", "3", "http://127.0.0.1:59998/"
    ], timeout=4)
    cleanup = run_cmd(["docker", "rm", "-f", "sustained_porttest"], timeout=10)
    return {"run": run, "probe": probe, "cleanup": cleanup}


def io_errors_since(since: datetime) -> list[str]:
    if not INIT_LOG.exists():
        return []
    r = run_cmd(["tail", "-n", "100", str(INIT_LOG)], timeout=5)
    errors = []
    for line in r["stdout"].splitlines():
        if any(k in line for k in ["I/O error", "journal abort", "Remounting filesystem read-only"]):
            # parse timestamp
            m = __import__("re").search(r'"time":"([^"]+)"', line)
            if m:
                try:
                    ts = datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
                    if ts >= since:
                        errors.append(line[:200])
                except Exception:
                    pass
            else:
                errors.append(line[:200])
    return errors


def main() -> None:
    start = datetime.now(timezone.utc)
    duration_sec = 180
    interval_sec = 30
    samples = []
    errors = []
    print(f"Observer start: {now_iso()}, duration: {duration_sec}s")

    elapsed = 0
    while elapsed < duration_sec:
        sample = {
            "at": now_iso(),
            "socket_ping": socket_ping(),
            "docker_ps": docker_ps(),
            "host_port_forward": host_port_forward(),
            "io_errors_since_start": io_errors_since(start),
        }
        samples.append(sample)
        errors.extend(sample["io_errors_since_start"])
        print(f"[{elapsed}s] socket={sample['socket_ping']['code']} ps={sample['docker_ps']['exit_code']} port={sample['host_port_forward']['probe']['stdout']} io_errors={len(sample['io_errors_since_start'])}")
        time.sleep(interval_sec)
        elapsed += interval_sec

    receipt = {
        "start_time": start.isoformat().replace("+00:00", "Z"),
        "end_time": now_iso(),
        "duration_sec": duration_sec,
        "interval_sec": interval_sec,
        "sample_count": len(samples),
        "all_socket_responsive": all(s["socket_ping"]["responsive"] for s in samples),
        "all_docker_ps_ok": all(s["docker_ps"]["exit_code"] == 0 for s in samples),
        "all_host_port_forward_ok": all(s["host_port_forward"]["probe"]["stdout"].strip() == "200" for s in samples),
        "total_new_io_errors": len(errors),
        "samples": samples,
    }

    out_path = OUT / "docker_sustained_validation.json"
    out_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Observer done. Sustained validation written to {out_path}")


if __name__ == "__main__":
    main()
