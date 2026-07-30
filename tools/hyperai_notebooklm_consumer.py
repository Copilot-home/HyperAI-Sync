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
"""Mode C: drive the consumer NotebookLM via the `notebooklm-py` CLI.

Requires `notebooklm` on PATH and a valid Chrome-cookie session under
`~/.notebooklm/profiles/default/storage_state.json`.

This uses the unofficial `teng-lin/notebooklm-py` package. It is a
browser-derived surface; use only when the creator has authenticated and the
risk of ToS/rate-limit changes is accepted.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


BUNDLE = Path("/Users/andy/.axcanon/memory/notebooklm")
DRIVE_MANIFEST = BUNDLE / "drive_manifest.json"
NOTEBOOKLM_DIR = Path.home() / ".notebooklm"


def run(args: list[str], timeout: int = 180, check: bool = True) -> dict[str, Any]:
    cmd = ["notebooklm"] + args
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        result: dict[str, Any] = {"cmd": " ".join(cmd), "rc": proc.returncode, "stdout": out, "stderr": err}
        if out:
            try:
                result["json"] = json.loads(out)
            except json.JSONDecodeError:
                result["json"] = None
        if check and proc.returncode != 0:
            raise RuntimeError(f"notebooklm failed: {err or out}")
        return result
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"notebooklm timeout: {e}") from e


def ensure_auth() -> bool:
    r = run(["auth", "check", "--test", "--json"], timeout=60, check=False)
    data = r.get("json") or {}
    return data.get("status") == "ok"


def refresh_auth() -> None:
    # Best-effort silent refresh from Chrome cookies.
    try:
        run(["auth", "refresh", "--browser-cookies", "chrome", "--quiet"], timeout=120, check=False)
    except Exception:
        pass


def load_drive_manifest() -> dict[str, Any]:
    if not DRIVE_MANIFEST.exists():
        raise FileNotFoundError(f"Drive manifest not found: {DRIVE_MANIFEST}")
    return json.loads(DRIVE_MANIFEST.read_text(encoding="utf-8"))


def find_or_create_notebook(title: str = "Σ_APΩ") -> str:
    r = run(["list", "--json"], timeout=60)
    data = r.get("json") or {}
    for nb in data.get("notebooks", []):
        if nb.get("title") == title:
            return str(nb["id"])
    create_r = run(["create", title, "--json"], timeout=120)
    create_data = create_r.get("json") or {}
    return str(create_data["notebook"]["id"])


def set_notebook(notebook_id: str) -> None:
    run(["use", notebook_id], timeout=60)


def add_drive_source(doc_id: str, title: str) -> dict[str, Any]:
    r = run(["source", "add-drive", doc_id, title, "--json"], timeout=120, check=False)
    return r.get("json") or {}


def sync_sources(notebook_id: str) -> dict[str, Any]:
    manifest = load_drive_manifest()
    results = []
    # Get existing source titles.
    existing = run(["source", "list", "--json"], timeout=60)
    existing_data = existing.get("json") or {}
    existing_titles = {s.get("title") for s in existing_data.get("sources", [])}
    for md_name, info in manifest.get("sources", {}).items():
        title = info["title"]
        doc_id = info["doc_id"]
        if title in existing_titles:
            results.append({"md_name": md_name, "title": title, "doc_id": doc_id, "skipped": True})
            continue
        res = add_drive_source(doc_id, title)
        results.append({"md_name": md_name, "title": title, "doc_id": doc_id, "result": res})
    return {"notebook_id": notebook_id, "sources": results}


def generate_mind_map(notebook_id: str, language: str = "vi") -> dict[str, Any]:
    r = run(
        ["generate", "mind-map", "--kind", "interactive", "--language", language, "--json"],
        timeout=300,
    )
    return r.get("json") or {}


def download_mind_map(notebook_id: str, out_path: Path, force: bool = True) -> dict[str, Any]:
    args = ["download", "mind-map", str(out_path)]
    if force:
        args.append("--force")
    args.append("--json")
    r = run(args, timeout=120)
    return r.get("json") or {}


def save_consumer_state(state: dict[str, Any]) -> Path:
    out = BUNDLE / "notebooklm_consumer_state.json"
    out.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Σ_APΩ NotebookLM consumer sync")
    parser.add_argument("--no-mind-map", action="store_true", help="Only sync sources, do not regenerate mind map")
    parser.add_argument("--language", default="vi", help="Language for generated mind map")
    parser.add_argument("--out", type=Path, default=BUNDLE, help="Output directory")
    args = parser.parse_args()

    if not shutil.which("notebooklm"):
        print("[error] 'notebooklm' CLI not found. Install with: uv tool install 'notebooklm-py[browser]'", file=sys.stderr)
        return 1

    if not ensure_auth():
        refresh_auth()
    if not ensure_auth():
        print("[error] NotebookLM auth failed. Run: notebooklm login --browser-cookies chrome --include-domains=all", file=sys.stderr)
        return 1

    notebook_id = find_or_create_notebook()
    set_notebook(notebook_id)
    sync = sync_sources(notebook_id)

    mind_map = None
    download = None
    if not args.no_mind_map:
        mind_map = generate_mind_map(notebook_id, language=args.language)
        out_path = args.out / "notebooklm_mindmap_interactive.json"
        download = download_mind_map(notebook_id, out_path)

    state = {
        "notebook_id": notebook_id,
        "notebook_url": f"https://notebooklm.google.com/notebook/{notebook_id}",
        "sync": sync,
        "mind_map": mind_map,
        "download": download,
    }
    state_path = save_consumer_state(state)
    print(json.dumps({**state, "state_file": str(state_path)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
