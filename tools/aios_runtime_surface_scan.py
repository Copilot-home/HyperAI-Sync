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

"""AIOS runtime surface scan for HyperAI-Sync."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "runtime" / "federation_orchestrator" / "aios_ecosystem_runtime_registry.json"


def _run(cmd: list[str], timeout_s: int = 10) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


def scan_listeners() -> dict[str, Any]:
    code, out, err = _run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"])
    if code != 0:
        return {"ok": False, "error": "LSOF_FAILED", "stderr": err.strip()}
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return {"ok": True, "lines": lines[:4000], "truncated": len(lines) > 4000}


def scan_docker_ps() -> dict[str, Any]:
    code, out, err = _run(["docker", "ps", "--no-trunc", "--format", "json"])
    if code != 0:
        return {"ok": False, "error": "DOCKER_PS_FAILED", "stderr": err.strip()}
    items = []
    for ln in out.splitlines()[:2000]:
        try:
            items.append(json.loads(ln))
        except Exception:
            pass
    return {"ok": True, "containers": items}


def load_registry_surfaces() -> dict[str, Any]:
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return {
            "ok": True,
            "surface_count": len(data.get("surfaces", {})),
            "surfaces": sorted(data.get("surfaces", {}).keys()),
        }
    except Exception as e:
        return {"ok": False, "error": f"REGISTRY_READ_FAILED: {e}"}


def scan_disk() -> dict[str, Any]:
    try:
        p = subprocess.run(["df", "-k", "/System/Volumes/Data"], capture_output=True, text=True, timeout=5, check=True)
        lines = p.stdout.splitlines()
        if len(lines) < 2:
            return {"ok": False, "error": "DF_PARSE_FAILED"}
        parts = lines[1].split()
        return {
            "ok": True,
            "size_kb": int(parts[1]),
            "used_kb": int(parts[2]),
            "available_kb": int(parts[3]),
            "capacity_percent": parts[4].rstrip("%"),
            "available_mb": int(parts[3]) // 1024,
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def main() -> int:
    parser = argparse.ArgumentParser(description="AIOS runtime surface scan")
    parser.add_argument("--print-summary", action="store_true", help="Print JSON summary to stdout")
    args = parser.parse_args()

    summary = {
        "schema_version": "2026-04-16.aios-runtime-surface-scan.v1",
        "listeners": scan_listeners(),
        "docker_ps": scan_docker_ps(),
        "disk": scan_disk(),
        "registry": load_registry_surfaces(),
    }

    if args.print_summary:
        print(json.dumps(summary, ensure_ascii=True, indent=2))
    else:
        out_path = ROOT / "runtime" / "federation_orchestrator" / "active_runtime_surface_scan_latest.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())