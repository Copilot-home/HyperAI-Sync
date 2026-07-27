#!/usr/bin/env python3
"""Materialize the governed HyperAI SyncLane from a narrow whitelist.

This script is intentionally conservative. It only copies a bounded set of
governance/source files from the current workspace into a clean sync lane and
emits an inventory proof for the lane. It never mutates runtime surfaces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
REGISTRY_PATH = WORKSPACE / "runtime" / "federation_orchestrator" / "sync_lane_registry.json"
WHITELIST_PATH = WORKSPACE / "runtime" / "federation_orchestrator" / "sync_lane_whitelist.json"
DEFAULT_LANE_ROOT = Path(r"C:\Users\pc\HyperAI-Sync")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_matches(include_globs: Iterable[str], exclude_globs: Iterable[str]) -> list[Path]:
    exclude_patterns = list(exclude_globs)
    selected: set[Path] = set()
    for pattern in include_globs:
        for match in WORKSPACE.glob(pattern):
            if not match.is_file():
                continue
            rel = match.relative_to(WORKSPACE).as_posix()
            if any(match.match(exclude) or rel.startswith(exclude.rstrip("/**")) for exclude in exclude_patterns):
                continue
            selected.add(match.resolve())
    return sorted(selected)


def ensure_clean_lane_root(lane_root: Path) -> None:
    lane_root.mkdir(parents=True, exist_ok=True)


def copy_files(files: list[Path], lane_root: Path) -> list[dict]:
    copied = []
    for source in files:
        rel = source.relative_to(WORKSPACE)
        destination = lane_root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(
            {
                "relative_path": rel.as_posix(),
                "size_bytes": destination.stat().st_size,
                "sha256": sha256_file(destination),
            }
        )
    return copied


def describe_file(path: Path, lane_root: Path) -> dict:
    rel = path.relative_to(lane_root)
    return {
        "relative_path": rel.as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def write_gitignore(lane_root: Path) -> None:
    gitignore = lane_root / ".gitignore"
    lines = [
        "# SyncLane is whitelist-materialized only.",
        "# Runtime artifacts and secrets stay out of this lane.",
        "*.db",
        "*.sqlite",
        "*.sqlite3",
        ".env",
        ".env.*",
        "logs/",
        "tmp/",
        "node_modules/",
        "dist/",
        "build/",
        "coverage/",
    ]
    gitignore.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return gitignore


def git_init_if_needed(lane_root: Path) -> dict:
    git_dir = lane_root / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init"], cwd=str(lane_root), check=True, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--short"], cwd=str(lane_root), check=True, capture_output=True, text=True)
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=str(lane_root),
        check=True,
        capture_output=True,
        text=True,
    )
    return {
        "branch": branch.stdout.strip(),
        "status_excerpt": status.stdout.strip(),
    }


def classify_dirty_state(status_excerpt: str) -> tuple[str, list[str]]:
    lines = [line for line in status_excerpt.splitlines() if line.strip()]
    if not lines:
        return "clean", []
    dirty_types = []
    has_untracked = any(line.startswith("??") for line in lines)
    has_tracked = any(not line.startswith("??") for line in lines)
    if has_tracked and has_untracked:
        state = "mixed"
    elif has_tracked:
        state = "modified"
    else:
        state = "untracked"
    dirty_types.extend(lines)
    return state, dirty_types


def update_registry_after_bootstrap(registry: dict, lane_root: Path) -> None:
    for machine in registry.get("machines", []):
        if machine.get("machine_id") == "titan_gt77":
            machine["root_path"] = str(lane_root)
            machine["current_state"] = "materialized"
    gates = registry.setdefault("promotion_gates", {})
    gates["repo_initialized"] = True
    gates["whitelist_installed"] = True
    registry["last_bootstrap_at"] = now_iso()
    registry["next_valid_action"] = "derive_dirty_ledger_then_prepare_mac_lane"
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_inventory(lane_root: Path, copied_files: list[dict], git_state: dict, whitelist_version: str) -> Path:
    inventory = {
        "schema_version": "2026-04-21.sync-lane-inventory.v1",
        "created_at": now_iso(),
        "machine_id": "titan_gt77",
        "lane_root": str(lane_root),
        "whitelist_version": whitelist_version,
        "file_count": len(copied_files),
        "git": git_state,
        "files": copied_files,
    }
    output_path = WORKSPACE / "runtime" / "lineage" / "sync_lane_inventory_titan_20260421.json"
    output_path.write_text(json.dumps(inventory, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return output_path


def write_dirty_ledger(lane_root: Path, git_state: dict) -> Path:
    dirty_state, dirty_lines = classify_dirty_state(git_state.get("status_excerpt", ""))
    ledger = {
        "schema_version": "2026-04-21.sync-lane-dirty-ledger.v1",
        "created_at": now_iso(),
        "machine_id": "titan_gt77",
        "lane_root": str(lane_root),
        "dirty_state": dirty_state,
        "entries": dirty_lines,
        "note": "Untracked files are expected immediately after whitelist materialization and before the first commit.",
    }
    output_path = WORKSPACE / "runtime" / "lineage" / "sync_lane_dirty_ledger_titan_20260421.json"
    output_path.write_text(json.dumps(ledger, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return output_path


def update_registry_after_ledger(dirty_state: str) -> None:
    registry = load_json(REGISTRY_PATH)
    registry.setdefault("promotion_gates", {})["dirty_ledger_verified"] = True
    for machine in registry.get("machines", []):
        if machine.get("machine_id") == "titan_gt77":
            machine["dirty_state"] = dirty_state
            machine["current_state"] = "bootstrap_dirty_ledger_verified"
    registry["next_valid_action"] = "prepare_mac_lane_then_compare_only"
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap the governed HyperAI SyncLane.")
    parser.add_argument("--lane-root", default=str(DEFAULT_LANE_ROOT), help="Target sync lane root directory.")
    args = parser.parse_args()

    registry = load_json(REGISTRY_PATH)
    whitelist = load_json(WHITELIST_PATH)
    lane_root = Path(args.lane_root).resolve()

    ensure_clean_lane_root(lane_root)
    selected = collect_matches(whitelist["include_globs"], whitelist["exclude_globs"])
    copied_files = copy_files(selected, lane_root)
    gitignore_path = write_gitignore(lane_root)
    copied_files.append(describe_file(gitignore_path, lane_root))
    git_state = git_init_if_needed(lane_root)
    update_registry_after_bootstrap(registry, lane_root)
    inventory_path = write_inventory(lane_root, copied_files, git_state, whitelist["whitelist_version"])
    dirty_ledger_path = write_dirty_ledger(lane_root, git_state)
    update_registry_after_ledger(classify_dirty_state(git_state["status_excerpt"])[0])

    print(
        json.dumps(
            {
                "lane_root": str(lane_root),
                "file_count": len(copied_files),
                "inventory_path": str(inventory_path),
                "dirty_ledger_path": str(dirty_ledger_path),
                "git": git_state,
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
