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

from __future__ import annotations

import json
import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from hyperai_runtime_policy import build_persisted_policy_state, build_policy_snapshot, ensure_runtime


ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "memory"
RUNTIME = ROOT / "runtime"
STATE_FILE = RUNTIME / "hyperai-autonomous-cycle-state.json"
POLICY_FILE = RUNTIME / "hyperai-autonomous-policy.json"
PROOF_FILE = RUNTIME / "hyperai-autonomous-boundary-proof.json"
FEDERATION_DIR = RUNTIME / "federation_orchestrator"
BRIDGE_FILE = FEDERATION_DIR / "autonomous_cycle_orchestration_bridge.json"
DELTA_SCRIPT = ROOT / "tools" / "check_hyperai_delta.py"
HAIOS_STATE_MODEL = MEMORY / "HAIOS_STATE_MODEL.md"
AGENT3_CAPSULE = MEMORY / "agent3_api_client_contract_capsule.md"
AGENT4_CAPSULE = MEMORY / "agent4_frontend_composition_capsule.md"
AGENT6_CAPSULE = MEMORY / "agent6_synthesis_capsule.md"


def run_delta() -> dict:
    proc = subprocess.run(
        [sys.executable, str(DELTA_SCRIPT)],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def read_state() -> dict | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_policy_state() -> dict | None:
    if not POLICY_FILE.exists():
        return None
    try:
        return json.loads(POLICY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_proof_state() -> dict | None:
    if not PROOF_FILE.exists():
        return None
    try:
        return json.loads(PROOF_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_state(payload: dict) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_bridge(payload: dict) -> None:
    FEDERATION_DIR.mkdir(parents=True, exist_ok=True)
    BRIDGE_FILE.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_policy(policy: dict) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    persisted_policy = read_policy_state() or {}
    cycle_number = policy.get("persisted_policy_state", {}).get(
        "cycle_number",
        persisted_policy.get("cycle_number", 0) + 1,
    )
    payload = build_persisted_policy_state(policy, cycle_number=cycle_number)
    payload["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    POLICY_FILE.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def upsert_markdown_section(path: Path, heading: str, body_lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    section = "\n".join([heading, "", *body_lines]).rstrip() + "\n"
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            break

    if start is None:
        updated = text.rstrip() + ("\n\n" if text.strip() else "") + section
        path.write_text(updated, encoding="utf-8")
        return

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break

    replacement = section.strip("\n").splitlines()
    updated_lines = lines[:start] + replacement + lines[end:]
    path.write_text("\n".join(updated_lines).rstrip() + "\n", encoding="utf-8")


def sync_haios_state_model(summary: dict, policy: dict) -> None:
    proof_events = policy.get("manifest_policy", {}).get("proof_events") or policy.get("proof_events") or []
    event_lines = [
        f"- {event.get('at', 'unknown')} | {event.get('type', 'event')} | {event.get('detail', '')}"
        for event in proof_events[-3:]
        if isinstance(event, dict)
    ] or ["- No recent proof events recorded."]
    upsert_markdown_section(
        HAIOS_STATE_MODEL,
        "## Latest Browser Cockpit Proof",
        [
            f"- last checked: {summary['policy_manifest'].get('updated_at', summary['policy_manifest'].get('updated_at', 'unknown'))}",
            f"- boundary state: {summary['policy_boundary_state']}",
            f"- selected action: {summary['policy_manifest_action']}",
            f"- backend classification: {summary['backend_classification']}",
            f"- frontend classification: {summary['frontend_classification']}",
            f"- runtime strategy: {summary['runtime_strategy']}",
            f"- operator relay required: {'yes' if summary['operator_attention_required'] else 'no'}",
            "- recent proof events:",
            *event_lines,
        ],
    )


def sync_capsules(summary: dict, policy: dict) -> None:
    manifest_policy = summary["policy_manifest"] or {}
    proof_events = manifest_policy.get("proof_events") or []
    proof_event_lines = [
        f"- {event.get('type', 'event')}: {event.get('detail', '')}"
        for event in proof_events[-3:]
        if isinstance(event, dict)
    ] or ["- No recent proof events recorded."]
    upsert_markdown_section(
        AGENT3_CAPSULE,
        "## Delta 2026-04-01 Autonomous Policy Authority",
        [
            "- `/api/autonomy/policy` is now part of the live app-core contract and should be treated as the browser-safe authority snapshot.",
            f"- current selected action: `{summary['policy_manifest_action']}`",
            f"- current boundary state: `{summary['policy_boundary_state']}`",
            f"- backend classification: `{summary['backend_classification']}`",
            f"- frontend classification: `{summary['frontend_classification']}`",
            "- recent proof events:",
            *proof_event_lines,
        ],
    )
    upsert_markdown_section(
        AGENT4_CAPSULE,
        "## Delta 2026-04-01 Autonomous Authority Surfacing",
        [
            "- `AutonomyContext.tsx` and `AutonomyPanel.tsx` should treat `/api/autonomy/policy` as the UI-facing authority artifact for routine runtime decisions.",
            "- The main shell remains limited to the autonomy-safe core while policy proof events explain default vs managed authority changes.",
            f"- current runtime story: `{summary['policy_manifest_action']}` with boundary `{summary['policy_boundary_state']}`",
            f"- runtime strategy: `{summary['runtime_strategy']}`",
        ],
    )
    upsert_markdown_section(
        AGENT6_CAPSULE,
        "## Current Autonomous Boundary Proof",
        [
            f"- boundary state: `{summary['policy_boundary_state']}`",
            f"- selected action: `{summary['policy_manifest_action']}`",
            f"- runtime strategy: `{summary['runtime_strategy']}`",
            f"- backend classification: `{summary['backend_classification']}`",
            f"- frontend classification: `{summary['frontend_classification']}`",
            f"- operator relay required: `{'yes' if summary['operator_attention_required'] else 'no'}`",
            "- recent proof events:",
            *proof_event_lines,
        ],
    )


def build_summary(delta: dict, policy: dict) -> dict:
    managed_runtime = policy.get("managed_runtime") or {}
    manifest_policy = policy.get("manifest_policy") or {}
    manifest_policy_action = manifest_policy.get("selected_action") or policy.get("selected_action")
    manifest_boundary_state = manifest_policy.get("boundary_state") or policy.get("haios_state")
    proof = read_proof_state() or {}
    return {
        "workspace_root": delta["workspace_root"],
        "product_surface": delta["product_surface"],
        "state_transition": policy["state_transition"],
        "selected_action": policy["selected_action"],
        "core_ready": policy["core_ready"],
        "managed_runtime_health": policy["managed_runtime_health"],
        "operator_attention_required": policy["operator_attention_required"],
        "haios_state": policy["haios_state"],
        "backend_classification": policy["backend_classification"],
        "frontend_classification": policy["frontend_classification"],
        "runtime_strategy": policy["runtime_strategy"],
        "recent_change_count": len(delta["recent_changes_since_memory"]),
        "managed_runtime_mode": managed_runtime.get("mode"),
        "managed_runtime_backend": managed_runtime.get("backendUrl"),
        "managed_runtime_frontend": managed_runtime.get("frontendUrl"),
        "policy_manifest": manifest_policy,
        "policy_manifest_action": manifest_policy_action,
        "policy_boundary_state": manifest_boundary_state,
        "boundary_proof_status": proof.get("status"),
        "boundary_proof_checked_at": proof.get("checked_at"),
        "boundary_proof_action": proof.get("selected_action"),
        "boundary_proof_path": str(PROOF_FILE) if proof else None,
        "orchestration_mode": "preservation_only",
        "agent_chain_status": "not_requested",
        "orchestration_bridge_path": str(BRIDGE_FILE),
    }


def maybe_update_memory(summary: dict, policy: dict) -> None:
    previous = read_state()
    if previous == summary:
        sync_haios_state_model(summary, policy)
        sync_capsules(summary, policy)
        return
    write_state(summary)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "update_memory.py"),
            "--focus",
            "Autonomous local-first runtime cycle",
            "--summary",
            (
                f"Cycle transitioned via {summary['state_transition']} with core_ready={summary['core_ready']} "
                f"and managed_runtime_health={summary['managed_runtime_health']}."
                f" Manifest policy reports boundary={summary['policy_boundary_state']} and action={summary['policy_manifest_action']}."
            ),
            "--next",
            policy["action_reason"],
        ],
        cwd=str(ROOT),
        check=False,
    )
    sync_haios_state_model(summary, policy)
    sync_capsules(summary, policy)


def run_json_command(command: list[str]) -> tuple[dict, str, str]:
    proc = subprocess.run(
        command,
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    stdout = proc.stdout.strip()
    data = json.loads(stdout) if stdout else {}
    return data, proc.stdout, proc.stderr


def run_text_command(command: list[str]) -> tuple[str, str]:
    proc = subprocess.run(
        command,
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout, proc.stderr


def run_agent_chain(summary: dict, args: argparse.Namespace) -> dict:
    bridge_started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    bridge = {
        "schema_version": "2026-04-16.autonomous-cycle-orchestration-bridge.v1",
        "started_at": bridge_started_at,
        "mode": "agent_chain",
        "non_destructive": True,
        "cycle_state": {
            "state_transition": summary["state_transition"],
            "selected_action": summary["selected_action"],
            "core_ready": summary["core_ready"],
            "runtime_strategy": summary["runtime_strategy"],
            "recent_change_count": summary["recent_change_count"],
        },
        "steps": [],
        "final_state": "running",
    }
    write_bridge(bridge)

    scan_stdout, _ = run_text_command([sys.executable, str(ROOT / "tools" / "aios_runtime_surface_scan.py"), "--print-summary"])
    bridge["steps"].append(
        {
            "name": "pre_dispatch_surface_scan",
            "status": "completed",
            "command": "python tools/aios_runtime_surface_scan.py --print-summary",
            "stdout": scan_stdout.strip(),
            "artifact": "runtime/federation_orchestrator/active_runtime_surface_scan_20260416.json",
        }
    )
    write_bridge(bridge)

    surfaces = args.surface or [
        "hyperai_product_runtime",
        "federation_orchestrator",
        "memory_writer",
        "verification_truth",
        "codex_operator_runtime",
        "openclaw_control_lane",
        "local_fakeapi_provider_fabric",
        "ollama_local_models",
        "mcp_connectors",
    ]
    dispatch_command = [
        sys.executable,
        str(ROOT / "tools" / "hyperai_agent_dispatch.py"),
        "--title",
        args.mission_title,
        "--description",
        args.mission_description,
        "--action-class",
        args.action_class,
    ]
    for surface in surfaces:
        dispatch_command.extend(["--surface", surface])
    dispatch_result, dispatch_stdout, _ = run_json_command(dispatch_command)
    mission_id = dispatch_result["mission_id"]
    bridge["steps"].append(
        {
            "name": "mission_dispatch",
            "status": "completed",
            "command": "python tools/hyperai_agent_dispatch.py ...",
            "mission_id": mission_id,
            "proof": dispatch_result.get("proof"),
            "stdout": dispatch_stdout.strip(),
        }
    )
    write_bridge(bridge)

    worker_result, worker_stdout, _ = run_json_command(
        [sys.executable, str(ROOT / "tools" / "hyperai_agent_worker_loop.py"), "--mission-id", mission_id]
    )
    bridge["steps"].append(
        {
            "name": "agent_worker_loop",
            "status": "completed",
            "command": f"python tools/hyperai_agent_worker_loop.py --mission-id {mission_id}",
            "mission_id": mission_id,
            "executed_agents": worker_result.get("executed_agents", []),
            "mission_status": worker_result.get("mission_status"),
            "final_state": worker_result.get("final_state"),
            "route_plan": worker_result.get("route_plan"),
            "stdout": worker_stdout.strip(),
        }
    )
    bridge["mission_id"] = mission_id
    bridge["final_state"] = worker_result.get("final_state", "needs_missing_evidence")
    bridge["completed_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    bridge["monitoring_artifacts"] = {
        "dispatch_registry": "runtime/federation_orchestrator/agent_task_dispatch_registry.json",
        "agent_outputs": f"runtime/federation_orchestrator/agent_task_outputs/{mission_id}",
        "route_plan": worker_result.get("route_plan"),
    }
    write_bridge(bridge)
    return bridge


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HyperAI local-first runtime cycle.")
    parser.add_argument(
        "--agent-chain",
        action="store_true",
        help="After runtime preservation proof, scan surfaces, dispatch a 6-agent mission, and run the worker loop.",
    )
    parser.add_argument(
        "--mission-title",
        default="Autonomous cycle routed through Agent 1-6",
        help="Mission title used when --agent-chain is set.",
    )
    parser.add_argument(
        "--mission-description",
        default=(
            "Create a governed plan from the autonomous runtime cycle, route it through the HyperAI "
            "Agent 1-6 chain, and close with proof before any implementation work."
        ),
        help="Mission description used when --agent-chain is set.",
    )
    parser.add_argument(
        "--action-class",
        default="route",
        choices=["inspect", "classify", "plan", "reason", "runtime_preserve", "runtime_probe", "route"],
        help="Dispatch action class used when --agent-chain is set.",
    )
    parser.add_argument("--surface", action="append", default=[], help="Target surface id for the dispatched mission. Can be repeated.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    delta = run_delta()
    policy = ensure_runtime(build_policy_snapshot())
    write_policy(policy)
    summary = build_summary(delta, policy)
    bridge = None
    if args.agent_chain:
        bridge = run_agent_chain(summary, args)
        summary["orchestration_mode"] = "agent_chain"
        summary["agent_chain_status"] = bridge.get("final_state")
        summary["agent_chain_mission_id"] = bridge.get("mission_id")
        summary["agent_chain_route_plan"] = bridge.get("monitoring_artifacts", {}).get("route_plan")
    maybe_update_memory(summary, policy)
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()