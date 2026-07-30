#!/usr/bin/env python3
# =============================================================================
# PROJECT: CANON-TO-SYSTEM DETERMINISTIC PROJECTION
# METHOD: D&R PROTOCOL (CLOSED)
#
# ORIGINATOR / CREATOR:
#   alpha_prime_omega
#
# LEGAL ONTOLOGY:
#   This source file is a deterministic projection of a closed Canon.
#   Removal or alteration of this header voids legal and ontological validity.
#
# STATUS:
#   GENERATED — NON-AUTONOMOUS — NON-OWNERLESS
#
# TRACEABILITY:
#   Canon -> COG -> Projection(Π) -> Artifact
#
# =============================================================================

"""Autonomous control loop for the governed HyperAI SyncLane."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "runtime" / "federation_orchestrator"
LINEAGE_DIR = ROOT / "runtime" / "lineage"
LOG_DIR = RUNTIME_DIR / "sync_lane_logs"
STATE_PATH = RUNTIME_DIR / "sync_lane_autonomy_state.json"
REGISTRY_PATH = RUNTIME_DIR / "sync_lane_registry.json"
WHITELIST_PATH = RUNTIME_DIR / "sync_lane_whitelist.json"
TITAN_INVENTORY = LINEAGE_DIR / "sync_lane_inventory_titan_20260421.json"
TITAN_LEDGER = LINEAGE_DIR / "sync_lane_dirty_ledger_titan_20260421.json"
MAC_INVENTORY = LINEAGE_DIR / "sync_lane_inventory_mac_20260421.json"
DEFAULT_MAC_HOST = "andy.local"
DEFAULT_IDENTITY = str(Path.home() / ".ssh" / "hyperai_titan_to_macbook_ed25519")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def run_command(command: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def read_known_hosts(mac_host: str) -> list[str]:
    known_hosts = Path.home() / ".ssh" / "known_hosts"
    if not known_hosts.exists():
        return []
    hits = []
    for line in known_hosts.read_text(encoding="utf-8", errors="ignore").splitlines():
        if mac_host in line:
            hits.append(line)
    return hits


def detect_ssh_client() -> str | None:
    return (
        shutil.which("ssh")
        or shutil.which("ssh.exe")
        or str(Path(r"C:\Program Files\Git\usr\bin\ssh.exe")) if Path(r"C:\Program Files\Git\usr\bin\ssh.exe").exists() else None
    )


def can_reach_mac_via_identity(mac_host: str, identity: str) -> bool:
    ssh_client = detect_ssh_client()
    if not ssh_client:
        return False
    identity_path = Path(identity)
    if not identity_path.exists():
        return False
    code, stdout, stderr = run_command(
        [
            ssh_client,
            "-i",
            str(identity_path),
            "-o",
            "IdentitiesOnly=yes",
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=8",
            f"andy@{mac_host}",
            "echo",
            "HYPERAI_MAC_OK",
        ]
    )
    return code == 0 and "HYPERAI_MAC_OK" in stdout


def bootstrap_titan() -> dict[str, Any]:
    command = [sys.executable, str(ROOT / "tools" / "bootstrap_sync_lane.py")]
    code, stdout, stderr = run_command(command)
    if code != 0:
        raise RuntimeError(stderr.strip() or stdout.strip())
    return json.loads(stdout)


def compare_inventories(titan: dict[str, Any], mac: dict[str, Any]) -> dict[str, Any]:
    titan_files = {item["relative_path"]: item["sha256"] for item in titan.get("files", [])}
    mac_files = {item["relative_path"]: item["sha256"] for item in mac.get("files", [])}
    titan_only = sorted(set(titan_files) - set(mac_files))
    mac_only = sorted(set(mac_files) - set(titan_files))
    changed = sorted(
        path for path in set(titan_files).intersection(mac_files) if titan_files[path] != mac_files[path]
    )
    if not titan_only and not mac_only and not changed:
        state = "same-head-like"
    else:
        state = "diverged"
    return {
        "state": state,
        "titan_file_count": titan.get("file_count"),
        "mac_file_count": mac.get("file_count"),
        "titan_only": titan_only[:25],
        "mac_only": mac_only[:25],
        "changed": changed[:25],
    }


def run_cycle(mac_host: str, identity: str) -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    whitelist = load_json(WHITELIST_PATH)
    cycle_id = f"sync-lane-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    observe = {
        "registry_exists": REGISTRY_PATH.exists(),
        "whitelist_exists": WHITELIST_PATH.exists(),
        "titan_inventory_exists": TITAN_INVENTORY.exists(),
        "titan_dirty_ledger_exists": TITAN_LEDGER.exists(),
        "mac_inventory_exists": MAC_INVENTORY.exists(),
        "ssh_client": detect_ssh_client(),
        "known_hosts_hits": read_known_hosts(mac_host),
        "identity_reachability": can_reach_mac_via_identity(mac_host, identity),
    }

    action = "hold"
    decision_reason = ""
    compare_summary: dict[str, Any] | None = None

    if not observe["titan_inventory_exists"] or not observe["titan_dirty_ledger_exists"]:
        bootstrap_result = bootstrap_titan()
        observe["titan_inventory_exists"] = TITAN_INVENTORY.exists()
        observe["titan_dirty_ledger_exists"] = TITAN_LEDGER.exists()
        action = "bootstrap_titan_sync_lane"
        decision_reason = "Titan proof artifacts were missing, so the lane was materialized first."
        act = bootstrap_result
    elif not observe["ssh_client"]:
        action = "wait_for_ssh_transport"
        decision_reason = "Peer lane bootstrap is blocked because no local ssh client is available on Titan."
        act = {
            "blocker": "ssh_client_missing",
            "required_for_next_step": f"reachable ssh client for {mac_host}",
        }
    elif not observe["identity_reachability"]:
        action = "wait_for_key_registration"
        decision_reason = "Titan has transport, but the governed identity key is not yet accepted for Mac peer bootstrap."
        act = {
            "blocker": "identity_key_not_accepted",
            "required_for_next_step": identity,
        }
    elif not observe["mac_inventory_exists"]:
        code, stdout, stderr = run_command(
            [
                sys.executable,
                str(ROOT / "tools" / "bootstrap_sync_lane_mac.py"),
                "--mac-host",
                mac_host,
                "--identity",
                identity,
            ]
        )
        if code != 0:
            action = "wait_for_mac_inventory"
            decision_reason = "Transport is reachable, but Mac peer bootstrap did not complete."
            act = {
                "blocker": "mac_bootstrap_failed",
                "detail": (stderr.strip() or stdout.strip())[:400],
            }
        else:
            observe["mac_inventory_exists"] = MAC_INVENTORY.exists()
            action = "bootstrap_mac_lane"
            decision_reason = "Transport and identity proof are live, so the runner bootstrapped the Mac peer lane."
            act = json.loads(stdout)
    else:
        titan_inventory = load_json(TITAN_INVENTORY)
        mac_inventory = load_json(MAC_INVENTORY)
        compare_summary = compare_inventories(titan_inventory, mac_inventory)
        action = "compare_only"
        decision_reason = "Both lane inventories exist, so autonomous flow can reconcile without mutation."
        act = compare_summary

    payload = {
        "schema_version": "2026-04-21.sync-lane-autonomous-cycle.v1",
        "created_at": now_iso(),
        "cycle_id": cycle_id,
        "orchestration_mode": "GAM physical-scan + HyperAI local-first reconcile",
        "agent_chain_status": "not_invoked",
        "scan_boundary": [
            "sync_lane_registry",
            "sync_lane_whitelist",
            "titan_proof_artifacts",
            "mac_proof_artifacts",
            "ssh_transport_preconditions",
        ],
        "context_units": [
            {
                "id": "cu_sync_lane_registry",
                "safe": True,
                "relation": "frames",
                "evidence": str(REGISTRY_PATH.relative_to(ROOT)),
            },
            {
                "id": "cu_titan_lane_proof",
                "safe": observe["titan_inventory_exists"] and observe["titan_dirty_ledger_exists"],
                "relation": "validated_by",
                "evidence": [
                    str(TITAN_INVENTORY.relative_to(ROOT)) if TITAN_INVENTORY.exists() else "missing",
                    str(TITAN_LEDGER.relative_to(ROOT)) if TITAN_LEDGER.exists() else "missing",
                ],
            },
            {
                "id": "cu_transport_boundary",
                "safe": bool(observe["ssh_client"]),
                "relation": "secured_by",
                "evidence": observe["ssh_client"] or "ssh client missing",
            },
            {
                "id": "cu_mac_peer_lane",
                "safe": observe["mac_inventory_exists"],
                "relation": "validated_by",
                "evidence": str(MAC_INVENTORY.relative_to(ROOT)) if MAC_INVENTORY.exists() else "missing",
            },
        ],
        "observe": observe,
        "registry_state": {
            "next_valid_action": registry.get("next_valid_action"),
            "promotion_gates": registry.get("promotion_gates", {}),
            "whitelist_version": whitelist.get("whitelist_version"),
        },
        "decide": {
            "selected_action": action,
            "reason": decision_reason,
            "path": ["cu_sync_lane_registry", "cu_titan_lane_proof", "cu_transport_boundary", "cu_mac_peer_lane"],
            "path_cost": 4,
        },
        "act": act,
        "compare_summary": compare_summary,
        "final_state": "executed_with_proof" if action in {"bootstrap_titan_sync_lane", "bootstrap_mac_lane", "compare_only"} else "blocked_by_gate",
    }
    log_path = LOG_DIR / f"{cycle_id}.json"
    payload["log_path"] = str(log_path.relative_to(ROOT))
    write_json(log_path, payload)
    write_json(STATE_PATH, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the autonomous SyncLane governance cycle.")
    parser.add_argument("--mac-host", default=DEFAULT_MAC_HOST, help="Expected MacBook host for the peer lane.")
    parser.add_argument("--identity", default=DEFAULT_IDENTITY, help="SSH identity file for Mac bootstrap.")
    args = parser.parse_args()
    payload = run_cycle(args.mac_host, args.identity)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())