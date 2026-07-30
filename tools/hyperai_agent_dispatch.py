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

"""Minimal HyperAI agent dispatch for HyperAI-Sync."""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "runtime" / "federation_orchestrator" / "agent_task_outputs"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description="Dispatch a HyperAI agent mission")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--action-class", default="route")
    parser.add_argument("--surface", action="append", default=[])
    args = parser.parse_args()

    mission_id = f"mission-{uuid.uuid4().hex[:16]}"
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    dispatch: dict[str, Any] = {
        "schema_version": "2026-04-16.hyperai-agent-dispatch.v1",
        "mission_id": mission_id,
        "dispatched_at": _now(),
        "title": args.title,
        "description": args.description,
        "action_class": args.action_class,
        "surfaces": args.surface,
        "status": "dispatched",
        "proof": {
            "source": "codex_operator_runtime",
            "gate": "creator_approval_intake",
            "note": "Mission routed through minimal HyperAI agent dispatch on macOS projection.",
        },
    }

    registry = ROOT / "runtime" / "federation_orchestrator" / "agent_task_dispatch_registry.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    if registry.exists():
        try:
            entries = json.loads(registry.read_text(encoding="utf-8"))
            if not isinstance(entries, list):
                entries = [entries]
        except Exception:
            entries = []
    entries.append(dispatch)
    registry.write_text(json.dumps(entries, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(dispatch, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())