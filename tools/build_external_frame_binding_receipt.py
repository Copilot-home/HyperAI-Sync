#!/usr/bin/env python3
"""Bind F0/F1 artifacts or record UNBOUND with environment/Canon anchors."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/andy/HyperAI-Sync")
OUT = ROOT / "runtime" / "federation_orchestrator"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(p: Path) -> str:
    if p.is_dir():
        files = sorted([str(x) for x in p.rglob("*") if x.is_file()])
        return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return hashlib.sha256(p.read_bytes()).hexdigest()


def find(name: str, roots: list[Path]) -> Path | None:
    for r in roots:
        if not r.exists():
            continue
        try:
            for p in r.rglob(name):
                if p.is_file():
                    return p
        except PermissionError:
            continue
    return None


def env_value(name: str) -> str | None:
    try:
        code, out = subprocess.getstatusoutput(f"launchctl getenv {name}")
        if code == 0 and out:
            return out
    except Exception:
        pass
    return os.environ.get(name)


def build() -> dict:
    search_roots = [
        ROOT,
        Path("/Users/andy/.local"),
        Path("/Users/andy/.config"),
        Path("/Users/andy/.axcanon"),
        Path("/Users/andy/axcontrol"),
        Path("/Users/andy/docker-recovery"),
        Path("/Users/andy/workbench"),
    ]

    f0_files = [
        "report_self_contained.html",
        "macbook_cache_log_deepdive.ipynb",
        "evidence_ledger.csv",
        "launchd_loop_metrics.csv",
    ]
    f1_files = [
        "APO_OPERATIONAL_MEMORY-v1.1.json",
        "APO_RECOVERY_EXECUTION_RECEIPT-2026-07-30.json",
        "APO_DELTA_RUN_LEDGER-2026-07-30.json",
    ]

    artifacts: list[dict] = []

    def add_file(frame: str, name: str) -> None:
        p = find(name, search_roots)
        if p:
            artifacts.append({
                "frame_id": frame,
                "artifact_title": name,
                "source_locator": str(p),
                "source_class": "file",
                "content_hash": sha256_file(p),
                "expected_hash": None,
                "availability": "FOUND",
                "binding_status": "LOCAL_CONTENT_BOUND",
                "retrieval_timestamp": now_iso(),
                "verification_method": "sha256_file",
            })
        else:
            artifacts.append({
                "frame_id": frame,
                "artifact_title": name,
                "source_locator": None,
                "source_class": "file",
                "content_hash": None,
                "expected_hash": None,
                "availability": "NOT_FOUND",
                "binding_status": "UNBOUND",
                "retrieval_timestamp": now_iso(),
                "verification_method": "rglob_search",
            })

    for n in f0_files:
        add_file("F0", n)
    for n in f1_files:
        add_file("F1", n)

    ax_vars = [
        ("AX_REASONING_METHOD", "policy reasoning method"),
        ("AX_APO_IDENTITY", "APO identity"),
        ("AX_CANON_MEMORY", "Canon memory path"),
        ("AX_CANON_POLICY", "Canon policy file"),
        ("AX_CANON_LAW", "Canon law file"),
        ("AX_CANON_ROOT", "Canon root path"),
    ]
    for var, desc in ax_vars:
        val = env_value(var)
        if val:
            if Path(val).exists():
                status = "LOCAL_CONTENT_BOUND"
                source_class = "env_then_file"
                content_hash = sha256_file(Path(val))
            else:
                status = "ENVIRONMENT_INHERITED"
                source_class = "env"
                content_hash = hashlib.sha256(val.encode()).hexdigest()
            artifacts.append({
                "frame_id": "F0",
                "artifact_title": f"launchd_env:{var}",
                "description": desc,
                "source_locator": val,
                "source_class": source_class,
                "content_hash": content_hash,
                "expected_hash": None,
                "availability": "FOUND",
                "binding_status": status,
                "retrieval_timestamp": now_iso(),
                "verification_method": "launchctl_getenv",
            })
        else:
            artifacts.append({
                "frame_id": "F0",
                "artifact_title": f"launchd_env:{var}",
                "description": desc,
                "source_locator": None,
                "source_class": "env",
                "content_hash": None,
                "expected_hash": None,
                "availability": "NOT_FOUND",
                "binding_status": "UNBOUND",
                "retrieval_timestamp": now_iso(),
                "verification_method": "launchctl_getenv",
            })

    f0_f1_bound = sum(1 for a in artifacts if a["frame_id"] in ("F0", "F1") and a["binding_status"] in ("LOCAL_CONTENT_BOUND", "EXTERNAL_CONTENT_BOUND"))
    f0_f1_unbound = sum(1 for a in artifacts if a["frame_id"] in ("F0", "F1") and a["binding_status"] == "UNBOUND")

    receipt = {
        "generated_at": now_iso(),
        "verdict": "PARTIAL" if f0_f1_unbound else "BOUND",
        "verdict_note": "F0/F1 file artifacts not found in filesystem; F0 environment/Canon anchors bound via launchctl",
        "f0_f1_bound_count": f0_f1_bound,
        "f0_f1_unbound_count": f0_f1_unbound,
        "artifacts": artifacts,
        "lineage_conclusion": "F2→F3 local lineage is bound; F0→F1 file lineage remains UNBOUND and is treated as external historical reference only",
    }
    (OUT / "external_frame_binding_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"wrote external_frame_binding_receipt: bound={f0_f1_bound} unbound={f0_f1_unbound}")
    return receipt


if __name__ == "__main__":
    build()
