#!/usr/bin/env python3
"""AIOS active-runtime qualification — read-only.

Implements the active-runtime discovery / identify / assign-role /
map-authority / resolve-auth / bind-plan workflow. No compute is bound,
no runtime is started, no credential plaintext is logged.

Outputs 7 artifacts under runtime/federation_orchestrator/:
- runtime_discovery_snapshot.json
- role_registry.json
- authority_matrix.json
- auth_topology.json
- dependency_graph.json
- binding_plan.json
- operational_qualification_report.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil

# Resolve absolute roots from source location or env, not from cwd.
DEFAULT_HYPER = Path(__file__).resolve().parents[1]
HYPER = Path(os.environ.get("HYPERAI_RUNTIME_ROOT") or DEFAULT_HYPER)
RUNTIME = HYPER / "runtime" / "federation_orchestrator"
REGISTRY = Path(os.environ.get("HYPERAI_REGISTRY") or "/Users/andy/workbench/aios_runtime_orchestrator/runtime_registry.json")
APO_CONFIG = Path(os.environ.get("HYPERAI_APO_CONFIG") or (Path.home() / ".apo" / "gateway" / "apo_config.yaml"))
CREDS_ENV = Path(os.environ.get("HYPERAI_CREDS_ENV") or (Path.home() / ".config" / "hyperai" / "credentials.env"))
OUT = RUNTIME

SENSITIVE_KEY_RE = re.compile(r"\b(KEY|TOKEN|SECRET|PASSWORD|CRED|AUTH|PRIVATE|PAT|API)\b", re.I)
SECRET_VALUE_RE = re.compile(r"\b(sk-[a-zA-Z0-9_-]{24,}|gh[pousr]_[a-zA-Z0-9_]{20,}|xoxb-[a-zA-Z0-9-]{20,}|AIza[0-9A-Za-z_-]{30,})\b")
RELEVANT_OPEN_RE = re.compile(
    r"aios|hyperai|codex|\.apo|openapi|workbench|federation|runtime|memory|tools|"
    r"\.config|credentials|bionic|pieces|finalai|lmstudio|lm-studio|ollama|ngrok|docker|ngrok",
    re.I,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: list[str], timeout: int = 15) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as exc:
        return -1, "", str(exc)


def load_json(p: Path) -> Any:
    if p.exists():
        return json.loads(p.read_text())
    return None


def load_apo_config() -> dict[str, Any]:
    try:
        import yaml
        return yaml.safe_load(APO_CONFIG.read_text()) or {}
    except Exception:
        return {}


def mask_env(key: str, value: str) -> str:
    if SENSITIVE_KEY_RE.search(key) or SECRET_VALUE_RE.search(value):
        return f"<present len={len(value)}>"
    return value


def mask_secret_in(text: str) -> str:
    return SECRET_VALUE_RE.sub("<secret>", text)


def relevant_env_key(key: str) -> bool:
    keep = [
        "PATH", "HOME", "USER", "SHELL", "PWD", "PYTHON", "VIRTUAL", "CONDA",
        "BROKER", "API", "KEY", "TOKEN", "SECRET", "PASSWORD", "CRED", "URL",
        "OLLAMA", "LMSTUDIO", "BIONIC", "PIECES", "FINALAI", "OPENAI", "GOOGLE",
        "SLACK", "GITHUB", "TELEGRAM", "TON", "MCP", "MODEL", "ENV",
    ]
    return any(k.lower() in key.lower() for k in keep)


def get_cred_key_names() -> dict[str, str]:
    result = {}
    for path in [CREDS_ENV, HOME / ".env", HOME / ".zshrc", HOME / ".bash_profile", HOME / ".bashrc"]:
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith("#"):
                        continue
                    if "=" in ln:
                        key = ln.split("=", 1)[0].strip().strip("export ")
                        if key and not key.startswith("-"):
                            result[key] = str(path)
        except Exception:
            pass
    return result


def find_tool_env_keys() -> dict[str, list[str]]:
    tool_env: dict[str, list[str]] = defaultdict(list)
    base = Path("/Users/andy/openapi-servers/servers")
    if not base.exists():
        return dict(tool_env)
    for srv_dir in base.iterdir():
        if not srv_dir.is_dir():
            continue
        name = srv_dir.name
        for py in srv_dir.rglob("*.py"):
            try:
                txt = py.read_text(errors="replace")
                keys = set(re.findall(r'(?:os\.getenv|os\.environ\.get)\s*\(\s*["\']([A-Z0-9_]+)', txt))
                if keys:
                    tool_env[name].extend(sorted(keys))
            except Exception:
                pass
    return {k: sorted(set(v)) for k, v in tool_env.items()}


LOSF_LINE_RE = re.compile(
    r"^(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*?)\s+\((\S+)\)"
)


def parse_addr(name: str) -> dict[str, Any] | None:
    if not name:
        return None
    # split on last colon for host:port
    m = re.match(r"^(.*):(\d+)$", name)
    if not m:
        return {"ip": name, "port": None}
    ip, port = m.group(1), int(m.group(2))
    return {"ip": ip, "port": port}


def get_all_connections() -> list[dict[str, Any]]:
    """Use lsof on macOS because psutil.net_connections needs elevated TCC."""
    conns = []
    code, out, err = _run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN,ESTABLISHED,CLOSE_WAIT"], timeout=30)
    if code != 0:
        return [{"error": err or "lsof failed"}]
    seen = set()
    for ln in out.splitlines():
        m = LOSF_LINE_RE.match(ln)
        if not m:
            continue
        command, pid, user, fd, family, device, size_off, node, name, state = m.groups()
        local_name = name
        remote_name = None
        if "->" in name and state == "ESTABLISHED":
            local_name, remote_name = name.split("->", 1)

        local = parse_addr(local_name)
        remote = parse_addr(remote_name) if remote_name else None
        key = (pid, fd, local_name, remote_name, state)
        if key in seen:
            continue
        seen.add(key)
        conns.append({
            "pid": int(pid),
            "command": command,
            "user": user,
            "fd": fd,
            "family": family,
            "type": node,  # TCP/UDP
            "local_addr": local,
            "remote_addr": remote,
            "status": state,
        })
    return conns


class RuntimeInspector:
    def __init__(self) -> None:
        self.qualifier_pid = os.getpid()
        self.registry: dict[str, Any] = load_json(REGISTRY) or {"nodes": []}
        self.apo: dict[str, Any] = load_apo_config()
        self.cred_keys: dict[str, str] = get_cred_key_names()
        self.tool_env: dict[str, list[str]] = find_tool_env_keys()
        self.conns: list[dict[str, Any]] = get_all_connections()
        self.pid_to_conns: dict[int, list[dict[str, Any]]] = defaultdict(list)
        self.port_to_pids: dict[int, list[int]] = defaultdict(list)
        for c in self.conns:
            pid = c.get("pid")
            if pid:
                self.pid_to_conns[pid].append(c)
                if c["local_addr"]:
                    port = c["local_addr"].get("port")
                    if port:
                        self.port_to_pids[port].append(pid)
        self.target_ports: set[int] = set()
        for n in self.registry.get("nodes", []):
            d = n.get("defaults", {})
            if d.get("port"):
                self.target_ports.add(int(d["port"]))
            if d.get("daemon_port"):
                self.target_ports.add(int(d["daemon_port"]))
        # extras for stale product and system gatekeepers
        self.target_ports |= {5000, 4173, 7000}
        # map launchd labels once
        self.launchd_map: dict[int, str] = {}
        code, out, _ = _run(["launchctl", "list"])
        if code == 0:
            for ln in out.splitlines():
                parts = ln.split()
                if len(parts) >= 3 and parts[0].isdigit():
                    self.launchd_map[int(parts[0])] = parts[2]
        # HyperAI-Sync runtime dirs
        self.aios_roots = [
            str(HYPER),
            str(HOME / ".codex"),
            str(HOME / ".agents"),
            str(HOME / ".apo"),
            str(HOME / ".config"),
            str(HOME / "openapi-servers"),
            str(HOME / "workbench"),
            "/Applications/Bionic.app",
            "/Applications/Codex.app",
            "/Applications/LM Studio.app",
            str(HOME / ".ollama"),
            "/Library/PrivilegedHelperTools/com.docker.vmnetd",
            "/var/run/docker.sock",
            "/opt/homebrew",
        ]

    # ------------------------------------------------------------------
    # 1. DISCOVERY
    # ------------------------------------------------------------------
    def is_relevant_process(self, p: psutil.Process) -> tuple[bool, list[str]]:
        """Direct relevance: keyword match or listening on an AIOS target port.

        Plain 'user=andy' is not enough — the house must be identifiable.
        """
        reasons: list[str] = []
        try:
            info = p.as_dict(attrs=["pid", "ppid", "name", "exe", "cmdline", "cwd", "username", "create_time"])
        except Exception:
            return False, []
        name = (info.get("name") or "").lower()
        exe = (info.get("exe") or "").lower()
        cmd = " ".join(info.get("cmdline") or []).lower()
        cwd = (info.get("cwd") or "").lower()

        keywords = [
            "aios", "hyperai", "apo", "codex", "ollama", "lmstudio", "lm-studio", "bionic",
            "pieces", "finalai", "runtime", "federation", "orchestrator", "openapi",
            "mcp", "credential", "gateway", "agent_os", "memory_writer", "update_memory",
            "ngrok", "com.docker",
        ]
        for kw in keywords:
            if kw in name or kw in exe or kw in cmd or kw in cwd:
                reasons.append(f"keyword:{kw}")

        for c in self.pid_to_conns.get(p.pid, []):
            if c["status"] == "LISTEN":
                port = c["local_addr"].get("port") if c["local_addr"] else None
                if port and int(port) in self.target_ports:
                    reasons.append(f"aios_port:{port}")

        # include system processes that hold aios ports
        if any(r.startswith("aios_port:") for r in reasons):
            reasons.append("port_holder")

        return len(reasons) > 0, list(set(reasons))

    def safe_as_dict(self, p: psutil.Process) -> dict[str, Any]:
        attrs = ["pid", "ppid", "name", "exe", "cmdline", "cwd", "username",
                 "create_time", "memory_info", "num_threads", "status"]
        try:
            info = p.as_dict(attrs=attrs)
        except Exception as exc:
            return {"pid": p.pid, "error": str(exc)}
        # create_time iso
        if info.get("create_time"):
            info["create_time"] = datetime.fromtimestamp(info["create_time"], tz=timezone.utc).isoformat()
        # memory
        if info.get("memory_info"):
            info["memory"] = {"rss": info["memory_info"].rss, "vms": info["memory_info"].vms}
            del info["memory_info"]
        # mask any secret values in cmdline
        if isinstance(info.get("cmdline"), list):
            info["cmdline"] = [mask_secret_in(str(arg)) for arg in info["cmdline"]]
        # open files filtered
        try:
            of = p.open_files()
            info["open_files"] = [{"path": f.path, "fd": f.fd} for f in of if self.is_relevant_path(f.path)]
        except Exception:
            info["open_files"] = []
        # env filtered + masked
        try:
            raw_env = p.environ()
            info["env"] = [
                {"key": k, "value": mask_env(k, v)}
                for k, v in raw_env.items()
                if relevant_env_key(k) or SENSITIVE_KEY_RE.search(k)
            ]
        except Exception:
            info["env"] = []
        # connections (already collected globally)
        info["connections"] = self.pid_to_conns.get(p.pid, [])
        info["listening"] = [c for c in info["connections"] if c.get("status") == "LISTEN"]
        listening_ports = [c["local_addr"]["port"] for c in info["listening"] if c.get("local_addr")]
        info["listening_ports"] = listening_ports
        info["file_roots"] = self.file_roots(info.get("open_files", []))
        info["launchd_label"] = self.launchd_map.get(p.pid)
        return info

    def is_relevant_path(self, path: str) -> bool:
        return bool(RELEVANT_OPEN_RE.search(path) or any(path.startswith(r) for r in self.aios_roots))

    def file_roots(self, open_files: list[dict[str, Any]]) -> list[str]:
        roots = set()
        for f in open_files:
            p = f.get("path", "")
            for root in self.aios_roots:
                if p.startswith(root):
                    roots.add(root)
        return sorted(roots)

    def discover_snapshot(self) -> dict[str, Any]:
        # First pass: keyword or aios-port listeners. Skip qualifier's own process.
        direct: dict[int, tuple[psutil.Process, list[str]]] = {}
        for p in psutil.process_iter():
            if p.pid == self.qualifier_pid:
                continue
            rel, reasons = self.is_relevant_process(p)
            if rel:
                direct[p.pid] = (p, reasons)

        relevant_pids = set(direct.keys())
        relevant_listening_ports: set[int] = set()
        for p, _ in direct.values():
            for c in self.pid_to_conns.get(p.pid, []):
                if c["status"] == "LISTEN" and c.get("local_addr"):
                    relevant_listening_ports.add(int(c["local_addr"]["port"]))

        # Second pass: include parents, children, connectors, and processes touching AIOS files.
        related: dict[int, tuple[psutil.Process, list[str]]] = {}
        for p in psutil.process_iter():
            if p.pid == self.qualifier_pid or p.pid in direct:
                continue
            try:
                info = p.as_dict(attrs=["pid", "ppid", "name", "cmdline", "exe", "cwd"])
            except Exception:
                continue

            reasons: list[str] = []

            # parent or child in relevant set
            ppid = info.get("ppid")
            if ppid and ppid in relevant_pids:
                reasons.append("related:parent")
            try:
                if any(child.pid in relevant_pids for child in p.children()):
                    reasons.append("related:child")
            except Exception:
                pass

            # connects to a relevant AIOS listening port
            for c in self.pid_to_conns.get(p.pid, []):
                if c.get("status") == "ESTABLISHED" and c.get("remote_addr"):
                    rport = int(c["remote_addr"].get("port", 0))
                    if rport in relevant_listening_ports:
                        reasons.append(f"related:connects_to_port:{rport}")

            # touches AIOS file roots
            try:
                for f in p.open_files():
                    if self.is_relevant_path(f.path):
                        reasons.append("related:aios_file")
                        break
            except Exception:
                pass

            if reasons:
                related[p.pid] = (p, list(set(reasons)))

        all_pids = {**direct, **related}

        processes = []
        for p, reasons in all_pids.values():
            info = self.safe_as_dict(p)
            info["relevance_reasons"] = reasons
            processes.append(info)

        port_index = defaultdict(list)
        for pr in processes:
            for port in pr.get("listening_ports", []):
                port_index[port].append(pr["pid"])

        return {
            "audited_at": now_iso(),
            "total_observed": len(processes),
            "total_connections": len(self.conns),
            "processes": processes,
            "port_index": {str(k): v for k, v in port_index.items()},
        }

    # ------------------------------------------------------------------
    # 2. MATCH REGISTRY
    # ------------------------------------------------------------------
    def node_fingerprint(self, node: dict[str, Any]) -> list[str]:
        """Return keywords that identify a process as this node."""
        node_id = node["id"]
        surfaces = node.get("surfaces", {})
        fingers = [node_id.lower()]

        # split node id, keep tokens >= 3 chars that are not generic
        generic = {
            "agent", "andy", "aios", "apo", "app", "auth", "build", "codex", "config", "control",
            "credentials", "dashboard", "docker", "federation", "gateway", "google", "hyperai", "labs",
            "macbook", "macmini", "mission", "mcp", "mcp_server", "memory", "openai", "openapi",
            "orchestrator", "product", "runtime", "server", "slack", "system", "titan", "time", "tool", "ui",
            "user",
        }
        all_tokens = [t for t in re.split(r"[_\-]", node_id.lower()) if len(t) >= 2]
        for token in all_tokens:
            if len(token) >= 3 and token not in generic:
                fingers.append(token)
        # also add 2-grams so compound names like agent_os are preserved even when the
        # individual tokens are generic
        for i in range(len(all_tokens) - 1):
            bigram = f"{all_tokens[i]}_{all_tokens[i+1]}"
            if all_tokens[i] not in generic and all_tokens[i+1] not in generic:
                fingers.append(bigram)
            if all_tokens[i] not in generic or all_tokens[i+1] not in generic:
                fingers.append(bigram)
                fingers.append(bigram.replace("_", "-"))

        # named surface / container (do not split short/generic tokens)
        for key in ("name", "container_name"):
            v = surfaces.get(key)
            if v and len(str(v)) >= 3:
                full = str(v).lower()
                if full not in generic:
                    fingers.append(full)
                for token in re.split(r"[_\-]", full):
                    if len(token) >= 3 and token not in generic:
                        fingers.append(token)

        # owner (skip generic/supervisory owners that match too many processes)
        owner = node.get("owner")
        skip_owners = {"apo_gateway", "aios"}
        if owner and len(str(owner)) >= 3 and str(owner).lower() not in skip_owners:
            full = str(owner).lower()
            if full not in generic:
                fingers.append(full)
            for token in re.split(r"[_\-]", full):
                if len(token) >= 3 and token not in generic:
                    fingers.append(token)

        # artifact / script / backend file / bundle / config
        for path_key in ("cli_path", "script", "mcp_server_path", "backend_file",
                         "registry_path", "ooda_contract", "app_bundle", "codex_config",
                         "mcp_config", "state", "journal", "socket_path"):
            path = surfaces.get(path_key)
            if not path:
                continue
            base = Path(path).stem.lower()
            if len(base) >= 3 and base not in generic:
                fingers.append(base)
            fingers.append(path.lower())
            # for config files, also include the parent directory so a process running
            # inside that directory is matched without a full file-name overlap
            if path_key in ("codex_config", "mcp_config"):
                parent = Path(path).parent.as_posix().lower().rstrip("/")
                if parent and parent not in ("/", "/users/andy"):
                    fingers.append(parent)

        # for openapi tools, add the service dir
        if node_id.startswith("openapi_tool_"):
            tool = node_id.replace("openapi_tool_", "")
            for sep in ("_", "-"):
                fingers.append(f"/servers/{tool.replace('_', sep)}")

        return list(set(fingers))

    def match_registry(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        pid_to_proc = {p["pid"]: p for p in snapshot["processes"]}
        port_index = {int(k): v for k, v in snapshot.get("port_index", {}).items()}

        matched: dict[str, Any] = {}
        for node in self.registry.get("nodes", []):
            node_id = node["id"]
            if node.get("state") == "STANDBY_UNREACHABLE":
                matched[node_id] = {"pids": [], "processes": []}
                continue
            d = node.get("defaults", {})
            port = d.get("port") or d.get("daemon_port")
            surfaces = node.get("surfaces", {})
            fingers = self.node_fingerprint(node)

            pids = set()

            def proc_blob(pr: dict[str, Any]) -> str:
                return " ".join([
                    pr.get("name") or "",
                    " ".join(pr.get("cmdline") or []),
                    pr.get("exe") or "",
                    pr.get("cwd") or "",
                ]).lower()

            def matches_finger(blob: str) -> bool:
                for f in fingers:
                    if "/" in f:
                        # path segment: next char must be /, space, or end
                        if re.search(re.escape(f) + r"(?=/|$|\s)", blob):
                            return True
                    else:
                        # token may be the first part of a snake/kebab compound name
                        if re.search(r"(?<![A-Za-z0-9])" + re.escape(f) + r"(?![A-Za-z0-9])", blob):
                            return True
                return False

            # by port + identity check
            if port and int(port) in port_index:
                for pid in port_index[int(port)]:
                    pr = pid_to_proc.get(pid)
                    if pr and matches_finger(proc_blob(pr)):
                        pids.add(pid)

            # by identity / path
            for pr in snapshot["processes"]:
                blob = proc_blob(pr)
                if matches_finger(blob):
                    pids.add(pr["pid"])
                    continue
                for path_key in ("cli_path", "script", "mcp_server_path", "backend_file",
                                 "registry_path", "ooda_contract", "app_bundle", "codex_config",
                                 "mcp_config", "state", "journal", "socket_path"):
                    path = surfaces.get(path_key)
                    if not path:
                        continue
                    if path in " ".join(pr.get("cmdline") or []):
                        pids.add(pr["pid"])
                    if path_key in ("codex_config", "mcp_config"):
                        parent = Path(path).parent.as_posix().lower().rstrip("/")
                        if parent and re.search(re.escape(parent) + r"(?=/|$|\s)", proc_blob(pr)):
                            pids.add(pr["pid"])

            matched[node_id] = {
                "pids": sorted(pids),
                "processes": [pid_to_proc[pid] for pid in sorted(pids) if pid in pid_to_proc],
            }
        return matched

    # ------------------------------------------------------------------
    # 3. ROLE REGISTRY
    # ------------------------------------------------------------------
    def role_from_role_str(self, role: str) -> str:
        r = (role or "").lower()
        if "root" in r:
            return "ROOT"
        if "inference" in r or "provider" in r or "model" in r:
            return "PROVIDER"
        if "gateway" in r:
            return "GATEWAY"
        if "broker" in r:
            return "BROKER"
        if "tool" in r:
            return "TOOL"
        if "mcp" in r:
            return "MCP"
        if "worker" in r or "desktop" in r or "operator" in r:
            return "WORKER"
        if "memory" in r or "cache" in r:
            return "MEMORY"
        if "product" in r or "app" in r:
            return "PRODUCT"
        if "orchestrator" in r:
            return "ORCHESTRATOR"
        if "registry" in r:
            return "ORCHESTRATOR"
        if "verifier" in r:
            return "VERIFIER"
        if "dashboard" in r or "cockpit" in r:
            return "WORKER"
        if "infra" in r or "fabric" in r:
            return "INFRA"
        return "UNKNOWN"

    def role_from_kind(self, kind: str, surfaces: dict[str, Any], gates: dict[str, Any] | None = None) -> str:
        k = (kind or "").lower()
        if "root" in k:
            return "ROOT"
        if "gateway" in k:
            return "GATEWAY"
        if k == "http_service":
            return self.role_from_http_service(surfaces, gates or {})
        if "broker" in k:
            return "BROKER"
        if "provider" in k or "model" in k or "inference" in k:
            return "PROVIDER"
        if "mcp" in k:
            return "MCP"
        if "tool" in k:
            return "TOOL"
        if "worker" in k or "operator" in k or "desktop" in k:
            return "WORKER"
        if "memory" in k or "cache" in k:
            return "MEMORY"
        if "product" in k or k == "app_runtime":
            return "PRODUCT"
        if k == "service_runtime":
            return self.role_from_service(surfaces)
        if "infra" in k or "fabric" in k or "container" in k:
            return "INFRA"
        if "orchestrator" in k or "registry" in k:
            return "ORCHESTRATOR"
        if "verifier" in k:
            return "VERIFIER"
        return "UNKNOWN"

    def role_from_service(self, surfaces: dict[str, Any]) -> str:
        script = (surfaces.get("script") or surfaces.get("cli_path") or "").lower()
        if "aios_mission_router" in script:
            return "ROOT"
        if "update_memory" in script or "memory" in script:
            return "MEMORY"
        if "federation" in script or "autonomous" in script:
            return "ORCHESTRATOR"
        if "credential" in script:
            return "BROKER"
        return "WORKER"

    def role_from_http_service(self, surfaces: dict[str, Any], gates: dict[str, Any]) -> str:
        if "proxy_path" in surfaces or "secret_lease_required" in gates:
            return "BROKER"
        if "tools_path" in surfaces or "models_path" in surfaces:
            return "GATEWAY"
        if "base_url" in surfaces:
            return "WORKER"
        return "UNKNOWN"

    def role_from_process(self, proc: dict[str, Any], node: dict[str, Any]) -> str:
        role = self.role_from_role_str(node.get("role", ""))
        if role != "UNKNOWN":
            return role
        cmd = " ".join(proc.get("cmdline") or []).lower()
        name = (proc.get("name") or "").lower()
        if "aios_mission_router" in cmd or node.get("id") == "aios_mission_router":
            return "ROOT"
        if "apo_gateway" in cmd or "apo_gateway" in name:
            return "GATEWAY"
        if "credential" in cmd or "hyperai_credentials" in name:
            return "BROKER"
        if node.get("kind") == "openapi_tool_server" or any(srv in cmd for srv in ["/servers/", "openapi"]):
            return "TOOL"
        if "ollama" in name:
            return "PROVIDER"
        if "lmstudio" in cmd or "lm-studio" in name or "LM Studio" in cmd:
            return "PROVIDER"
        if "bionic" in name:
            return "WORKER"
        if "pieces" in name:
            return "MCP"
        if "finalai" in cmd or "finalai" in name:
            return "PROVIDER"
        if "redis" in name:
            return "MEMORY"
        if "docker" in name and "com.docker" in name:
            return "INFRA"
        if "ngrok" in name:
            return "TUNNEL"
        return self.role_from_kind(node.get("kind", ""), node.get("surfaces", {}), node.get("gates", {}))

    def build_role_registry(self, snapshot: dict[str, Any], match: dict[str, Any]) -> dict[str, Any]:
        roles = []
        for node in self.registry.get("nodes", []):
            node_id = node["id"]
            procs = match.get(node_id, {}).get("processes", [])
            observed = len(procs) > 0
            if observed:
                role = self.role_from_process(procs[0], node)
            else:
                role = self.role_from_role_str(node.get("role", ""))
                if role == "UNKNOWN":
                    role = self.role_from_kind(node.get("kind", ""), node.get("surfaces", {}), node.get("gates", {}))

            roles.append({
                "id": node_id,
                "declared_kind": node.get("kind"),
                "assigned_role": role,
                "owner": node.get("owner"),
                "observed_runtime": observed,
                "pids": match.get(node_id, {}).get("pids", []),
                "role_resolved": observed and role != "UNKNOWN",
                "entrypoint": node.get("surfaces", {}).get("base_url") or node.get("surfaces", {}).get("cli_path"),
                "compute_request": node.get("defaults", {}),
                "notes": [] if observed else ["declared but not observed"],
            })

        # also add discovered but unregistered processes
        matched_pids = set()
        for v in match.values():
            matched_pids.update(v.get("pids", []))
        for proc in snapshot["processes"]:
            if proc["pid"] not in matched_pids:
                roles.append({
                    "id": f"discovered_pid_{proc['pid']}",
                    "declared_kind": None,
                    "assigned_role": "UNKNOWN",
                    "owner": proc.get("username"),
                    "observed_runtime": True,
                    "pids": [proc["pid"]],
                    "role_resolved": False,
                    "entrypoint": proc.get("exe"),
                    "compute_request": {},
                    "notes": ["discovered runtime not in registry; needs identification"],
                    "process": proc,
                })
        return {
            "audited_at": now_iso(),
            "roles": roles,
        }

    # ------------------------------------------------------------------
    # 4. AUTHORITY MATRIX
    # ------------------------------------------------------------------
    def authority_for_role(self, role: str) -> list[str]:
        base = ["OBSERVE"]
        if role == "ROOT":
            return ["OBSERVE", "PLAN", "ROUTE", "VERIFY", "AUTH", "ALLOCATE", "REVOKE"]
        if role == "ORCHESTRATOR":
            return ["OBSERVE", "PLAN", "ROUTE", "VERIFY"]
        if role == "GATEWAY":
            return ["OBSERVE", "ROUTE"]
        if role == "BROKER":
            return ["OBSERVE", "AUTH", "VERIFY"]
        if role == "PROVIDER":
            return ["OBSERVE", "INVOKE", "READ"]
        if role == "TOOL":
            return ["OBSERVE", "INVOKE", "READ"]
        if role == "MCP":
            return ["OBSERVE", "INVOKE", "READ"]
        if role == "WORKER":
            return ["OBSERVE", "READ", "WRITE"]
        if role == "MEMORY":
            return ["OBSERVE", "READ", "WRITE"]
        if role == "PRODUCT":
            return ["OBSERVE", "READ", "WRITE", "EXECUTE"]
        if role == "INFRA":
            return ["OBSERVE", "ALLOCATE", "EXECUTE"]
        if role == "VERIFIER":
            return ["OBSERVE", "VERIFY"]
        return ["OBSERVE"]

    def build_authority_matrix(self, role_registry: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
        pid_to_proc = {p["pid"]: p for p in snapshot["processes"]}
        entries = []
        for r in role_registry["roles"]:
            node_id = r["id"]
            proc = None
            if r.get("pids"):
                proc = pid_to_proc.get(r["pids"][0])
            if not proc and r.get("process"):
                proc = r["process"]

            auth = self.authority_for_role(r["assigned_role"])
            read_scope = []
            write_scope = []
            execute_scope = []
            network_scope = []

            if proc:
                roots = proc.get("file_roots", [])
                read_scope = roots
                # Write scope: any path that looks like data/cache/state under andy's home
                write_candidates = [
                    p["path"] for p in proc.get("open_files", [])
                    if any(s in p["path"] for s in ["/tmp", "/cache", "/state", "/data", "/logs", "/memory", "/db", "/.ollama", "/.codex"])
                ]
                write_scope = sorted(set(write_candidates))[:10]
                execute_scope = [proc.get("exe"), proc.get("cwd")]
                network_scope = [
                    f"{c['local_addr']['ip']}:{c['local_addr']['port']}" if c.get("local_addr") else "?"
                    for c in proc.get("connections", [])
                ]

            authority_resolved = bool(proc) and r["assigned_role"] != "UNKNOWN"
            entries.append({
                "id": node_id,
                "role": r["assigned_role"],
                "authority": auth,
                "read_scope": read_scope,
                "write_scope": write_scope,
                "execute_scope": [e for e in execute_scope if e],
                "network_scope": list(set(network_scope)),
                "authority_resolved": authority_resolved,
                "notes": ["needs explicit write-authority grant before mutation"] if not authority_resolved else [],
            })
        return {
            "audited_at": now_iso(),
            "entries": entries,
        }

    # ------------------------------------------------------------------
    # 5. AUTH TOPOLOGY
    # ------------------------------------------------------------------
    def auth_status_for_key(self, key: str) -> tuple[str, str]:
        if key in self.cred_keys:
            return "PRESENT", self.cred_keys[key]
        if key in os.environ:
            return "PRESENT", "process_environment"
        # macOS keychain generic hint
        if key in ("SLACK_BOT_TOKEN", "GOOGLE_API_KEY", "GOOGLE_PSE_CX"):
            return "MISSING", "expected in credentials.env or keychain"
        return "MISSING", "not found in known credential sources"

    def build_auth_topology(self, role_registry: dict[str, Any]) -> dict[str, Any]:
        topo = []

        # APΩ / providers
        provider_scopes = {
            "openai": ("OPENAI_API_KEY", "api.openai.com"),
            "anthropic": ("ANTHROPIC_API_KEY", "anthropic.com"),
            "openrouter": ("OPENROUTER_API_KEY", "openrouter.ai"),
            "google": ("GEMINI_API_KEY", "googleapis.com"),
            "github_models": ("GITHUB_MODELS_TOKEN", "models.inference.ai.azure.com"),
            "microsoftfoundry": ("AZURE_OPENAI_API_KEY", "services.ai.azure.com"),
            "lmstudio": ("LMSTUDIO_API_KEY", "127.0.0.1:1235"),
        }
        for pname, (key, domain) in provider_scopes.items():
            status, source = self.auth_status_for_key(key)
            topo.append({
                "surface": f"apo_upstream_{pname}",
                "provider": pname,
                "domain": domain,
                "required_key": key,
                "status": status,
                "source": source,
                "scope": "model inference",
                "expiry": "UNKNOWN",
                "refresh_path": f"credential_broker / {key}",
                "consent_boundary": "external paid API",
            })

        # Tool servers
        tool_map = {
            "slack": (["SLACK_BOT_TOKEN", "SLACK_TEAM_ID"], "Slack workspace"),
            "google_pse": (["GOOGLE_API_KEY", "GOOGLE_PSE_CX"], "Google Programmable Search"),
            "sql": (["DATABASE_URL", "OPENAI_API_KEY"], "SQL database + OpenAI"),
            "external_rag": ([], "local FAISS only"),
        }
        for tname, (keys, desc) in tool_map.items():
            for key in keys:
                status, source = self.auth_status_for_key(key)
                topo.append({
                    "surface": f"openapi_tool_{tname}",
                    "provider": desc,
                    "domain": "127.0.0.1",
                    "required_key": key,
                    "status": status,
                    "source": source,
                    "scope": f"tool:{tname}",
                    "expiry": "UNKNOWN",
                    "refresh_path": f"credential_broker / {key}",
                    "consent_boundary": "external account" if tname in ("slack", "google_pse") else "local database",
                })

        # Pieces token-in-path
        topo.append({
            "surface": "mcp_pieces",
            "provider": "Pieces",
            "domain": "127.0.0.1:39300",
            "required_key": "token (path parameter)",
            "status": "PRESENT_UNKNOWN",
            "source": "SSE URL token param",
            "scope": "mcp bridge",
            "expiry": "UNKNOWN",
            "refresh_path": "Pieces app re-authentication",
            "consent_boundary": "Pieces account",
        })

        # Bionic / LM Studio app-side
        topo.append({
            "surface": "lmstudio_bionic_api",
            "provider": "LM Studio",
            "domain": "127.0.0.1:1235",
            "required_key": "LMSTUDIO_API_KEY",
            "status": self.auth_status_for_key("LMSTUDIO_API_KEY")[0],
            "source": self.auth_status_for_key("LMSTUDIO_API_KEY")[1],
            "scope": "local inference",
            "expiry": "UNKNOWN",
            "refresh_path": "LM Studio app settings",
            "consent_boundary": "local app",
        })

        # Summary
        status_counts = defaultdict(int)
        for t in topo:
            status_counts[t["status"]] += 1
        return {
            "audited_at": now_iso(),
            "total_auth_records": len(topo),
            "status_counts": dict(status_counts),
            "records": topo,
        }

    # ------------------------------------------------------------------
    # 6. DEPENDENCY GRAPH
    # ------------------------------------------------------------------
    def build_dependency_graph(self, snapshot: dict[str, Any], match: dict[str, Any],
                               role_registry: dict[str, Any], auth: dict[str, Any]) -> dict[str, Any]:
        nodes = {}
        pid_to_proc = {p["pid"]: p for p in snapshot["processes"]}

        # registry nodes
        for node in self.registry.get("nodes", []):
            node_id = node["id"]
            pids = match.get(node_id, {}).get("pids", [])
            nodes[node_id] = {
                "id": node_id,
                "type": "registry_surface",
                "pids": pids,
            }

        # discovered unregistered
        matched_pids = {pid for v in match.values() for pid in v.get("pids", [])}
        for proc in snapshot["processes"]:
            if proc["pid"] not in matched_pids:
                nodes[f"pid_{proc['pid']}"] = {
                    "id": f"pid_{proc['pid']}",
                    "type": "discovered_process",
                    "pids": [proc["pid"]],
                }

        edges = []
        for proc in snapshot["processes"]:
            pid = proc["pid"]
            # parent
            if proc.get("ppid"):
                edges.append({
                    "source": f"pid_{proc['ppid']}",
                    "target": f"pid_{pid}",
                    "type": "PARENT_OF",
                })
            # launchd
            if proc.get("launchd_label"):
                edges.append({
                    "source": proc["launchd_label"],
                    "target": f"pid_{pid}",
                    "type": "CONTROL",
                })
            # network
            for c in proc.get("connections", []):
                if c.get("status") == "ESTABLISHED" and c.get("remote_addr"):
                    rip = c["remote_addr"].get("ip")
                    rport = c["remote_addr"].get("port")
                    # find which other process listens on that remote port
                    if rip in ("127.0.0.1", "::1", "localhost") and rport:
                        for other in snapshot["processes"]:
                            if other["pid"] == pid:
                                continue
                            if rport in other.get("listening_ports", []):
                                edges.append({
                                    "source": f"pid_{pid}",
                                    "target": f"pid_{other['pid']}",
                                    "type": "CONNECTS_TO",
                                    "port": rport,
                                })
            # file roots
            for root in proc.get("file_roots", []):
                edges.append({
                    "source": f"pid_{pid}",
                    "target": root,
                    "type": "DEPENDS_FILE",
                })

        # gateway routes from apo_config
        for tname, cfg in (self.apo.get("tools") or {}).items():
            url = cfg.get("base_url", "")
            try:
                port = int(url.split(":")[-1].split("/")[0])
            except Exception:
                port = None
            if port:
                edges.append({
                    "source": "apo_gateway",
                    "target": f"openapi_tool_{tname}",
                    "type": "ROUTE",
                    "port": port,
                })

        return {
            "audited_at": now_iso(),
            "nodes": list(nodes.values()),
            "edges": edges,
        }

    # ------------------------------------------------------------------
    # 7. BINDING PLAN
    # ------------------------------------------------------------------
    def build_binding_plan(self, role_registry: dict[str, Any], authority: dict[str, Any],
                           auth: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
        pid_to_proc = {p["pid"]: p for p in snapshot["processes"]}
        auth_by_surface = {a["surface"]: a for a in auth.get("records", [])}

        plans = []
        for r in role_registry["roles"]:
            node_id = r["id"]
            if node_id.startswith("discovered_pid_"):
                continue
            proc = None
            if r.get("pids"):
                proc = pid_to_proc.get(r["pids"][0])

            missing = []
            if not r["observed_runtime"]:
                missing.append("observed_runtime")
            if not r["role_resolved"]:
                missing.append("role_resolved")

            auth_records = [a for a in auth.get("records", []) if a["surface"] == node_id]
            auth_resolved = all(a["status"].startswith("PRESENT") or a["required_key"] == "token (path parameter)" for a in auth_records) if auth_records else True
            if not auth_resolved:
                missing.extend([f"auth:{a['required_key']}" for a in auth_records if a["status"] == "MISSING"])

            # authority check
            auth_entry = next((a for a in authority.get("entries", []) if a["id"] == node_id), None)
            authority_resolved = auth_entry.get("authority_resolved") if auth_entry else False
            if not authority_resolved:
                missing.append("authority_resolved")

            # dependencies: at least the process has parent or launchd
            dependencies_resolved = bool(proc and (proc.get("ppid") or proc.get("launchd_label")))
            if not dependencies_resolved:
                missing.append("dependencies_resolved")

            health_probed = bool(proc)
            if not health_probed:
                missing.append("health_probed")

            lifecycle_known = r["assigned_role"] not in ("UNKNOWN",)
            if not lifecycle_known:
                missing.append("lifecycle_known")

            operationally_qualified = (
                r["observed_runtime"]
                and r["role_resolved"]
                and authority_resolved
                and auth_resolved
                and dependencies_resolved
                and health_probed
                and lifecycle_known
            )

            compute_claim = "none"
            if not r["observed_runtime"]:
                compute_claim = "manual_or_recycle"
            elif r["assigned_role"] in ("ROOT", "GATEWAY", "BROKER", "TOOL", "MCP", "PROVIDER"):
                compute_claim = "launchd_or_daemon" if proc.get("launchd_label") else "process_group"

            plans.append({
                "id": node_id,
                "role": r["assigned_role"],
                "observed_runtime": r["observed_runtime"],
                "role_resolved": r["role_resolved"],
                "authority_resolved": authority_resolved,
                "auth_resolved": auth_resolved,
                "dependencies_resolved": dependencies_resolved,
                "health_probed": health_probed,
                "lifecycle_known": lifecycle_known,
                "operationally_qualified": operationally_qualified,
                "missing": missing,
                "compute_claim": compute_claim,
                "proposed_binding": f"bind when {','.join(missing)} resolved" if missing else "ready for gate approval",
                "pids": r.get("pids", []),
            })

        qualified = sum(1 for p in plans if p["operationally_qualified"])
        return {
            "audited_at": now_iso(),
            "total": len(plans),
            "qualified": qualified,
            "plans": plans,
        }

    # ------------------------------------------------------------------
    # 8. REPORT
    # ------------------------------------------------------------------
    def build_report(self, snapshot: dict[str, Any], roles: dict[str, Any],
                     authority: dict[str, Any], auth: dict[str, Any],
                     dep: dict[str, Any], plan: dict[str, Any]) -> str:
        lines = [
            "# Operational Qualification Report",
            "",
            f"audited_at: {now_iso()}",
            "",
            "## 1. Runtime discovery",
            "",
            f"Observed AIOS-relevant processes: **{snapshot['total_observed']}**",
            f"Total network connections observed: **{snapshot.get('total_connections', 0)}**",
            "",
            "### Observed by command (selected)",
            "",
            "| pid | command | listening_ports | role |",
            "|-----|---------|-----------------|------|",
        ]
        for proc in snapshot["processes"][:40]:
            cmd = " ".join(proc.get("cmdline") or [])[:60]
            ports = ",".join(str(p) for p in proc.get("listening_ports", []))[:30]
            role = "UNKNOWN"
            for r in roles["roles"]:
                if proc["pid"] in r.get("pids", []) and not r["id"].startswith("discovered_pid_"):
                    role = r["assigned_role"]
                    break
            lines.append(f"| {proc['pid']} | {cmd} | {ports} | {role} |")

        lines.extend([
            "",
            "## 2. Role registry",
            "",
            f"Total surfaces: **{len(roles['roles'])}**",
            f"Observed runtime: **{sum(1 for r in roles['roles'] if r['observed_runtime'])}**",
            f"Role resolved: **{sum(1 for r in roles['roles'] if r['role_resolved'])}**",
            "",
        ])

        lines.extend([
            "## 3. Authority matrix",
            "",
            f"Authority resolved: **{sum(1 for e in authority['entries'] if e['authority_resolved'])} / {len(authority['entries'])}**",
            "",
        ])

        lines.extend([
            "## 4. Auth topology",
            "",
        ])
        for st, cnt in auth.get("status_counts", {}).items():
            lines.append(f"- {st}: {cnt}")

        lines.extend([
            "",
            "## 5. Dependency graph",
            "",
            f"Nodes: **{len(dep['nodes'])}**, Edges: **{len(dep['edges'])}**",
            "",
        ])

        lines.extend([
            "## 6. Binding plan",
            "",
            f"Operationally qualified: **{plan['qualified']} / {plan['total']}**",
            "",
            "### Not qualified (selected)",
            "",
            "| id | role | missing | compute_claim |",
            "|-----|------|---------|---------------|",
        ])
        for p in plan["plans"]:
            if not p["operationally_qualified"] and not p["id"].startswith("discovered_pid_"):
                missing = ", ".join(p["missing"])[:60]
                lines.append(f"| {p['id']} | {p['role']} | {missing} | {p['compute_claim']} |")

        lines.extend([
            "",
            "## 7. Invariants preserved",
            "",
            "- READONLY_DISCOVERY = 1",
            "- UNBOUNDED_DISCOVERY = 0",
            "- AUTO_BINDING = 0",
            "- AUTO_EXECUTION = 0",
            "- AUTO_MUTATION = 0",
            "- No plaintext secrets logged",
            "- mcp_docker_mcp:8811 not started",
            "- Gate 2 not opened",
            "",
            "## 8. Gaps requiring explicit gate",
            "",
        ])
        for p in plan["plans"]:
            if not p["operationally_qualified"] and not p["id"].startswith("discovered_pid_"):
                lines.append(f"- **{p['id']}**: {p['missing']}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    def run(self) -> int:
        OUT.mkdir(parents=True, exist_ok=True)

        snapshot = self.discover_snapshot()
        with (OUT / "runtime_discovery_snapshot.json").open("w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        match = self.match_registry(snapshot)

        roles = self.build_role_registry(snapshot, match)
        with (OUT / "role_registry.json").open("w", encoding="utf-8") as f:
            json.dump(roles, f, indent=2, ensure_ascii=False)

        authority = self.build_authority_matrix(roles, snapshot)
        with (OUT / "authority_matrix.json").open("w", encoding="utf-8") as f:
            json.dump(authority, f, indent=2, ensure_ascii=False)

        auth = self.build_auth_topology(roles)
        with (OUT / "auth_topology.json").open("w", encoding="utf-8") as f:
            json.dump(auth, f, indent=2, ensure_ascii=False)

        dep = self.build_dependency_graph(snapshot, match, roles, auth)
        with (OUT / "dependency_graph.json").open("w", encoding="utf-8") as f:
            json.dump(dep, f, indent=2, ensure_ascii=False)

        plan = self.build_binding_plan(roles, authority, auth, snapshot)
        with (OUT / "binding_plan.json").open("w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)

        report = self.build_report(snapshot, roles, authority, auth, dep, plan)
        (OUT / "operational_qualification_report.md").write_text(report, encoding="utf-8")

        print(f"wrote to {OUT}")
        print(f"  processes observed: {snapshot['total_observed']}")
        print(f"  qualified: {plan['qualified']}/{plan['total']}")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIOS active-runtime qualification")
    parser.add_argument("--runtime-root", default=None, help="Absolute path to HyperAI-Sync root (default: source parent)")
    parser.add_argument("--registry", default=None, help="Absolute path to runtime_registry.json")
    parser.add_argument("--apo-config", default=None, help="Absolute path to apo_config.yaml")
    parser.add_argument("--creds-env", default=None, help="Absolute path to credentials.env")
    args = parser.parse_args()
    if args.runtime_root:
        os.environ["HYPERAI_RUNTIME_ROOT"] = args.runtime_root
        global HYPER, RUNTIME, OUT
        HYPER = Path(args.runtime_root)
        RUNTIME = HYPER / "runtime" / "federation_orchestrator"
        OUT = RUNTIME
    if args.registry:
        os.environ["HYPERAI_REGISTRY"] = args.registry
        global REGISTRY
        REGISTRY = Path(args.registry)
    if args.apo_config:
        os.environ["HYPERAI_APO_CONFIG"] = args.apo_config
        global APO_CONFIG
        APO_CONFIG = Path(args.apo_config)
    if args.creds_env:
        os.environ["HYPERAI_CREDS_ENV"] = args.creds_env
        global CREDS_ENV
        CREDS_ENV = Path(args.creds_env)
    raise SystemExit(RuntimeInspector().run())
