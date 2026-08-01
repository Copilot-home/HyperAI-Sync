#!/usr/bin/env python3
"""Verify aios_runtime_qualification.py produces the same qualified set regardless of cwd."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/andy/HyperAI-Sync")
QUALIFIER = ROOT / "tools" / "aios_runtime_qualification.py"
OUT = ROOT / "runtime" / "federation_orchestrator"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_from(cwd: Path) -> dict:
    env = os.environ.copy()
    env["HYPERAI_RUNTIME_ROOT"] = str(ROOT)
    start = datetime.now(timezone.utc).isoformat()
    proc = subprocess.run(
        [sys.executable, str(QUALIFIER)],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    end = datetime.now(timezone.utc).isoformat()
    plan = json.loads((OUT / "binding_plan.json").read_text())
    unqualified = sorted([p["id"] for p in plan["plans"] if not p["operationally_qualified"]])
    return {
        "cwd": str(cwd),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip()[-200:] if proc.stderr else "",
        "started_at": start,
        "completed_at": end,
        "qualified": f"{plan['qualified']}/{plan['total']}",
        "unqualified_ids": unqualified,
        "unqualified_count": len(unqualified),
        "binding_plan_hash": hashlib.sha256((OUT / "binding_plan.json").read_bytes()).hexdigest(),
    }


def main() -> int:
    test_cwds = [
        Path("/"),
        Path.home(),
        OUT,
    ]
    results = [run_from(cwd) for cwd in test_cwds]
    qualified_set = {r["qualified"] for r in results}
    unqualified_sets = [set(r["unqualified_ids"]) for r in results]
    all_same = len(qualified_set) == 1 and all(s == unqualified_sets[0] for s in unqualified_sets)

    receipt = {
        "generated_at": now_iso(),
        "verdict": "PATH_INDEPENDENT" if all_same else "ENVIRONMENTALLY_COUPLED",
        "qualifier": str(QUALIFIER),
        "runtime_root_env_used": str(ROOT),
        "test_runs": results,
        "comparison": {
            "all_qualified_same": len(qualified_set) == 1,
            "all_unqualified_same": all(s == unqualified_sets[0] for s in unqualified_sets),
            "observed_qualified_values": sorted(qualified_set),
            "divergence": [
                {
                    "cwd": r["cwd"],
                    "qualified": r["qualified"],
                    "unqualified_count": r["unqualified_count"],
                }
                for r in results
            ],
        },
    }
    (OUT / "qualifier_path_independence_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"verdict={receipt['verdict']}")
    for r in results:
        print(f"  {r['cwd']}: {r['qualified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
