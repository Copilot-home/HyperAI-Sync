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
"""Mode A Google Drive sync for the Σ_APΩ NotebookLM bundle.

Uploads / updates the six bounded source documents as Google Docs inside a
shared Drive folder. Uses the active gcloud account and its Drive + Docs OAuth
scope. Call this explicitly; it is never triggered by autopilot.

Prerequisites:
- gcloud installed and authenticated
- gcloud auth has drive scope: gcloud auth login --enable-gdrive-access
- AX_NOTEBOOKLM_DRIVE_ENABLED is set
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import requests


HOME = Path("/Users/andy")
BUNDLE = HOME / ".axcanon" / "memory" / "notebooklm"
DRIVE_MANIFEST = BUNDLE / "drive_manifest.json"
FOLDER_NAME = "HyperAI_NotebookLM"

SOURCE_TITLES = [
    ("01_knowledge_axioms.md", "01 Σ_APΩ Operational Axioms"),
    ("02_knowledge_system.md", "02 Σ_APΩ System Documentation"),
    ("03_connectors_credentials.md", "03 APΩ Credential & Secret Sync"),
    ("04_execution_sleep.md", "04 Σ_APΩ Sleep & Night Watch"),
    ("05_execution_runtime.md", "05 Agent Capsules & Runtime State"),
    ("06_evidence_state.md", "06 Current Runtime Evidence"),
]


def get_token() -> str | None:
    try:
        proc = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        )
        return proc.stdout.strip()
    except Exception as e:
        print(f"[drive] failed to get gcloud token: {e}", file=sys.stderr)
        return None


def drive_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def drive_headers_json(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def find_or_create_folder(token: str, name: str = FOLDER_NAME) -> str:
    q = (
        "mimeType='application/vnd.google-apps.folder' "
        f"and name='{name}' "
        "and trashed=false"
    )
    r = requests.get(
        "https://www.googleapis.com/drive/v3/files",
        headers=drive_headers_json(token),
        params={"q": q, "spaces": "drive", "fields": "files(id,name)"},
    )
    r.raise_for_status()
    files = r.json().get("files", [])
    if files:
        return files[0]["id"]

    r = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        headers=drive_headers_json(token),
        json={"name": name, "mimeType": "application/vnd.google-apps.folder"},
    )
    r.raise_for_status()
    return r.json()["id"]


def find_doc(token: str, folder_id: str, title: str) -> str | None:
    q = (
        "mimeType='application/vnd.google-apps.document' "
        f"and name='{title}' "
        f"and '{folder_id}' in parents "
        "and trashed=false"
    )
    r = requests.get(
        "https://www.googleapis.com/drive/v3/files",
        headers=drive_headers_json(token),
        params={"q": q, "spaces": "drive", "fields": "files(id,name)"},
    )
    r.raise_for_status()
    files = r.json().get("files", [])
    return files[0]["id"] if files else None


def create_doc(token: str, folder_id: str, title: str) -> str:
    r = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        headers=drive_headers_json(token),
        json={
            "name": title,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [folder_id],
        },
    )
    r.raise_for_status()
    return r.json()["id"]


def heading_style(line: str) -> str | None:
    m = re.match(r"^(#{1,6}) ", line)
    if not m:
        return None
    n = len(m.group(1))
    return f"HEADING_{n}"


def parse_markdown_headings(text: str) -> tuple[str, list[tuple[int, str, int]]]:
    """Return cleaned text and list of (start_index, heading_style, line_len) tuples."""
    cleaned_parts: list[str] = []
    headings: list[tuple[int, str, int]] = []  # (start_index, named_style, end_index)
    idx = 1
    for line in text.splitlines(keepends=True):
        newline = "\n" if line.endswith("\n") else ""
        stripped = line.rstrip("\n")
        m = re.match(r"^(#{1,6}) (.*)$", stripped)
        if m:
            style = f"HEADING_{len(m.group(1))}"
            clean_line = m.group(2) + newline
            end = idx + len(m.group(2))
            headings.append((idx, style, end))
        else:
            clean_line = line
        cleaned_parts.append(clean_line)
        idx += len(clean_line)
    return "".join(cleaned_parts), headings


def build_batch_requests(text: str) -> list[dict[str, Any]]:
    clean_text, headings = parse_markdown_headings(text)
    reqs: list[dict[str, Any]] = []
    reqs.append({"insertText": {"location": {"index": 1}, "text": clean_text}})

    for start, style, end in headings:
        reqs.append(
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": style},
                    "fields": "namedStyleType",
                }
            }
        )

    return reqs


def update_doc(token: str, doc_id: str, text: str) -> dict[str, Any]:
    r = requests.get(
        f"https://docs.googleapis.com/v1/documents/{doc_id}",
        headers=drive_headers(token),
    )
    r.raise_for_status()
    doc = r.json()
    end = doc["body"]["content"][-1]["endIndex"]

    reqs: list[dict[str, Any]] = []
    if end > 2:
        reqs.append(
            {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end - 1}}}
        )
    reqs.extend(build_batch_requests(text))

    r = requests.post(
        f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
        headers=drive_headers_json(token),
        json={"requests": reqs},
    )
    r.raise_for_status()
    return r.json()


def sync(token: str | None = None, force: bool = False) -> dict[str, Any]:
    if token is None:
        token = get_token()
    if not token:
        raise RuntimeError("No gcloud access token. Run: gcloud auth login --enable-gdrive-access")

    folder_id = find_or_create_folder(token)
    results: list[dict[str, Any]] = []
    manifest: dict[str, Any] = {
        "folder_id": folder_id,
        "folder_name": FOLDER_NAME,
        "updated_at": _now(),
        "sources": {},
    }

    for md_name, title in SOURCE_TITLES:
        md_path = BUNDLE / md_name
        if not md_path.exists():
            raise FileNotFoundError(md_path)
        text = md_path.read_text(encoding="utf-8")

        doc_id = find_doc(token, folder_id, title)
        if not doc_id:
            doc_id = create_doc(token, folder_id, title)
            created = True
        else:
            created = False

        update_doc(token, doc_id, text)
        results.append({"md_name": md_name, "title": title, "doc_id": doc_id, "created": created})
        manifest["sources"][md_name] = {"title": title, "doc_id": doc_id}

    DRIVE_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"status": "ok", "folder_id": folder_id, "results": results}


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Σ_APΩ NotebookLM bundle to Google Drive")
    parser.add_argument("--force", action="store_true", help="Force sync even if unchanged")
    args = parser.parse_args()

    enabled = os.environ.get("AX_NOTEBOOKLM_DRIVE_ENABLED") or os.environ.get("NOTEBOOKLM_DRIVE_ENABLED")
    if not enabled:
        print(
            "[error] Mode A sync disabled. Set AX_NOTEBOOKLM_DRIVE_ENABLED=1 and run again.",
            file=sys.stderr,
        )
        return 1

    try:
        summary = sync(force=args.force)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
