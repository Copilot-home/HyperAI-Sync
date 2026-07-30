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

"""Compute local delta for HyperAI-Sync preservation cycle."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MEMORY_ANCHOR = ROOT / "memory" / "runtime_execution_todo.md"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _git_recent_changes() -> list[str]:
    """Return a compact list of recently modified tracked files."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain", "-uno"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode != 0:
            return []
        changes = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        return changes[:200]
    except Exception:
        return []


def _repo_size() -> int:
    try:
        proc = subprocess.run(
            ["git", "count-objects", "-vH"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Just return stdout length as a cheap metric
        return len(proc.stdout)
    except Exception:
        return 0


def main() -> int:
    changes = _git_recent_changes()
    payload: dict[str, Any] = {
        "schema_version": "2026-04-16.hyperai-delta.v1",
        "checked_at": _now(),
        "workspace_root": str(ROOT),
        "product_surface": str(ROOT / ".." / "HyperAI"),
        "memory_anchor": str(MEMORY_ANCHOR),
        "recent_changes_since_memory": changes,
        "recent_change_count": len(changes),
        "repo_size_metric": _repo_size(),
        "delta_note": "macOS projection; canonical Windows product surface not present.",
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())