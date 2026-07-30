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

"""HyperAI OODA loop runner.

This runner keeps Codex and other AI systems in the correct role: workers
receive assignments from the HyperAI core loop instead of bypassing it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "runtime" / "federation_orchestrator"
STATE_PATH = RUNTIME_DIR / "autonomous_ooda_loop_state.json"
LOG_DIR = RUNTIME_DIR / "autonomous_ooda_logs"
WORKFLOW_PATH = RUNTIME_DIR / "autonomous_ooda_workflow.json"
WORKER_POLICY_PATH = RUNTIME_DIR / "worker_runtime_binding_policy.json"
ECOSYSTEM_REGISTRY_PATH = RUNTIME_DIR / "aios_ecosystem_runtime_registry.json"
AIDEV_TRACE_PATH = ROOT / "memory" / "AIDEV_DEEP_TRACE_REPORT_20260415.md"
AIDEV_CAPABILITY_TREE_PATH = ROOT / "memory" / "HYPERAI_AIDEV_CAPABILITY_TREE.md"


DEFAULT_SURFACES = [
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


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(command: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def parse_first_json(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            payload, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    raise ValueError("no JSON object found in command output")


def classify_task(task: str | None, preservation: dict[str, Any]) -> dict[str, Any]:
    text = (task or "").lower()
    if not task:
        recent_changes = int(preservation.get("recent_change_count") or 0)
        return {
            "task_class": "preservation",
            "requires_agent_chain": recent_changes > 0,
            "reason": "No explicit task; agent chain is required only if preservation cycle detected meaningful delta.",
        }
    if any(token in text for token in ["deploy", "publish", "telegram", "wallet", "cloud", "phone", "device", "cron"]):
        return {
            "task_class": "gated_external_or_side_effect",
            "requires_agent_chain": True,
            "reason": "Task mentions external or side-effect surface; route plan and gates are required.",
        }
    if any(token in text for token in ["code", "implement", "fix", "build", "runtime", "workflow", "agent", "ooda", "autonom"]):
        return {
            "task_class": "governed_system_task",
            "requires_agent_chain": True,
            "reason": "Task changes or evaluates system operation; Agent 1-6 closure is required before implementation handoff.",
        }
    return {
        "task_class": "bounded_reasoning_or_diagnostic",
        "requires_agent_chain": True,
        "reason": "HyperAI task intake should still produce a governed mission unless explicitly preservation-only.",
    }


def build_mission_text(task: str | None, orientation: dict[str, Any]) -> tuple[str, str]:
    task_text = task or "OODA maintenance cycle"
    title = f"OODA routed task: {task_text[:80]}"
    description = (
        "Run the HyperAI OODA loop for the creator input. Observe active runtime surfaces, orient against "
        "AIOS memory/registry and AIDEV genesis/core lineage, decide the valid worker route, and close "
        f"with Agent 6 proof before implementation handoff. Task: {task_text}. "
        f"Orientation: {orientation['task_class']} - {orientation['reason']}"
    )
    return title, description


def run_preservation_cycle() -> dict[str, Any]:
    code, stdout, stderr = run_command([sys.executable, str(ROOT / "tools" / "hyperai_autonomous_cycle.py")])
    if code != 0:
        raise RuntimeError(f"preservation cycle failed: {stderr.strip() or stdout.strip()}")
    return parse_first_json(stdout)


def run_scan() -> dict[str, Any]:
    code, stdout, stderr = run_command([sys.executable, str(ROOT / "tools" / "aios_runtime_surface_scan.py"), "--print-summary"])
    if code != 0:
        raise RuntimeError(f"surface scan failed: {stderr.strip() or stdout.strip()}")
    return parse_first_json(stdout)


def run_agent_chain(title: str, description: str, surfaces: list[str]) -> dict[str, Any]:
    command = [
        sys.executable,
        str(ROOT / "tools" / "hyperai_autonomous_cycle.py"),
        "--agent-chain",
        "--mission-title",
        title,
        "--mission-description",
        description,
    ]
    for surface in surfaces:
        command.extend(["--surface", surface])
    code, stdout, stderr = run_command(command)
    if code != 0:
        raise RuntimeError(f"agent chain failed: {stderr.strip() or stdout.strip()}")
    return parse_first_json(stdout)


def run_ooda_cycle(task: str | None, surfaces: list[str]) -> dict[str, Any]:
    cycle_id = f"ooda-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    workflow = load_json(WORKFLOW_PATH)
    worker_policy = load_json(WORKER_POLICY_PATH)
    ecosystem = load_json(ECOSYSTEM_REGISTRY_PATH)

    observe_scan = run_scan()
    preservation = run_preservation_cycle()
    orientation = classify_task(task, preservation)
    title, description = build_mission_text(task, orientation)

    act: dict[str, Any]
    if orientation["requires_agent_chain"]:
        agent_chain = run_agent_chain(title, description, surfaces)
        final_state = agent_chain.get("agent_chain_status") or "needs_missing_evidence"
        act = {
            "action": "agent_chain_dispatched",
            "mission_id": agent_chain.get("agent_chain_mission_id"),
            "route_plan": agent_chain.get("agent_chain_route_plan"),
            "agent_chain_status": agent_chain.get("agent_chain_status"),
            "orchestration_bridge": agent_chain.get("orchestration_bridge_path"),
        }
    else:
        final_state = "no_meaningful_delta"
        act = {
            "action": "preservation_only_no_dispatch",
            "reason": orientation["reason"],
        }

    payload = {
        "schema_version": "2026-04-16.hyperai-ooda-cycle-log.v1",
        "cycle_id": cycle_id,
        "created_at": now_iso(),
        "input_surface": "codex_operator_runtime_or_current_worker",
        "task": task,
        "observe": {
            "surface_scan": observe_scan,
            "preservation": {
                "state_transition": preservation.get("state_transition"),
                "core_ready": preservation.get("core_ready"),
                "runtime_strategy": preservation.get("runtime_strategy"),
                "recent_change_count": preservation.get("recent_change_count"),
                "orchestration_mode": preservation.get("orchestration_mode"),
                "agent_chain_status": preservation.get("agent_chain_status"),
            },
        },
        "orient": {
            **orientation,
            "workflow": str(WORKFLOW_PATH.relative_to(ROOT)),
            "worker_policy": str(WORKER_POLICY_PATH.relative_to(ROOT)),
            "ecosystem_registry": str(ECOSYSTEM_REGISTRY_PATH.relative_to(ROOT)),
            "aidev_lineage_inputs": [
                str(AIDEV_TRACE_PATH.relative_to(ROOT)),
                str(AIDEV_CAPABILITY_TREE_PATH.relative_to(ROOT)),
            ],
            "registered_surface_count": len(ecosystem.get("surfaces", {})),
            "worker_distribution_rule": worker_policy.get("worker_distribution_rule") or worker_policy.get("system_rule"),
        },
        "decide": {
            "requires_agent_chain": orientation["requires_agent_chain"],
            "selected_surfaces": surfaces,
            "decision_reason": orientation["reason"],
        },
        "act": act,
        "final_state": final_state,
        "remaining_risk": [
            "Direct low-level tool calls can still bypass OODA if operators ignore this entrypoint.",
            "AIDEV genesis/core lineage remains source-capability until fresh runtime proof promotes a lane.",
        ],
    }
    log_path = LOG_DIR / f"{cycle_id}.json"
    payload["log_path"] = str(log_path.relative_to(ROOT))
    write_json(log_path, payload)
    write_json(STATE_PATH, payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HyperAI OODA loop and distribute work to registered AI workers.")
    parser.add_argument("--task", help="Creator task/control signal to route through the OODA loop.")
    parser.add_argument("--surface", action="append", default=[], help="Target surface id. Can be repeated.")
    parser.add_argument("--cycles", type=int, default=1, help="Number of OODA cycles to run.")
    parser.add_argument("--sleep-seconds", type=int, default=30, help="Delay between cycles.")
    parser.add_argument("--once", action="store_true", help="Alias for --cycles 1.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cycles = 1 if args.once else max(args.cycles, 1)
    surfaces = args.surface or DEFAULT_SURFACES
    last_payload: dict[str, Any] | None = None
    try:
        for index in range(cycles):
            last_payload = run_ooda_cycle(args.task, surfaces)
            if index < cycles - 1:
                time.sleep(args.sleep_seconds)
        print(json.dumps(last_payload, indent=2, ensure_ascii=False))
        return 0
    except Exception as error:
        payload = {
            "schema_version": "2026-04-16.hyperai-ooda-cycle-log.v1",
            "created_at": now_iso(),
            "final_state": "blocked_by_gate",
            "error": f"{type(error).__name__}: {error}",
        }
        write_json(STATE_PATH, payload)
        print(json.dumps(payload, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())