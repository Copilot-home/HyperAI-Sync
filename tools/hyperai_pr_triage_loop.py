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

"""HyperAI PR Triage Autonomous Loop.

Monitors the ecosystem PR queue by repeatedly invoking
`hyperai_pr_triage_agent.py` until no low-risk actions remain.

  1. Run triage agent with --execute.
  2. Read the generated triage_report.json.
  3. If actions == 0 -> stop.
  4. If actions > 0 and max iterations not reached -> wait and re-run.
  5. Aggregate final state.

This implements the "cậu theo dõi quản lý tới xong thì dừng" instruction:
let HyperAI auto-run, the assistant monitors, and the loop stops when done.
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
TRIAGE = ROOT / "tools" / "hyperai_pr_triage_agent.py"
DEFAULT_OUTPUT = ROOT / "runtime" / "federation_orchestrator" / "agent_task_outputs"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_triage(
    mission_id: str,
    owners: list[str],
    stale_days: int,
    execute: bool,
    output_dir: Path,
) -> dict[str, Any] | None:
    cmd = [
        sys.executable,
        str(TRIAGE),
        "--stale-days",
        str(stale_days),
        "--mission-id",
        mission_id,
        "--output-dir",
        str(output_dir),
        "--owners",
        *owners,
    ]
    if execute:
        cmd.append("--execute")

    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout, end="")
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        return None

    report_path = output_dir / mission_id / "triage_report.json"
    if not report_path.exists():
        return None
    return json.loads(report_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="HyperAI PR Triage Autonomous Loop")
    parser.add_argument("--owners", nargs="+", default=["NguyenCuong1989", "Copilot-home"])
    parser.add_argument("--stale-days", type=int, default=90)
    parser.add_argument("--max-iter", type=int, default=5)
    parser.add_argument("--sleep", type=int, default=10)
    parser.add_argument("--mission-id", default=f"mission-pr-triage-loop-{_now().replace(':', '')}")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    loop_dir = args.output_dir / args.mission_id
    loop_dir.mkdir(parents=True, exist_ok=True)

    iterations: list[dict[str, Any]] = []
    total_closed = 0
    total_merged = 0

    print(f"=== HyperAI PR Triage Autonomous Loop ===")
    print(f"mission_id: {args.mission_id}")
    print(f"owners: {args.owners}")
    print(f"stale_days: {args.stale_days}")
    print(f"max_iter: {args.max_iter}")
    print("")

    for i in range(1, args.max_iter + 1):
        iter_id = f"{args.mission_id}-iter-{i}"
        print(f"--- Iteration {i}: {iter_id} ---")
        report = run_triage(
            mission_id=iter_id,
            owners=args.owners,
            stale_days=args.stale_days,
            execute=True,
            output_dir=args.output_dir,
        )
        if report is None:
            print(f"[iter {i}] triage agent failed; aborting loop.")
            iterations.append({"iteration": i, "mission_id": iter_id, "status": "failed"})
            break

        summary = report.get("summary", {})
        actions = summary.get("actions", 0)
        closed = summary.get("closed", 0)
        merged = summary.get("merged", 0)
        if closed:
            total_closed += closed
        if merged:
            total_merged += merged

        iterations.append({
            "iteration": i,
            "mission_id": iter_id,
            "status": "completed",
            "summary": summary,
            "report": str(args.output_dir / iter_id / "triage_report.json"),
        })

        print(f"[iter {i}] actions={actions}, closed={closed}, merged={merged}")
        if actions == 0:
            print(f"[iter {i}] no low-risk actions remaining. loop complete.")
            break

        if i < args.max_iter:
            print(f"[iter {i}] sleeping {args.sleep}s before next scan...")
            time.sleep(args.sleep)
    else:
        print(f"[loop] reached max iterations ({args.max_iter}) without empty queue.")

    final = {
        "schema_version": "2026-04-16.hyperai-pr-triage-loop.v1",
        "mission_id": args.mission_id,
        "timestamp": _now(),
        "owners": args.owners,
        "stale_days": args.stale_days,
        "max_iter": args.max_iter,
        "iterations": iterations,
        "total_closed": total_closed,
        "total_merged": total_merged,
        "final_state": "loop_complete" if (iterations and iterations[-1]["summary"].get("actions", 0) == 0) else "max_iter_reached",
    }
    (loop_dir / "loop_state.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")

    print("")
    print(f"=== Loop Summary ===")
    print(f"iterations run: {len(iterations)}")
    print(f"total closed: {total_closed}")
    print(f"total merged: {total_merged}")
    print(f"final state: {final['final_state']}")
    print(f"loop state: {loop_dir / 'loop_state.json'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())