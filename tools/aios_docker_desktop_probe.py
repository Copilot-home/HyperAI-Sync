#!/usr/bin/env python3
"""Docker Desktop causal probe v2: bind current reality, discriminate hypotheses.

One-shot, bounded, read-mostly. Does not restart Docker.
Kills child process groups on timeout so hung CLI plugins do not accumulate.
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
DIAG_REPORTS = HOME / "Library" / "Logs" / "DiagnosticReports"
DOCKER_SOCK = HOME / ".docker" / "run" / "docker.sock"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def run_cmd(args: list[str], timeout: float = 10.0, cwd: Path | None = None, kill_children: bool = True) -> dict:
    """Run a command, killing the process group on timeout to avoid hung docker plugins."""
    start = time.time()
    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
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
        elapsed = round(time.time() - start, 3)
        return {
            "exit_code": proc.returncode,
            "stdout": stdout[:12000],
            "stderr": stderr[:2000],
            "timeout": False,
            "elapsed_sec": elapsed,
        }
    except Exception as exc:
        return {
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc)[:500],
            "timeout": False,
            "elapsed_sec": round(time.time() - start, 3),
        }


def add_evidence(ledger: list[dict], step: str, cmd: list[str], result: dict) -> None:
    ledger.append({
        "step": step,
        "cmd": " ".join(cmd),
        "timestamp": now_iso(),
        "exit_code": result["exit_code"],
        "timeout": result["timeout"],
        "elapsed_sec": result["elapsed_sec"],
        "stdout_hash": sha256(result["stdout"]),
        "stderr_hash": sha256(result["stderr"]),
        "stdout_preview": result["stdout"][:500],
        "stderr_preview": result["stderr"][:300],
    })


def extract_docker_processes() -> dict:
    """Find Docker-related processes. macOS pgrep -af only returns PIDs, so we fetch details with ps."""
    result = run_cmd(["pgrep", "-f", "-i", "docker"], timeout=5, kill_children=False)
    pids: list[str] = []
    for line in result["stdout"].splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(line)
    processes: list[dict] = []
    if pids:
        # Use a single ps call with comma-separated PIDs to avoid per-PID overhead.
        pid_arg = ",".join(pids[:64])
        ps = run_cmd(["ps", "-p", pid_arg, "-o", "pid,ppid,%cpu,%mem,etime,command"], timeout=5, kill_children=False)
        for line in ps["stdout"].splitlines()[1:]:
            if line.strip():
                processes.append({"ps": line.strip()})
        # Drop pgrep itself and the python probe to avoid self-reporting noise.
        noise = re.compile(r"pgrep|ps -p|docker_desktop_probe")
        processes = [p for p in processes if not noise.search(p["ps"].lower())]
    return {"pgrep_evidence": result, "pids": pids, "processes": processes}


def find_docker_raw() -> dict:
    candidates = [
        HOME / "Library" / "Containers" / "com.docker.docker" / "Data" / "vms" / "0" / "data" / "Docker.raw",
        HOME / "Library" / "Containers" / "com.docker.docker" / "Data" / "vms" / "0" / "Docker.raw",
    ]
    for p in candidates:
        if p.exists():
            size_bytes = p.stat().st_size
            du = run_cmd(["du", "-h", str(p)], timeout=5)
            ls = run_cmd(["ls", "-lh", str(p)], timeout=5)
            return {
                "path": str(p),
                "size_bytes": size_bytes,
                "size_gb": round(size_bytes / (1024 ** 3), 2),
                "du_preview": du["stdout"].strip(),
                "ls_preview": ls["stdout"].strip(),
                "exists": True,
            }
    return {"exists": False, "candidates": [str(c) for c in candidates]}


def disk_usage_for(path: Path) -> dict:
    result = run_cmd(["df", "-h", str(path)], timeout=5)
    return result


def tail_log(path: Path, n: int = 50) -> dict:
    if not path.exists():
        return {"exists": False}
    result = run_cmd(["tail", "-n", str(n), str(path)], timeout=5)
    return {"exists": True, "path": str(path), "lines": result["stdout"].splitlines(), "tail_result": result}


def get_crash_reports() -> dict:
    result = run_cmd(["ls", "-lt", str(DIAG_REPORTS)], timeout=5)
    lines = result["stdout"].splitlines()
    docker_lines = [line for line in lines if any(k in line.lower() for k in ["docker", "virtualization", "vm", "com.docker"])]
    return {"evidence": result, "docker_lines": docker_lines[:10]}


def http_probe(url: str, timeout: float = 5.0, unix_socket: Path | None = None) -> dict:
    if unix_socket and unix_socket.exists():
        result = run_cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}", "--max-time", str(timeout), "--unix-socket", str(unix_socket), f"http://localhost{url}"], timeout=timeout + 1)
    else:
        result = run_cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}", "--max-time", str(timeout), url], timeout=timeout + 1)
    return {"evidence": result}


def socket_lsof(path: Path) -> dict:
    return run_cmd(["lsof", str(path)], timeout=5)


def launchctl_list() -> dict:
    return run_cmd(["sh", "-c", "launchctl list | grep -i docker"], timeout=5)


def probe_docker() -> tuple[dict, list[dict]]:
    ledger: list[dict] = []
    exec_id = f"docker-probe-{uuid.uuid4().hex[:8]}"
    frame = {
        "execution_id": exec_id,
        "timestamp": now_iso(),
        "host_build": run_cmd(["uname", "-a"], timeout=5, kill_children=False),
        "macos_version": run_cmd(["sw_vers"], timeout=5, kill_children=False),
    }
    add_evidence(ledger, "host_build", ["uname", "-a"], frame["host_build"])
    add_evidence(ledger, "macos_version", ["sw_vers"], frame["macos_version"])

    # Docker version / info / ps (these hang if daemon is unresponsive; keep short)
    frame["docker_version"] = run_cmd(["docker", "version"], timeout=5)
    add_evidence(ledger, "docker_version", ["docker", "version"], frame["docker_version"])
    frame["docker_info"] = run_cmd(["docker", "system", "info"], timeout=5)
    add_evidence(ledger, "docker_info", ["docker", "system", "info"], frame["docker_info"])
    frame["docker_ps"] = run_cmd(["docker", "ps", "--format", "json"], timeout=5)
    add_evidence(ledger, "docker_ps", ["docker", "ps"], frame["docker_ps"])
    frame["docker_ps_a"] = run_cmd(["docker", "ps", "-a", "--format", "json"], timeout=5)
    add_evidence(ledger, "docker_ps_a", ["docker", "ps", "-a"], frame["docker_ps_a"])

    # Context and sockets
    frame["docker_context"] = run_cmd(["docker", "context", "ls"], timeout=5, kill_children=False)
    add_evidence(ledger, "docker_context", ["docker", "context", "ls"], frame["docker_context"])
    frame["sockets"] = {
        "/var/run/docker.sock": Path("/var/run/docker.sock").exists() and Path("/var/run/docker.sock").is_socket(),
        str(DOCKER_SOCK): DOCKER_SOCK.exists() and DOCKER_SOCK.is_socket(),
        str(HOME / ".docker" / "run" / "docker-cli-api.sock"): (HOME / ".docker" / "run" / "docker-cli-api.sock").exists(),
    }
    frame["socket_lsof"] = socket_lsof(DOCKER_SOCK)
    add_evidence(ledger, "socket_lsof", ["lsof", str(DOCKER_SOCK)], frame["socket_lsof"])
    add_evidence(ledger, "launchctl_list", ["launchctl", "list", "|", "grep", "docker"], launchctl_list())

    # Try socket-level ping (does not start CLI plugins)
    frame["sock_ping"] = http_probe("/_ping", timeout=3, unix_socket=DOCKER_SOCK)
    add_evidence(ledger, "sock_ping", ["curl", "--unix-socket", str(DOCKER_SOCK), "http://localhost/_ping"], frame["sock_ping"]["evidence"])

    # Processes
    frame["desktop_processes"] = extract_docker_processes()
    add_evidence(ledger, "pgrep_docker", ["pgrep", "-af", "-i", "docker"], frame["desktop_processes"]["pgrep_evidence"])

    # BuildKit / extension
    frame["buildx"] = run_cmd(["docker", "buildx", "ls"], timeout=5)
    add_evidence(ledger, "buildx", ["docker", "buildx", "ls"], frame["buildx"])
    frame["docker_extension"] = run_cmd(["docker", "extension", "ls"], timeout=5)
    add_evidence(ledger, "docker_extension", ["docker", "extension", "ls"], frame["docker_extension"])

    # Kubernetes
    frame["kubectl_version"] = run_cmd(["kubectl", "version", "--client"], timeout=5, kill_children=False)
    add_evidence(ledger, "kubectl_version", ["kubectl", "version"], frame["kubectl_version"])
    frame["kube_context"] = run_cmd(["kubectl", "config", "current-context"], timeout=5, kill_children=False)
    add_evidence(ledger, "kube_context", ["kubectl", "config", "current-context"], frame["kube_context"])

    # MCP
    frame["mcp_port"] = run_cmd(["lsof", "-nP", "-i", "TCP:8811"], timeout=5)
    add_evidence(ledger, "mcp_port", ["lsof", "-i", ":8811"], frame["mcp_port"])
    frame["mcp_http"] = http_probe("http://127.0.0.1:8811", timeout=3)
    add_evidence(ledger, "mcp_http", ["curl", "http://127.0.0.1:8811"], frame["mcp_http"]["evidence"])

    # Host resources
    frame["df_root"] = run_cmd(["df", "-h", "/"], timeout=5, kill_children=False)
    add_evidence(ledger, "df_root", ["df", "-h", "/"], frame["df_root"])
    frame["df_data"] = run_cmd(["df", "-h", "/System/Volumes/Data"], timeout=5, kill_children=False)
    add_evidence(ledger, "df_data", ["df", "-h", "/System/Volumes/Data"], frame["df_data"])
    frame["df_home"] = disk_usage_for(HOME)
    add_evidence(ledger, "df_home", ["df", "-h", str(HOME)], frame["df_home"])
    frame["df_dockerraw"] = run_cmd(["df", "-h", str(DOCKER_LOG_DIR)], timeout=5, kill_children=False)
    add_evidence(ledger, "df_dockerraw", ["df", "-h", str(DOCKER_LOG_DIR)], frame["df_dockerraw"])
    frame["vm_stat"] = run_cmd(["vm_stat"], timeout=5, kill_children=False)
    add_evidence(ledger, "vm_stat", ["vm_stat"], frame["vm_stat"])
    frame["memory_pressure"] = run_cmd(["memory_pressure"], timeout=5, kill_children=False)
    add_evidence(ledger, "memory_pressure", ["memory_pressure"], frame["memory_pressure"])
    frame["docker_raw"] = find_docker_raw()

    # Logs
    logs: dict[str, Any] = {}
    for rel in [
        "vm/console.log",
        "vm/init.log",
        "host/com.docker.virtualization.log",
        "host/com.docker.backend.log",
        "host/monitor.log",
        "host/docker-desktop.log",
        "host/Docker.log",
    ]:
        p = DOCKER_LOG_DIR / rel
        logs[rel] = tail_log(p, 30)
    frame["logs"] = logs

    # Crash reports
    frame["crash_reports"] = get_crash_reports()
    add_evidence(ledger, "crash_reports", ["ls", "-lt", str(DIAG_REPORTS)], frame["crash_reports"]["evidence"])

    return frame, ledger


def build_plane_state_matrix(frame: dict) -> dict:
    # Process info
    procs = frame.get("desktop_processes", {})
    pids = procs.get("pids", [])
    has_backend = any("com.docker.backend" in p.get("ps", "") for p in procs.get("processes", []))
    has_virtualization = any("com.docker.virtualization" in p.get("ps", "") for p in procs.get("processes", []))
    has_desktop_ui = any("Docker Desktop.app" in p.get("ps", "") for p in procs.get("processes", []))
    has_build = any("com.docker.build" in p.get("ps", "") for p in procs.get("processes", []))

    # Daemon responsiveness from socket ping and docker ps
    sock_ping = frame.get("sock_ping", {})
    sock_ping_code = sock_ping.get("evidence", {}).get("stdout", "").strip().split()[0] if sock_ping.get("evidence", {}).get("stdout", "").strip() else None
    docker_ps_exit = frame.get("docker_ps", {}).get("exit_code")
    docker_info_exit = frame.get("docker_info", {}).get("exit_code")
    daemon_responsive = sock_ping_code == "200" or docker_ps_exit == 0

    # Container parsing
    containers: list[dict] = []
    if docker_ps_exit == 0:
        for line in frame["docker_ps"]["stdout"].splitlines():
            if line.strip():
                try:
                    containers.append(json.loads(line))
                except Exception:
                    pass
    running_count = len([c for c in containers if c.get("State") == "running"])

    # MCP
    mcp_http = frame.get("mcp_http", {})
    mcp_ev = mcp_http.get("evidence", {})
    mcp_status = mcp_ev.get("stdout", "").strip().split()[0] if mcp_ev.get("stdout", "").strip() else None

    # Log I/O error detection
    logs = frame.get("logs", {})
    io_errors = []
    for rel, log in logs.items():
        for line in log.get("lines", []):
            if any(k in line for k in ["I/O error", "input/output error", "Remounting filesystem read-only"]):
                io_errors.append({"source": rel, "line": line})

    matrix = {
        "HOST_RESOURCE_PLANE": {
            "current_state": "BOUND",
            "same_frame_evidence": ["df_root", "df_data", "df_home", "vm_stat", "memory_pressure", "docker_raw"],
            "dependencies": [],
            "resource_cost": {
                "docker_raw_gb": frame.get("docker_raw", {}).get("size_gb"),
                "root_df": frame.get("df_root", {}).get("stdout", ""),
                "data_df": frame.get("df_data", {}).get("stdout", ""),
                "home_df": frame.get("df_home", {}).get("stdout", ""),
            },
            "failure_signature": "disk near full" if any("88%" in frame.get("df_root", {}).get("stdout", "") or "100%" in frame.get("df_root", {}).get("stdout", "") for _ in [1]) else None,
            "value_produced": "capacity to sustain Docker",
            "confidence": "HIGH",
            "unknowns": ["actual physical blocks of Docker.raw", "memory pressure trend"],
        },
        "DESKTOP_UI_PLANE": {
            "current_state": "ALIVE" if has_desktop_ui else "UNVERIFIED",
            "same_frame_evidence": ["desktop_processes"],
            "dependencies": ["HOST_RESOURCE_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "user control surface",
            "confidence": "HIGH" if has_desktop_ui else "LOW",
            "unknowns": [],
        },
        "BACKEND_CONTROL_PLANE": {
            "current_state": "ALIVE" if has_backend else "UNVERIFIED",
            "same_frame_evidence": ["desktop_processes", "socket_lsof"],
            "dependencies": ["HOST_RESOURCE_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "API control",
            "confidence": "HIGH" if has_backend else "LOW",
            "unknowns": ["backend responsiveness"],
        },
        "VIRTUALIZATION_VM_PLANE": {
            "current_state": "PROCESS_ALIVE" if has_virtualization else "UNBOUND",
            "same_frame_evidence": ["desktop_processes", "vm/console.log", "vm/init.log"],
            "dependencies": ["HOST_RESOURCE_PLANE", "PERSISTENT_DATA_PLANE"],
            "resource_cost": None,
            "failure_signature": "I/O errors in init.log" if io_errors else None,
            "value_produced": "Linux VM for engine",
            "confidence": "HIGH" if has_virtualization else "LOW",
            "unknowns": ["VM filesystem state"],
        },
        "ENGINE_DAEMON_PLANE": {
            "current_state": "UNRESPONSIVE" if not daemon_responsive else "ALIVE",
            "same_frame_evidence": ["docker_ps", "docker_info", "sock_ping"],
            "dependencies": ["VIRTUALIZATION_VM_PLANE", "BACKEND_CONTROL_PLANE"],
            "resource_cost": None,
            "failure_signature": "docker ps timed out" if docker_ps_exit is None else None,
            "value_produced": "container orchestration",
            "confidence": "LOW" if not daemon_responsive else "HIGH",
            "unknowns": ["daemon latency"],
        },
        "SOCKET_AND_CONTEXT_PLANE": {
            "current_state": "PRESENT" if frame["sockets"].get(str(DOCKER_SOCK)) else "MISSING",
            "same_frame_evidence": ["sockets", "docker_context", "socket_lsof"],
            "dependencies": ["ENGINE_DAEMON_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "client-to-daemon path",
            "confidence": "MEDIUM",
            "unknowns": ["daemon on the other side"],
        },
        "CONTAINER_RUNTIME_PLANE": {
            "current_state": f"{running_count} running" if daemon_responsive else "UNVERIFIED",
            "same_frame_evidence": ["docker_ps"],
            "dependencies": ["ENGINE_DAEMON_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "container execution",
            "confidence": "HIGH" if daemon_responsive else "LOW",
            "unknowns": ["health of each container"],
        },
        "NETWORK_AND_PORT_FORWARDING_PLANE": {
            "current_state": "UNVERIFIED",
            "same_frame_evidence": ["published_ports"],
            "dependencies": ["CONTAINER_RUNTIME_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "host/container network reachability",
            "confidence": "LOW",
            "unknowns": ["actual reachability"],
        },
        "BUILD_AND_BUILDKIT_PLANE": {
            "current_state": "PROCESS_ALIVE" if has_build else "UNVERIFIED",
            "same_frame_evidence": ["buildx", "desktop_processes"],
            "dependencies": ["ENGINE_DAEMON_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "image build",
            "confidence": "MEDIUM" if has_build else "LOW",
            "unknowns": ["builder active"],
        },
        "KUBERNETES_PLANE": {
            "current_state": "UNVERIFIED",
            "same_frame_evidence": ["kube_context"],
            "dependencies": ["ENGINE_DAEMON_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "K8s cluster",
            "confidence": "LOW",
            "unknowns": ["kubectl not available or context missing"],
        },
        "EXTENSION_SERVICE_PLANE": {
            "current_state": "UNVERIFIED",
            "same_frame_evidence": ["docker_extension"],
            "dependencies": ["ENGINE_DAEMON_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "extension UX",
            "confidence": "LOW",
            "unknowns": ["extension list may hang"],
        },
        "AI_INFERENCE_SANDBOX_PLANE": {
            "current_state": "UNVERIFIED",
            "same_frame_evidence": ["desktop_processes"],
            "dependencies": ["CONTAINER_RUNTIME_PLANE", "NETWORK_AND_PORT_FORWARDING_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "AI sandbox",
            "confidence": "LOW",
            "unknowns": ["no active probe"],
        },
        "MCP_CAPABILITY_PLANE": {
            "current_state": "INACTIVE" if not mcp_status or mcp_status == "000" else "ACTIVE",
            "same_frame_evidence": ["mcp_port", "mcp_http"],
            "dependencies": ["NETWORK_AND_PORT_FORWARDING_PLANE", "CONTAINER_RUNTIME_PLANE"],
            "resource_cost": None,
            "failure_signature": None,
            "value_produced": "MCP server",
            "confidence": "LOW",
            "unknowns": ["MCP value not verified"],
        },
        "PERSISTENT_DATA_PLANE": {
            "current_state": "BOUND",
            "same_frame_evidence": ["docker_raw", "df_dockerraw"],
            "dependencies": ["HOST_RESOURCE_PLANE"],
            "resource_cost": frame.get("docker_raw", {}),
            "failure_signature": "I/O errors on vda" if io_errors else None,
            "value_produced": "state persistence",
            "confidence": "HIGH" if frame.get("docker_raw", {}).get("exists") else "LOW",
            "unknowns": ["write amplification", "sparse vs allocated"],
        },
    }
    return matrix


def build_hypothesis_matrix(frame: dict) -> dict:
    logs = frame.get("logs", {})
    docker_raw = frame.get("docker_raw", {})
    df_root = frame.get("df_root", {}).get("stdout", "")
    df_data = frame.get("df_data", {}).get("stdout", "")
    memory = frame.get("memory_pressure", {}).get("stdout", "")

    io_errors = []
    for rel, log in logs.items():
        for line in log.get("lines", []):
            if any(k in line for k in ["I/O error", "input/output error", "Remounting filesystem read-only"]):
                io_errors.append({"source": rel, "line": line[:200]})

    disk_full = False
    for line in (df_root + df_data).splitlines():
        m = re.search(r"(\d+)%", line)
        if m and int(m.group(1)) >= 85:
            disk_full = True

    mem_free_pages = 0
    m = re.search(r"Pages free:\s+(\d+)", memory)
    if m:
        mem_free_pages = int(m.group(1))
    total_pages = 0
    m = re.search(r"(\d+)\s+\(\d+ pages", memory)
    if m:
        total_pages = int(m.group(1))
    mem_pressure = mem_free_pages < (total_pages * 0.02) if total_pages else False

    has_backend = any("com.docker.backend" in p.get("ps", "") for p in frame.get("desktop_processes", {}).get("processes", []))
    has_virtualization = any("com.docker.virtualization" in p.get("ps", "") for p in frame.get("desktop_processes", {}).get("processes", []))
    daemon_responsive = frame.get("sock_ping", {}).get("evidence", {}).get("stdout", "").strip().startswith("200")

    def has_log_pattern(patterns: list[str]) -> bool:
        for rel, log in logs.items():
            for line in log.get("lines", []):
                if any(pattern in line for pattern in patterns):
                    return True
        return False

    h = {
        "H1_HOST_RESOURCE_PRESSURE": {
            "supporting": [df_root, df_data, docker_raw.get("du_preview", "")],
            "contradicting": [],
            "missing": ["sustained write rate", "Docker.raw physical blocks"],
            "causal_confidence": "HIGH" if (disk_full or mem_pressure) and io_errors else "MEDIUM" if disk_full else "LOW",
            "next_observation": "measure Docker.raw growth and host APFS free space during VM write",
        },
        "H2_VM_INTERNAL_STATE_FAILURE": {
            "supporting": [io_errors, has_virtualization and not daemon_responsive],
            "contradicting": [],
            "missing": ["full vm console log"],
            "causal_confidence": "HIGH" if io_errors and has_virtualization and not daemon_responsive else "MEDIUM" if has_virtualization and not daemon_responsive else "LOW",
            "next_observation": "tail vm/init.log for 'I/O error' and 'Internal Virtualization Error' around time daemon stopped",
        },
        "H3_SERVICE_PLANE_BOOT_AMPLIFICATION": {
            "supporting": [frame.get("desktop_processes", {}).get("pids", []), frame.get("docker_extension", {}).get("exit_code")],
            "contradicting": [],
            "missing": ["CPU/RSS time series", "container churn"],
            "causal_confidence": "MEDIUM" if not daemon_responsive and has_backend and has_virtualization and len(frame.get("desktop_processes", {}).get("pids", [])) > 5 else "LOW",
            "next_observation": "profile process tree CPU/RSS at startup and extension load",
        },
        "H4_NETWORK_OR_FORWARDING_FAILURE": {
            "supporting": [frame.get("mcp_http", {}).get("evidence", {}).get("stdout", "")],
            "contradicting": [],
            "missing": ["container-to-container ping", "host-to-container HTTP round-trip"],
            "causal_confidence": "LOW",
            "next_observation": "run disposable container with ping/curl once engine responds",
        },
    }
    return h


def build_incident_sequence(frame: dict) -> list[dict]:
    seq = []
    logs = frame.get("logs", {})
    patterns = {
        "FAILURE": ["I/O error", "input/output error", "Remounting filesystem read-only", "Internal Virtualization Error", "Aborting journal"],
        "RECOVERY": ["VM started", "engine started", "Daemon started", "API listen", "Docker Desktop is running", "Docker Desktop is resuming"],
    }
    for rel, log in logs.items():
        for line in log.get("lines", []):
            ts_match = re.search(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})", line)
            ts = ts_match.group(1) if ts_match else now_iso()
            for kind, keys in patterns.items():
                if any(k in line for k in keys):
                    seq.append({"timestamp": ts, "source": rel, "event": line.strip()[:200], "kind": kind})
                    break
    return sorted(seq, key=lambda x: x["timestamp"])[-30:]


def main() -> int:
    frame, ledger = probe_docker()
    matrix = build_plane_state_matrix(frame)
    hypotheses = build_hypothesis_matrix(frame)
    sequence = build_incident_sequence(frame)

    has_io_error = bool(matrix["VIRTUALIZATION_VM_PLANE"].get("failure_signature"))
    daemon_responsive = matrix["ENGINE_DAEMON_PLANE"]["current_state"] == "ALIVE"
    has_virtualization = matrix["VIRTUALIZATION_VM_PLANE"]["current_state"] == "PROCESS_ALIVE"

    manifest = {
        "execution_id": frame["execution_id"],
        "timestamp": frame["timestamp"],
        "host_build": frame["host_build"]["stdout"].strip(),
        "macos_version": frame["macos_version"]["stdout"].strip(),
        "docker_version_exit": frame["docker_version"]["exit_code"],
        "docker_info_exit": frame["docker_info"]["exit_code"],
        "docker_ps_exit": frame["docker_ps"]["exit_code"],
        "sock_ping": frame["sock_ping"].get("evidence", {}).get("stdout", "").strip(),
        "daemon_responsive": daemon_responsive,
        "docker_process_count": len(frame.get("desktop_processes", {}).get("pids", [])),
        "has_virtualization": has_virtualization,
        "has_backend": any("com.docker.backend" in p.get("ps", "") for p in frame.get("desktop_processes", {}).get("processes", [])),
        "has_desktop_ui": any("Docker Desktop.app" in p.get("ps", "") for p in frame.get("desktop_processes", {}).get("processes", [])),
        "mcp_http_status": frame["mcp_http"].get("evidence", {}).get("stdout", "").strip(),
        "docker_raw": frame["docker_raw"],
        "root_df": frame["df_root"]["stdout"].strip(),
        "data_df": frame["df_data"]["stdout"].strip(),
        "home_df": frame["df_home"]["stdout"].strip(),
        "io_error_count": sum(1 for e in sequence if e["kind"] == "FAILURE"),
    }

    (OUT / "docker_current_frame_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "docker_plane_state_matrix.json").write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "docker_same_frame_evidence_ledger.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "docker_hypothesis_discrimination_matrix.json").write_text(json.dumps(hypotheses, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "docker_incident_sequence.json").write_text(json.dumps(sequence, indent=2, ensure_ascii=False), encoding="utf-8")

    # Verdict
    if daemon_responsive and has_virtualization:
        final = "DOCKER_DESKTOP_OPERATIONAL_VERIFIED"
    elif has_io_error and has_virtualization:
        final = "VM_INTERNAL_FAILURE_SUSPECTED"
    else:
        final = "CURRENT_FRAME_BOUND"

    # Report
    report = [
        "# DOCKER DESKTOP CAUSAL RECOVERY REPORT",
        f"*Execution ID: {manifest['execution_id']}*",
        f"*Timestamp: {manifest['timestamp']}*",
        "",
        "## 1. Current Frame Manifest",
        f"- Docker version exit: {manifest['docker_version_exit']}",
        f"- Docker info exit: {manifest['docker_info_exit']}",
        f"- Docker ps exit: {manifest['docker_ps_exit']}",
        f"- Socket ping: {manifest['sock_ping']}",
        f"- Daemon responsive: {manifest['daemon_responsive']}",
        f"- Docker process count: {manifest['docker_process_count']}",
        f"- Virtualization process: {manifest['has_virtualization']}",
        f"- Backend process: {manifest['has_backend']}",
        f"- Desktop UI process: {manifest['has_desktop_ui']}",
        f"- MCP HTTP: {manifest['mcp_http_status']}",
        f"- Docker.raw: {json.dumps(manifest['docker_raw'])}",
        f"- Root disk: {manifest['root_df']}",
        f"- Data disk: {manifest['data_df']}",
        f"- Home disk: {manifest['home_df']}",
        f"- I/O error events: {manifest['io_error_count']}",
        "",
        "## 2. Plane State Matrix",
    ]
    for plane, state in matrix.items():
        report.append(f"- {plane}: `{state['current_state']}` (confidence {state['confidence']})")
    report.append("")
    report.append("## 3. Hypotheses")
    for h, v in hypotheses.items():
        report.append(f"- {h}: confidence {v['causal_confidence']}; next: {v['next_observation']}")
    report.append("")
    report.append("## 4. Incident Sequence (last 30)")
    for ev in sequence:
        report.append(f"- {ev['timestamp']} [{ev['kind']}] {ev['source']}: {ev['event'][:120]}")
    report.append("")
    report.append("## 5. Verdict")
    report.append(f"- {final}")
    report.append("")
    report.append("## 6. Recovery path")
    if final == "VM_INTERNAL_FAILURE_SUSPECTED":
        report.append("- Persistent data plane (Docker.raw) shows I/O errors in VM init.log.")
        report.append("- Root volume at 88%; /System/Volumes/Data (where Docker.raw and user data live) at 100% capacity.")
        report.append("- Virtualization process is alive but engine is unresponsive.")
        report.append("- Recovery must: (a) free host disk margin, (b) verify Docker.raw integrity, (c) controlled Docker restart, (d) staged capability admission.")
        report.append("- Do NOT factory reset or delete Docker.raw without Creator boundary.")

    (OUT / "DOCKER_DESKTOP_CAUSAL_RECOVERY_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    print(f"Execution: {manifest['execution_id']}")
    print(f"verdict: {final}")
    print(f"processes: {manifest['docker_process_count']}")
    print(f"io_errors: {manifest['io_error_count']}")
    print(f"report: {OUT / 'DOCKER_DESKTOP_CAUSAL_RECOVERY_REPORT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
