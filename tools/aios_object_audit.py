#!/usr/bin/env python3
"""AIOS object audit: qualify local runtime nodes per the mathematical object model.

Read-only. Checks:
- id, type, location, endpoint, capabilities, authority, state, health, lease, lineage, cost, value
- process / PID / command
- port listener
- HTTP health endpoint
- recent log tail (if available)
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urljoin
from pathlib import Path
from typing import Any

REGISTRY = Path("/Users/andy/workbench/aios_runtime_orchestrator/runtime_registry.json")
LOG_DIR = Path.home() / "Library" / "Logs"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as exc:
        return -1, "", str(exc)


def get_lsof_for_port(port: int) -> list[dict[str, str]]:
    code, out, _ = _run(["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"])
    if code != 0 or not out:
        return []
    lines = out.strip().splitlines()
    result = []
    header = lines[0].split() if lines else []
    for ln in lines[1:]:
        parts = re.split(r"\s+", ln.strip())
        if len(parts) >= 10:
            result.append({
                "command": parts[0],
                "pid": parts[1],
                "user": parts[2],
                "fd": parts[3],
                "node": parts[7] if len(parts) > 7 else "",
                "name": parts[8] if len(parts) > 8 else "",
            })
    return result


def get_ps_for_command(name: str) -> list[dict[str, str]]:
    code, out, _ = _run(["ps", "-ef"])
    if code != 0 or not out:
        return []
    matches = []
    for ln in out.splitlines():
        if name.lower() in ln.lower():
            parts = ln.split(None, 7)
            if len(parts) >= 8:
                matches.append({"uid": parts[0], "pid": parts[1], "ppid": parts[2], "command": parts[7]})
    return matches


def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 5) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, headers=headers or {}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(512)
            return {"status": r.status, "reachable": True, "sample": body.decode("utf-8", "replace")[:120]}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "reachable": True, "sample": str(e)[:120]}
    except Exception as e:
        return {"status": None, "reachable": False, "sample": str(e)[:120]}


def infer_log_path(node_id: str) -> str | None:
    candidates = [
        LOG_DIR / f"{node_id}.log",
        LOG_DIR / f"{node_id.replace('_', '-')}.log",
        LOG_DIR / f"{node_id.replace('_', '.')}.log",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def tail_log(path: str | None, lines: int = 5) -> str:
    if not path or not Path(path).exists():
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
            return "".join(all_lines[-lines:])
    except Exception as e:
        return f"log read error: {e}"


def artifact_exists(surfaces: dict[str, Any]) -> tuple[bool, str]:
    for key in ["script", "registry_path", "cli_path", "callable", "state", "journal", "canon_path", "codex_config", "mcp_config"]:
        val = surfaces.get(key)
        if val:
            p = Path(val)
            if p.exists():
                return True, str(p)
            # try relative to known roots
            for root in [Path.home(), Path("/Users/andy/HyperAI-Sync"), Path("/Users/andy/workbench/aios_runtime_orchestrator")]:
                p2 = root / val
                if p2.exists():
                    return True, str(p2)
    return False, "no artifact"


def determine_health(
    port: int | None,
    listeners: list[dict],
    http: dict[str, Any],
    procs: list[dict],
    surfaces: dict[str, Any],
) -> tuple[str, str]:
    if port:
        if not listeners and not procs:
            return "FAILED", "no process and no listener"
        if not listeners and procs:
            return "DEGRADED", f"process exists ({procs[0]['pid']}) but no listener"
        if listeners:
            if http.get("reachable"):
                if 200 <= (http.get("status") or 0) < 300:
                    return "HEALTHY", f"{listeners[0]['command']} pid {listeners[0]['pid']} listening, HTTP {http['status']}"
                if http.get("status") in (401, 403, 404):
                    return "PARTIAL", f"{listeners[0]['command']} pid {listeners[0]['pid']} listening, HTTP {http['status']} (auth/endpoint mismatch)"
            return "PARTIAL", f"{listeners[0]['command']} pid {listeners[0]['pid']} listening, HTTP {http.get('status')}"
    # no port: conceptual / script / registry
    if procs:
        return "HEALTHY", f"process exists ({procs[0]['pid']})"
    ok, path = artifact_exists(surfaces)
    if ok:
        return "HEALTHY", f"artifact exists: {path}"
    return "DEGRADED", "no process and no artifact"


def main() -> int:
    registry = json.loads(REGISTRY.read_text())
    nodes = registry.get("nodes", [])

    audit = []
    for node in nodes:
        node_id = node.get("id", "unknown")
        node["type"] = node.get("kind", node.get("type", "UNKNOWN"))
        node_type = node["type"]
        surfaces = node.get("surfaces", {})
        defaults = node.get("defaults", {})
        gates = node.get("gates", {})

        base_url = surfaces.get("base_url") or surfaces.get("frontend_url") or ""
        health_path = (
            surfaces.get("health_path")
            or surfaces.get("api_path")
            or surfaces.get("models_path")
            or ""
        )
        port = defaults.get("port") or defaults.get("daemon_port")

        # Process
        procs = []
        for keyword in [node_id, surfaces.get("name", "")]:
            if keyword and keyword not in ("unknown", "unspecified", "aios", "hyperai"):
                procs.extend(get_ps_for_command(keyword))
        procs = [dict(t) for t in {tuple(d.items()) for d in procs}]  # dedup

        # Listener
        listeners = []
        if port:
            listeners = get_lsof_for_port(port)

        # HTTP
        http = {}
        if base_url and health_path:
            http = http_get(urljoin(base_url.rstrip("/") + "/", health_path))
        elif base_url:
            http = http_get(base_url)

        # Log tail
        log_path = infer_log_path(node_id)
        log_tail = tail_log(log_path, 3)

        # Health
        health, health_note = determine_health(port, listeners, http, procs, surfaces)

        qualified = True
        missing = []
        for f in ["id", "type", "state", "authority", "lineage", "health", "cost", "value"]:
            # map object fields from registry structure
            val = node.get(f) or node.get(f.replace("_", "")) or surfaces.get(f)
            if not val:
                if f == "health":
                    val = health
                    node["health"] = health
                elif f == "state":
                    val = "declared"
                    node["state"] = "declared"
                elif f == "authority":
                    val = node.get("role", "unknown")
                    node["authority"] = val
                elif f == "lineage":
                    val = node.get("owner", "unknown")
                    node["lineage"] = val
                elif f == "cost":
                    val = "unmeasured"
                    node["cost"] = val
                elif f == "value":
                    val = node.get("role", "unknown")
                    node["value"] = val
                else:
                    missing.append(f)
                    qualified = False

        audit.append({
            "id": node_id,
            "type": node_type,
            "location": node.get("owner") or defaults.get("host", ""),
            "endpoint": base_url,
            "port": port,
            "capabilities": list(surfaces.keys()),
            "authority": node.get("authority", node.get("role", "unknown")),
            "state": node.get("state", "declared"),
            "health": health,
            "health_note": health_note,
            "lease": defaults,
            "lineage": node.get("lineage", node.get("owner", "unknown")),
            "cost": node.get("cost", "unmeasured"),
            "value": node.get("value", node.get("role", "unknown")),
            "processes": procs[:3],
            "listeners": listeners[:2],
            "http_probe": http,
            "log_path": log_path,
            "log_tail": log_tail[:200],
            "qualified": qualified,
            "missing_fields": missing,
            "gates": gates,
            "timestamp": now_iso(),
        })

    out = {
        "audited_at": now_iso(),
        "total_nodes": len(audit),
        "qualified_count": sum(1 for n in audit if n["qualified"]),
        "health_summary": {h: sum(1 for n in audit if n["health"] == h) for h in ["HEALTHY", "PARTIAL", "DEGRADED", "STALE", "FAILED", "UNKNOWN"]},
        "nodes": audit,
    }

    out_path = Path("/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/aios_object_audit_20260730.json")
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out["health_summary"], indent=2))
    print(f"\nFull audit written to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
