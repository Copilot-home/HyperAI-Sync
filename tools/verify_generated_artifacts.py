#!/usr/bin/env python3
"""Verify the qualification artifacts are complete, valid, and safe."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

OUT = Path("/Users/andy/HyperAI-Sync/runtime/federation_orchestrator")
ARTIFACTS = [
    "runtime_discovery_snapshot.json",
    "role_registry.json",
    "authority_matrix.json",
    "auth_topology.json",
    "dependency_graph.json",
    "binding_plan.json",
    "operational_qualification_report.md",
]

SECRET_RE = re.compile(r"\b(sk-[a-zA-Z0-9_-]{24,}|gh[pousr]_[a-zA-Z0-9_]{20,}|xoxb-[a-zA-Z0-9-]{20,}|AIza[0-9A-Za-z_-]{30,})\b")
SENSITIVE_KEY_RE = re.compile(r"\b(KEY|TOKEN|SECRET|PASSWORD|CRED|AUTH|PRIVATE|PAT|API)\b", re.I)


def _run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return p.returncode, p.stdout, p.stderr


def main() -> int:
    result: dict[str, Any] = {
        "verified_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "files": {},
        "no_plaintext_secrets": True,
        "mcp_docker_mcp_8811_started": False,
        "invariants_preserved": True,
        "qualified_count": None,
        "total_count": None,
    }

    # 1. File existence and JSON validity
    for name in ARTIFACTS:
        path = OUT / name
        exists = path.exists()
        ok = exists
        if exists and name.endswith(".json"):
            try:
                json.loads(path.read_text())
            except Exception as exc:
                ok = False
                result["files"][name] = {"exists": exists, "valid": False, "error": str(exc)}
                continue
        result["files"][name] = {"exists": exists, "valid": ok}

    # 2. No mcp_docker_mcp:8811 listener
    code, out, _ = _run(["lsof", "-nP", "-iTCP:8811", "-sTCP:LISTEN"])
    result["mcp_docker_mcp_8811_started"] = (code == 0 and len(out.strip().splitlines()) > 1)

    # 3. No plaintext secrets in discovery snapshot and auth topology
    leaks = []
    for fname in ("runtime_discovery_snapshot.json", "auth_topology.json", "binding_plan.json"):
        data = json.loads((OUT / fname).read_text())
        text = json.dumps(data)
        for m in SECRET_RE.finditer(text):
            leaks.append({"file": fname, "pattern": m.group(0)[:16] + "..."})
        # ensure env values are masked when key is sensitive
        if fname == "runtime_discovery_snapshot.json":
            for proc in data.get("processes", []):
                for env in proc.get("env", []):
                    if SENSITIVE_KEY_RE.search(env.get("key", "")):
                        value = env.get("value", "")
                        if not value.startswith("<") and len(value) > 10:
                            leaks.append({"file": fname, "pid": proc.get("pid"), "key": env.get("key"), "unmasked_value_prefix": value[:20]})

    result["no_plaintext_secrets"] = len(leaks) == 0
    result["secret_leaks"] = leaks

    # 4. Invariants preserved in report
    report = (OUT / "operational_qualification_report.md").read_text()
    invariants = ["READONLY_DISCOVERY = 1", "AUTO_BINDING = 0", "AUTO_EXECUTION = 0", "AUTO_MUTATION = 0"]
    missing = [inv for inv in invariants if inv not in report]
    result["invariants_preserved"] = len(missing) == 0
    result["missing_invariants"] = missing

    # 5. Qualified count consistency
    plan = json.loads((OUT / "binding_plan.json").read_text())
    result["qualified_count"] = plan.get("qualified")
    result["total_count"] = plan.get("total")

    result["overall"] = (
        all(f.get("exists") and f.get("valid") for f in result["files"].values())
        and result["no_plaintext_secrets"]
        and not result["mcp_docker_mcp_8811_started"]
        and result["invariants_preserved"]
        and result["qualified_count"] is not None
    )

    (OUT / "verification_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"verification: {result['overall']}")
    print(f"  files ok: {len([f for f in result['files'].values() if f['exists'] and f['valid']])}/{len(ARTIFACTS)}")
    print(f"  qualified: {result['qualified_count']}/{result['total_count']}")
    print(f"  no secret leaks: {result['no_plaintext_secrets']}")
    print(f"  mcp_docker_mcp:8811: {result['mcp_docker_mcp_8811_started']}")
    return 0 if result["overall"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
