#!/usr/bin/env python3
"""APΩ Living Loop — one closed-cycle execution.

WAKE → OBSERVE → IDENTIFY NEED → SELECT PURPOSE → ASSIGN MISSIONS
→ EXCHANGE INFORMATION → EXECUTE → VERIFY → LEARN → UPDATE MEMORY → SELECT NEXT ACTION
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runtime" / "federation_orchestrator"
WORKBENCH = Path("/Users/andy/workbench/aios_runtime_orchestrator")
APO_CONFIG = Path("/Users/andy/.apo/gateway/apo_config.yaml")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(data: Any, p: Path) -> None:
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Artifact generator with corrected ontology
# ---------------------------------------------------------------------------

def base_app_for(node: dict, proc: dict | None) -> str:
    """Return the actual OS app / process name, not just kind."""
    surfaces = node.get("surfaces", {})
    for key in ("app_bundle", "name", "registry_path", "script", "mcp_server_path", "backend_file", "codex_config"):
        v = surfaces.get(key)
        if v:
            return v
    if proc:
        # prefer the script path in cmdline (e.g. servers/slack/main.py)
        for arg in proc.get("cmdline") or []:
            if "/servers/" in arg or "main.py" in arg or arg.endswith(".py"):
                return arg
        return proc.get("name") or proc.get("exe")
    return node.get("kind", "unknown")


def capabilities_for(node: dict) -> list[str]:
    caps = []
    kind = node.get("kind", "")
    if "provider" in kind or "model" in kind or "inference" in kind:
        caps.append("inference")
    if "tool" in kind:
        caps.append(f"tool:{node['id'].replace('openapi_tool_', '').replace('_', '-')}")
    if "mcp" in kind:
        caps.append("mcp-bridge")
    if "broker" in kind:
        caps.append("auth-lease")
        caps.append("proxy")
    if "gateway" in kind:
        caps.append("route")
        caps.append("proxy")
    if "memory" in kind or "cache" in kind:
        caps.append("store")
        caps.append("recall")
    if "worker" in kind or "operator" in kind:
        caps.append("execute")
    if "product" in kind or "app_runtime" in kind:
        caps.append("product-ui")
    if "infra" in kind or "container" in kind:
        caps.append("container-fabric")
    if "root" in kind or "orchestrator" in kind or "registry" in kind:
        caps.append("orchestrate")
        caps.append("route")
    # surfaces
    for k, v in node.get("surfaces", {}).items():
        if k in ("base_url", "models_path", "tools_path", "sse_path", "api_path") and v:
            caps.append(k)
    return caps or ["unknown"]


def lanes_for(node_id: str, role: str) -> list[str]:
    primary = {
        "aios_mission_router": ["ROUTING"],
        "federation_orchestrator": ["ROUTING", "PLANNING"],
        "apo_gateway": ["ROUTING"],
        "credential_broker": ["AUTH"],
        "ollama_macbook": ["KNOWLEDGE"],
        "apo_upstream_macbook_ollama": ["KNOWLEDGE"],
        "apo_upstream_lmstudio": ["KNOWLEDGE"],
        "lmstudio_bionic_api": ["KNOWLEDGE"],
        "finalai": ["KNOWLEDGE"],
        "openapi_tool_google_pse": ["KNOWLEDGE", "EXECUTION"],
        "openapi_tool_slack": ["COMMUNICATION", "EXECUTION", "KNOWLEDGE"],
        "redis_local": ["MEMORY"],
        "memory_writer": ["MEMORY"],
        "hyperai_product_runtime": ["PRODUCT"],
        "docker_desktop": ["INFRASTRUCTURE"],
        "agent_os_dashboard": ["PLANNING", "EXECUTION"],
        "bionic_app": ["EXECUTION"],
        "codex_operator_runtime": ["EXECUTION"],
        "mcp_pieces": ["EXECUTION"],
        "pieces_mcp": ["EXECUTION"],
        "mcp_docker_mcp": ["EXECUTION"],
    }
    if node_id in primary:
        return primary[node_id]
    if node_id.startswith("openapi_tool_"):
        return ["EXECUTION"]
    if node_id.startswith("apo_upstream_"):
        return ["KNOWLEDGE"]
    role_l = (role or "").lower()
    if role_l == "root" or role_l == "orchestrator":
        return ["ROUTING"]
    if role_l == "provider":
        return ["KNOWLEDGE"]
    if role_l == "tool":
        return ["EXECUTION"]
    if role_l == "mcp":
        return ["EXECUTION"]
    if role_l == "worker":
        return ["EXECUTION"]
    if role_l == "memory":
        return ["MEMORY"]
    if role_l == "broker":
        return ["AUTH"]
    if role_l == "product":
        return ["PRODUCT"]
    if role_l == "infra":
        return ["INFRASTRUCTURE"]
    return ["UNKNOWN"]


def host_and_state(node: dict) -> tuple[str, str]:
    state = node.get("state")
    host = node.get("host")
    if state:
        return host or "UNKNOWN", state
    base = node.get("surfaces", {}).get("base_url", "")
    host_default = node.get("defaults", {}).get("host", "")
    if host_default in ("127.0.0.1", "localhost") or "127.0.0.1" in base or "localhost" in base:
        return "MACBOOK_ACTIVE", "ACTIVE"
    if "192.168.3.84" in base or host_default == "192.168.3.84":
        return "TITAN_STANDBY", "STANDBY_UNREACHABLE"
    if "192.168.3.28" in base or host_default == "192.168.3.28":
        return "MACMINI_STANDBY", "STANDBY_UNREACHABLE"
    return "UNKNOWN_UNBOUND", "UNKNOWN_UNBOUND"


def compute_declared(node: dict) -> dict:
    d = node.get("defaults", {})
    return {
        "port": d.get("port"),
        "host": d.get("host"),
        "frontend_port": d.get("frontend_port"),
        "memory_limit_mb": None,
        "note": "declared from registry defaults",
    }


def build_upstream_downstream(node_id: str, apo: dict) -> tuple[list[str], list[str]]:
    ups: list[str] = []
    downs: list[str] = []
    # Aliases that route to this upstream
    for alias, cfg in (apo.get("aliases") or {}).items():
        if cfg.get("upstream") == node_id:
            downs.append(f"alias:{alias}")
    # Tool base urls
    for tool, cfg in (apo.get("tools") or {}).items():
        if cfg.get("base_url") and node_id in tool or node_id.replace("openapi_tool_", "") == tool:
            downs.append(f"tool:{tool}")
    # Upstream uses env key from broker
    env_key = (registry_node(node_id).get("surfaces") or {}).get("env_key")
    if env_key:
        ups.append(f"credential_broker:{env_key}")
    if node_id.startswith("openapi_tool_"):
        ups.append("apo_gateway")
        downs.append("agent_os_dashboard / memory")
    if node_id == "apo_gateway":
        ups.extend(["credential_broker", "ollama_macbook", "lmstudio_bionic_api", "openrouter"])
        downs.extend(["openapi_tool_*", "mcp_pieces", "mcp_docker_mcp"])
    if node_id == "aios_mission_router":
        ups.append("creator intent")
        downs.extend(["federation_orchestrator", "apo_gateway", "agent_os_dashboard"])
    if node_id == "credential_broker":
        ups.append("Keychain / credentials.env")
        downs.extend(["apo_gateway", "openapi_tool_slack", "openapi_tool_google_pse"])
    if node_id == "ollama_macbook" or node_id == "lmstudio_bionic_api":
        ups.append("local substrate")
        downs.append("apo_gateway")
    if node_id == "redis_local":
        ups.append("runtime writes")
        downs.append("all lanes")
    if node_id == "memory_writer":
        ups.append("verified events")
        downs.append("memory")
    return ups or ["runtime"], downs or ["ecosystem"]


def registry_node(node_id: str) -> dict:
    data = load_json(WORKBENCH / "runtime_registry.json")
    for n in data.get("nodes", []):
        if n["id"] == node_id:
            return n
    return {}


def build_capability_to_mission_map(apo: dict) -> dict:
    data = load_json(WORKBENCH / "runtime_registry.json")
    binding = load_json(OUT / "binding_plan.json")
    authority = load_json(OUT / "authority_matrix.json")
    auth = load_json(OUT / "auth_topology.json")
    snapshot = load_json(OUT / "runtime_discovery_snapshot.json")
    pid_to_proc = {p["pid"]: p for p in snapshot["processes"]}
    bind_lookup = {p["id"]: p for p in binding["plans"]}
    auth_map: dict[str, list[dict]] = defaultdict(list)
    for rec in auth["records"]:
        auth_map[rec["surface"]].append(rec)
    auth_lookup = dict(auth_map)

    caps = []
    for node in data.get("nodes", []):
        nid = node["id"]
        bind = bind_lookup.get(nid, {})
        procs = [pid_to_proc.get(x) for x in bind.get("pids", []) if x in pid_to_proc]
        first_proc = procs[0] if procs else None
        host, state = host_and_state(node)
        lanes = lanes_for(nid, node.get("role", ""))
        ups, downs = build_upstream_downstream(nid, apo)
        auth_refs = [
            {
                "key": r["required_key"],
                "status": r["status"],
                "source": r["source"],
                "consent_boundary": r["consent_boundary"],
            }
            for r in auth_lookup.get(nid, [])
        ]
        authority_entry = next((x for x in authority["entries"] if x["id"] == nid), {})
        authority_list = authority_entry.get("authority", ["OBSERVE"])
        observed_rss = sum((pr.get("memory") or {}).get("rss", 0) for pr in procs if pr)
        observed_ports = sorted(set(po for pr in procs for po in pr.get("listening_ports", []) if pr))
        caps.append({
            "node": nid,
            "base_app": base_app_for(node, first_proc),
            "ai_projection": nid,
            "capabilities": capabilities_for(node),
            "assigned_lanes": lanes,
            "upstream": ups,
            "downstream": downs,
            "authority": authority_list,
            "auth_reference": auth_refs,
            "compute_budget": compute_declared(node),
            "observed_compute": {
                "pids": [pr["pid"] for pr in procs],
                "rss_bytes": observed_rss,
                "ports": observed_ports,
                "qualified": bind.get("operationally_qualified", False),
                "missing": bind.get("missing", []),
            },
            "mission": f"operate {nid} as {'/'.join(lanes)}",
            "expected_value": f"{lanes[0].lower()} output produced",
            "failure_action": "fallback to next lane or suppress",
            "host": host,
            "host_state": state,
        })
    return {
        "generated_at": now_iso(),
        "execution_hash": sha256_file(Path(__file__)),
        "version": 2,
        "capabilities": caps,
    }


def build_ecosystem_value_flow() -> dict:
    lanes = {
        "ROUTING": {
            "nodes": ["aios_mission_router", "federation_orchestrator", "apo_gateway"],
            "input": "mission / request",
            "output": "routed call / plan",
            "upstream": "creator, runtime",
            "downstream": "all lanes",
            "authority": "OBSERVE PLAN ROUTE VERIFY",
            "compute": "gateway routing",
            "value": "correct dispatch",
            "failure": "wrong route / loop",
        },
        "AUTH": {
            "nodes": ["credential_broker"],
            "input": "capability request",
            "output": "scoped lease / proof",
            "upstream": "Keychain, OAuth, providers",
            "downstream": "execution lane",
            "authority": "AUTH VERIFY",
            "compute": "broker validation",
            "value": "secure identity",
            "failure": "unauthorized",
        },
        "SECURITY": {
            "nodes": ["security_openai_rotation"],
            "input": "exposure / drift alert",
            "output": "incident receipt / rotated credential",
            "upstream": "scanner, audit",
            "downstream": "auth lane",
            "authority": "AUDIT REVOKE ROTATE",
            "compute": "verification calls",
            "value": "continuity of trust",
            "failure": "credential compromise",
        },
        "VERIFICATION": {
            "nodes": ["verify_generated_artifacts", "health probes", "evidence collectors"],
            "input": "claim / output",
            "output": "proof / delta",
            "upstream": "all execution lanes",
            "downstream": "memory / routing",
            "authority": "OBSERVE VERIFY",
            "compute": "probe / test",
            "value": "truth preserved",
            "failure": "false claim accepted",
        },
        "KNOWLEDGE": {
            "nodes": ["ollama_macbook", "apo_upstream_macbook_ollama", "apo_upstream_lmstudio", "lmstudio_bionic_api", "finalai", "openapi_tool_google_pse"],
            "input": "query / prompt",
            "output": "model response / search result",
            "upstream": "execution / routing",
            "downstream": "execution / memory",
            "authority": "OBSERVE INVOKE READ",
            "compute": "LLM / search",
            "value": "inference value",
            "failure": "no model",
        },
        "EXECUTION": {
            "nodes": ["bionic_app", "codex_operator_runtime", "agent_os_dashboard", "mcp_pieces", "pieces_mcp", "mcp_docker_mcp", "openapi_tool_*"],
            "input": "tool call / task",
            "output": "result / side effect",
            "upstream": "routing / knowledge",
            "downstream": "memory / product",
            "authority": "OBSERVE INVOKE READ WRITE",
            "compute": "tool process",
            "value": "task completion",
            "failure": "tool failure",
        },
        "COMMUNICATION": {
            "nodes": ["openapi_tool_slack"],
            "input": "message / mention",
            "output": "sent message / reaction",
            "upstream": "routing",
            "downstream": "memory",
            "authority": "OBSERVE INVOKE READ",
            "compute": "Slack API",
            "value": "team coordination",
            "failure": "Slack unreachable",
        },
        "MEMORY": {
            "nodes": ["redis_local", "memory_writer", "openapi_tool_memory"],
            "input": "read / write",
            "output": "stored state",
            "upstream": "all lanes",
            "downstream": "all lanes",
            "authority": "OBSERVE READ WRITE",
            "compute": "redis / disk",
            "value": "continuity",
            "failure": "state loss",
        },
        "PRODUCT": {
            "nodes": ["hyperai_product_runtime"],
            "input": "user action",
            "output": "UI state",
            "upstream": "runtime",
            "downstream": "user",
            "authority": "OBSERVE READ WRITE EXECUTE",
            "compute": "frontend / backend",
            "value": "user value",
            "failure": "product down",
        },
        "INFRASTRUCTURE": {
            "nodes": ["docker_desktop"],
            "input": "container / net request",
            "output": "runtime fabric",
            "upstream": "OS",
            "downstream": "all",
            "authority": "OBSERVE ALLOCATE EXECUTE",
            "compute": "Docker daemon",
            "value": "runtime fabric",
            "failure": "Docker down",
        },
        "STANDBY_PROJECTION": {
            "nodes": ["apo_upstream_titan_ollama", "apo_upstream_macmini_ollama"],
            "input": "n/a",
            "output": "n/a",
            "upstream": "host offline",
            "downstream": "host offline",
            "authority": "NONE",
            "compute": "0",
            "value": "lineage preserved",
            "failure": "n/a",
        },
    }
    return {
        "generated_at": now_iso(),
        "execution_hash": sha256_file(Path(__file__)),
        "version": 2,
        "value_flow": lanes,
        "flow": {
            "source": "creator intent + OS processes",
            "interpret": "ROUTING lane",
            "plan": "ROUTING lane maps to capability map",
            "execute": "AUTH → KNOWLEDGE → EXECUTION/COMMUNICATION → PRODUCT",
            "verify": "SECURITY + VERIFICATION lanes",
            "record": "MEMORY lane",
        },
    }


def build_auth_recovery_execution() -> dict:
    actions = []
    # openai completed
    receipt = load_json(OUT / "security_incident_receipt.json")
    actions.append({
        "surface": "openai",
        "provider": "openai",
        "status": "COMPLETED",
        "current_status": "COMPLETED",
        "old_key_id": receipt.get("old_key_id"),
        "new_key_id": receipt.get("new_key_id"),
        "new_key_masked": receipt.get("new_key_masked"),
        "consent_boundary": "none",
        "recovery_path": "admin API: create service account -> update OPENAI_API_KEY_3 -> restart broker -> delete old user API key",
        "verification": "broker /status healthy: openai",
        "completed_at": receipt.get("timestamp"),
    })

    # slack planned
    actions.append({
        "surface": "openapi_tool_slack",
        "provider": "slack",
        "status": "PLANNED",
        "current_status": "MISSING",
        "required_scope": "channels:read, chat:write, users:read, reactions:write",
        "credential_reference": "SLACK_BOT_TOKEN / SLACK_TEAM_ID",
        "consent_boundary": "Creator must authorize Slack app install / workspace",
        "recovery_path": [
            "identify or create Slack app",
            "OAuth install to workspace",
            "broker loads SLACK_BOT_TOKEN",
            "resolve SLACK_TEAM_ID via auth.test",
            "verify with Slack API",
        ],
        "verification_probe": "GET /health on openapi_tool_slack + broker /status slack healthy",
    })

    # google pse planned
    actions.append({
        "surface": "openapi_tool_google_pse",
        "provider": "google_pse",
        "status": "PLANNED",
        "current_status": "MISSING",
        "required_scope": "customsearch.readonly",
        "credential_reference": "GOOGLE_PSE_CX",
        "consent_boundary": "Creator must confirm CSE ownership / creation",
        "recovery_path": [
            "locate existing CSE in Google console",
            "if none, create CSE as external consent action",
            "bind GOOGLE_PSE_CX",
            "verify with real search query through broker",
        ],
        "verification_probe": "GET /health on openapi_tool_google_pse + broker /status google_pse healthy",
    })

    return {
        "generated_at": now_iso(),
        "execution_hash": sha256_file(Path(__file__)),
        "version": 2,
        "actions": actions,
    }


def build_host_runtime_topology() -> dict:
    data = load_json(WORKBENCH / "runtime_registry.json")
    topology = {
        "generated_at": now_iso(),
        "execution_hash": sha256_file(Path(__file__)),
        "version": 2,
        "hosts": {
            "MACBOOK_ACTIVE": {"state": "ACTIVE_CONTROL", "ip": "127.0.0.1", "note": "all observed processes are local"},
            "TITAN_STANDBY": {"state": "MAINTENANCE_STANDBY", "ip": "192.168.3.84", "note": "do not route new workload"},
            "MACMINI_STANDBY": {"state": "STANDBY", "ip": "192.168.3.28", "note": "do not route new workload"},
            "UNKNOWN_UNBOUND": {"state": "UNKNOWN", "ip": "unknown", "note": "no host evidence"},
        },
        "nodes": [],
    }
    for node in data.get("nodes", []):
        host, state = host_and_state(node)
        topology["nodes"].append({
            "node": node["id"],
            "host": host,
            "state": state,
            "base_url": node.get("surfaces", {}).get("base_url", ""),
            "role": node.get("role", ""),
        })
    return topology


def build_process_compute_ledger() -> dict:
    snapshot = load_json(OUT / "runtime_discovery_snapshot.json")
    roles = load_json(OUT / "role_registry.json")
    pid_to_nodes: dict[int, list[str]] = defaultdict(list)
    for r in roles["roles"]:
        for pid in r.get("pids", []):
            pid_to_nodes[pid].append(r["id"])

    entries = []
    totals: dict[str, dict] = defaultdict(lambda: {"count": 0, "rss": 0})
    unknown_pids = []
    for pr in snapshot["processes"]:
        pid = pr["pid"]
        nodes = pid_to_nodes.get(pid, [])
        if nodes:
            lanes = [l for n in nodes for l in lanes_for(n, "")]
            mission = " / ".join(f"operate {n}" for n in nodes)
            system = "DAIOF"
        else:
            name = pr.get("name", "")
            exe = pr.get("exe", "")
            if ".app" in exe or name.endswith(".app") or any(x in name for x in ["Helper", "IDE", "Desktop", "Chrome", "LM Studio", "Ollama", "Pieces"]):
                system = "NATIVE_APP"
                lanes = ["NATIVE"]
                mission = "native OS app / support process"
            else:
                system = "UNKNOWN_UNBOUND"
                lanes = ["UNKNOWN"]
                mission = "unknown - assign to discovery/security lane"
                unknown_pids.append(pid)
        rss = (pr.get("memory") or {}).get("rss", 0)
        totals[system]["count"] += 1
        totals[system]["rss"] += rss
        entries.append({
            "pid": pid,
            "name": pr.get("name"),
            "exe": pr.get("exe"),
            "system": system,
            "lanes": lanes,
            "mission": mission,
            "rss_bytes": rss,
            "listening_ports": pr.get("listening_ports", []),
        })
    return {
        "generated_at": now_iso(),
        "execution_hash": sha256_file(Path(__file__)),
        "version": 2,
        "total_processes": len(snapshot["processes"]),
        "total_rss_bytes": sum((pr.get("memory") or {}).get("rss", 0) for pr in snapshot["processes"]),
        "unknown_pids": unknown_pids,
        "system_totals": dict(totals),
        "processes": entries,
    }


def build_active_dispatch_report(cap_map: dict, flow: dict, ledger: dict, host: dict, auth_rec: dict) -> str:
    caps = cap_map["capabilities"]
    qualified = sum(1 for c in caps if c["observed_compute"]["qualified"])
    lines = [
        "# ACTIVE DISPATCH REPORT",
        f"*Generated: {now_iso()}*",
        f"*Execution hash: {cap_map['execution_hash']}*",
        "",
        "## Executive Summary",
        f"- Processes observed: {ledger['total_processes']}",
        f"- Registry nodes: {len(caps)}",
        f"- Operationally qualified: {qualified}/{len(caps)}",
        f"- OpenAI credential rotated: {load_json(OUT / 'security_incident_receipt.json').get('timestamp')}",
        f"- Titan/MacMini Ollama projections: STANDBY_UNREACHABLE",
        f"- Unknown unbound processes: {len(ledger['unknown_pids'])}",
        "",
        "## Capability Map Summary",
        "| node | base_app | lanes | host | state | mission |",
        "|---|---|---|---|---|---|",
    ]
    for c in caps:
        lines.append(f"| {c['node']} | {c['base_app']} | {','.join(c['assigned_lanes'])} | {c['host']} | {c['host_state']} | {c['mission']} |")
    lines.append("")
    lines.append("## Auth Recovery Status")
    for a in auth_rec["actions"]:
        status = a.get("status", a.get("current_status", ""))
        verif = a.get("verification", a.get("verification_probe", a.get("recovery_path", "")))
        lines.append(f"- **{a['surface']}**: {status} — {verif}")
    lines.append("")
    lines.append("## Compute Ledger Summary")
    for sys, total in ledger["system_totals"].items():
        lines.append(f"- {sys}: {total['count']} processes, {total['rss']} bytes RSS")
    lines.append("")
    lines.append("## Value Flow")
    lines.append(f"- source → {flow['flow']['source']}")
    lines.append(f"- interpret/plan → {flow['flow']['interpret']}")
    lines.append(f"- execute → {flow['flow']['execute']}")
    lines.append(f"- verify → {flow['flow']['verify']}")
    lines.append(f"- record → {flow['flow']['record']}")
    lines.append("")
    lines.append("## Stopping Conditions")
    lines.append("- Any external provider returns 401/403 after credential rotation.")
    lines.append("- Broker /status returns openai unhealthy.")
    lines.append("- Canon change attempted without receipt or rollback path.")
    lines.append("- Plaintext secret detected in any artifact.")
    return "\n".join(lines)


def generate_artifacts() -> None:
    apo = yaml.safe_load(APO_CONFIG.read_text(encoding="utf-8"))
    cap = build_capability_to_mission_map(apo)
    flow = build_ecosystem_value_flow()
    ledger = build_process_compute_ledger()
    host = build_host_runtime_topology()
    auth_rec = build_auth_recovery_execution()
    report = build_active_dispatch_report(cap, flow, ledger, host, auth_rec)
    save_json(cap, OUT / "capability_to_mission_map.json")
    save_json(flow, OUT / "ecosystem_value_flow.json")
    save_json(auth_rec, OUT / "auth_recovery_execution.json")
    save_json(host, OUT / "host_runtime_topology.json")
    save_json(ledger, OUT / "process_compute_ledger.json")
    (OUT / "active_dispatch_report.md").write_text(report, encoding="utf-8")
    # Do not overwrite security_incident_receipt.json; it is produced by rotation.


# ---------------------------------------------------------------------------
# Living loop execution
# ---------------------------------------------------------------------------

def run_qualifier() -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "aios_runtime_qualification.py")],
        cwd=str(OUT),
        check=True,
    )
    return load_json(OUT / "binding_plan.json")


def health_probe(url: str, timeout: float = 5.0) -> dict:
    try:
        r = httpx.get(url, timeout=timeout)
        return {"url": url, "status": r.status_code, "ok": r.status_code == 200, "body_preview": r.text[:200]}
    except Exception as e:
        return {"url": url, "status": 0, "ok": False, "error": str(e)}


def broker_status() -> dict:
    return health_probe("http://127.0.0.1:8765/status")


def apo_gateway_health() -> dict:
    return health_probe("http://127.0.0.1:9011/health")


def time_probe() -> dict:
    # Execute through apo_gateway /tools/time/get_current_utc_time
    url = "http://127.0.0.1:9011/tools/time/get_current_utc_time"
    try:
        r = httpx.get(url, timeout=10.0)
        return {
            "url": url,
            "status": r.status_code,
            "ok": r.status_code == 200,
            "body": r.json() if r.status_code == 200 and r.text else r.text[:200],
        }
    except Exception as e:
        return {"url": url, "status": 0, "ok": False, "error": str(e)}


def load_state() -> dict:
    p = ROOT / "memory" / "project_state.json"
    if p.exists():
        return load_json(p)
    return {}


def save_state(state: dict) -> None:
    (ROOT / "memory" / "project_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_journal(entry: str) -> None:
    p = ROOT / "memory" / "work_journal.md"
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n## {now_iso()}\n{entry}\n")


def append_todo(item: str) -> None:
    p = ROOT / "memory" / "runtime_execution_todo.md"
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n## AIOS Runtime Queue Item - {now_iso()}\n{item}\n")


def select_next_action() -> str:
    binding = load_json(OUT / "binding_plan.json")
    not_qualified = [p for p in binding["plans"] if not p["operationally_qualified"]]
    if not not_qualified:
        return "all nodes qualified; enter continuous verification mode"
    # priority: auth gaps first, then unobserved runtimes
    auth_gaps = [p for p in not_qualified if any(m.startswith("auth:") for m in p["missing"])]
    if auth_gaps:
        n = auth_gaps[0]
        return f"resolve auth for {n['id']}: {', '.join(n['missing'])}"
    unobs = [p for p in not_qualified if "observed_runtime" in p["missing"]]
    if unobs:
        n = unobs[0]
        return f"qualify or suppress {n['id']} (unobserved)"
    return f"resolve {not_qualified[0]['id']}: {', '.join(not_qualified[0]['missing'])}"


def run_one_cycle() -> dict:
    log: dict = {"cycle_id": f"living-{now_iso()}", "started_at": now_iso(), "stages": {}}

    # WAKE
    previous = load_state()
    log["stages"]["WAKE"] = {"previous_mission": previous.get("last_mission"), "timestamp": now_iso()}

    # OBSERVE
    binding = run_qualifier()
    broker = broker_status()
    apo = apo_gateway_health()
    log["stages"]["OBSERVE"] = {
        "qualified": f"{binding['qualified']}/{binding['total']}",
        "broker_status": broker,
        "apo_gateway_health": apo,
        "timestamp": now_iso(),
    }

    # IDENTIFY NEED
    not_qualified = [p for p in binding["plans"] if not p["operationally_qualified"]]
    need = f"verify cross-lane execution while {len(not_qualified)} nodes remain unqualified"
    log["stages"]["IDENTIFY_NEED"] = {"need": need, "unqualified_count": len(not_qualified)}

    # SELECT PURPOSE
    purpose = "execute a closed-loop time-probe through routing, execution, and verification lanes"
    log["stages"]["SELECT_PURPOSE"] = {"purpose": purpose}

    # ASSIGN MISSIONS
    missions = {
        "ROUTING": "apo_gateway receives time request and routes to time tool",
        "AUTH": "broker status confirms credential plane alive",
        "EXECUTION": "time tool returns current UTC",
        "VERIFICATION": "check 200 + JSON time value",
        "MEMORY": "record cycle and value",
    }
    log["stages"]["ASSIGN_MISSIONS"] = missions

    # EXCHANGE INFORMATION (before execution)
    exchange = {
        "ROUTING": {"state": "ready", "endpoint": "http://127.0.0.1:9011"},
        "AUTH": {"state": broker["ok"], "endpoint": "http://127.0.0.1:8765"},
        "EXECUTION": {"state": apo["ok"], "endpoint": "http://127.0.0.1:8901"},
        "VERIFICATION": {"state": "ready"},
        "MEMORY": {"state": "ready"},
    }
    log["stages"]["EXCHANGE_INFORMATION"] = exchange

    # EXECUTE
    time_result = time_probe()
    log["stages"]["EXECUTE"] = {"time_probe": time_result}

    # VERIFY
    body = time_result.get("body") if time_result.get("ok") else {}
    verified = time_result["ok"] and isinstance(body, dict) and ("current_utc_time" in body or "utc" in body)
    log["stages"]["VERIFY"] = {"verified": verified, "criteria": "status 200 and time value present"}

    # LEARN
    learnings = {
        "openapi_tool_time_produces_value": verified,
        "apo_gateway_routing_alive": apo["ok"],
        "credential_broker_alive": broker["ok"],
        "unqualified_nodes": [p["id"] for p in not_qualified],
    }
    log["stages"]["LEARN"] = learnings

    # UPDATE MEMORY
    state = {
        "last_mission": purpose,
        "last_verified": verified,
        "last_time_value": time_result.get("body", {}).get("current_utc_time") if verified else None,
        "unqualified_count": len(not_qualified),
        "last_cycle": log["cycle_id"],
        "updated_at": now_iso(),
    }
    save_state(state)
    append_journal(
        f"Living cycle {log['cycle_id']}: time-probe via apo_gateway -> time tool "
        f"verified={verified}; broker={broker['ok']}; apo={apo['ok']}; "
        f"qualified={binding['qualified']}/{binding['total']}."
    )

    # SELECT NEXT ACTION
    next_action = select_next_action()
    log["stages"]["UPDATE_MEMORY"] = {"project_state_updated": True, "journal_appended": True}
    log["stages"]["SELECT_NEXT_ACTION"] = {"next_action": next_action}
    log["completed_at"] = now_iso()

    # Save mission execution log
    save_json(log, OUT / "mission_execution_log.json")
    append_todo(f"- mission: {purpose}\n- verified: {verified}\n- next: {next_action}")
    return log


def main() -> int:
    # Regenerate artifacts with corrected ontology before living cycle
    generate_artifacts()
    print("regenerated artifacts")
    # Run one living cycle
    log = run_one_cycle()
    print(f"living cycle completed: verified={log['stages']['VERIFY']['verified']}")
    print(f"next action: {log['stages']['SELECT_NEXT_ACTION']['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
