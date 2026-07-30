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

"""Minimal HyperAI runtime policy builder for HyperAI-Sync."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
POLICY_FILE = RUNTIME / "hyperai-autonomous-policy.json"
PROOF_FILE = RUNTIME / "hyperai-autonomous-boundary-proof.json"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _probe_port(port: int) -> dict[str, Any]:
    """Check if a local TCP port responds to HTTP GET /health."""
    try:
        import urllib.request
        url = f"http://127.0.0.1:{port}/health"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {"reachable": True, "status": resp.status, "body": body[:500]}
    except Exception as e:
        return {"reachable": False, "error": f"{type(e).__name__}: {e}"}


def _disk_free_mb(path: str = "/System/Volumes/Data") -> int:
    try:
        p = subprocess.run(["df", "-k", path], capture_output=True, text=True, timeout=5, check=True)
        lines = p.stdout.splitlines()
        if len(lines) < 2:
            return -1
        return int(lines[1].split()[3]) // 1024
    except Exception:
        return -1


def _disk_state(free_mb: int) -> str:
    if free_mb < 0:
        return "UNKNOWN"
    if free_mb < 2048:
        return "CRITICAL"
    if free_mb < 10240:
        return "MINIMUM_RECOVERED"
    return "STABLE"


def _default_policy() -> dict[str, Any]:
    return {
        "state_transition": "no_prior_state",
        "selected_action": "preserve_runtime",
        "core_ready": False,
        "managed_runtime_health": "unknown",
        "operator_attention_required": True,
        "haios_state": "projection_missing",
        "backend_classification": "unproven",
        "frontend_classification": "unproven",
        "runtime_strategy": "local_first_probe",
        "disk_state": "UNKNOWN",
        "disk_free_mb": -1,
        "manifest_policy": {},
        "managed_runtime": {},
        "action_reason": "Default policy initialized on macOS projection; no live HyperAI product runtime proven yet.",
    }


def build_policy_snapshot() -> dict[str, Any]:
    """Build a fresh policy snapshot from local probes."""
    policy = _default_policy()

    # Probe canonical HyperAI product ports from ecosystem registry / memory
    backend_probe = _probe_port(5000)
    frontend_probe = _probe_port(4173)

    if backend_probe.get("reachable"):
        policy["backend_classification"] = "live"
        policy["core_ready"] = True
        policy["managed_runtime_health"] = "healthy"
        policy["haios_state"] = "live"
    else:
        policy["backend_classification"] = "offline"

    if frontend_probe.get("reachable"):
        policy["frontend_classification"] = "live"
    else:
        policy["frontend_classification"] = "offline"

    free_mb = _disk_free_mb()
    policy["disk_free_mb"] = free_mb
    policy["disk_state"] = _disk_state(free_mb)

    if policy["disk_state"] == "CRITICAL":
        policy["selected_action"] = "runtime_cleanup"
        policy["state_transition"] = "disk_critical"
        policy["operator_attention_required"] = True
        policy["action_reason"] = f"Disk CRITICAL ({free_mb} MiB free); trigger AIOS_CLEANUP_CANON execution."
    elif policy["disk_state"] == "MINIMUM_RECOVERED":
        policy["selected_action"] = "runtime_cleanup"
        policy["state_transition"] = "disk_low"
        policy["operator_attention_required"] = True
        policy["action_reason"] = f"Disk low ({free_mb} MiB free); run disposable cleanup."
    elif policy["core_ready"] and policy["frontend_classification"] == "live":
        policy["operator_attention_required"] = False
        policy["selected_action"] = "reuse_default_runtime"
        policy["state_transition"] = "recover_default_runtime"
        policy["action_reason"] = "Both canonical HyperAI product ports responded; reuse default runtime."
    else:
        policy["operator_attention_required"] = True
        policy["selected_action"] = "local_probe_and_wait"
        policy["state_transition"] = "projection_missing"
        policy["action_reason"] = "Canonical HyperAI product runtime not reachable on macOS; runtime projection missing."

    policy["manifest_policy"] = {
        "boundary_state": policy["haios_state"],
        "selected_action": policy["selected_action"],
        "disk_state": policy["disk_state"],
        "disk_free_mb": free_mb,
        "updated_at": _now(),
    }
    policy["managed_runtime"] = {
        "backendUrl": "http://127.0.0.1:5000" if backend_probe.get("reachable") else None,
        "frontendUrl": "http://127.0.0.1:4173" if frontend_probe.get("reachable") else None,
        "mode": "local_first",
    }
    return policy


def ensure_runtime(policy: dict[str, Any]) -> dict[str, Any]:
    """Validate/add runtime evidence to a policy snapshot."""
    policy = dict(policy)
    policy["runtime_validated_at"] = _now()

    # Reconcile against persisted proof file if present
    if PROOF_FILE.exists():
        try:
            proof = json.loads(PROOF_FILE.read_text(encoding="utf-8"))
            policy["boundary_proof_status"] = proof.get("status", "unknown")
        except Exception:
            policy["boundary_proof_status"] = "invalid"
    else:
        policy["boundary_proof_status"] = "none"

    return policy


def build_persisted_policy_state(policy: dict[str, Any], cycle_number: int = 1) -> dict[str, Any]:
    """Wrap a policy snapshot into a persisted state record."""
    return {
        "cycle_number": cycle_number,
        "persisted_at": _now(),
        "policy": policy,
    }