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
"""Mode B: Gemini Notebook Enterprise API (discoveryengine.googleapis.com).

Requires a Gemini Notebook Enterprise license.
Does nothing until AX_NOTEBOOKLM_ENTERPRISE_ENABLED is set and the project has a
valid SUBSCRIPTION_TIER_NOTEBOOK_LM license.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import requests


PROJECT_NUMBER = "171781820082"
ENDPOINT = "us"
LOCATION = "us"
BASE_URL = f"https://{ENDPOINT}-discoveryengine.googleapis.com/v1alpha/projects/{PROJECT_NUMBER}/locations/{LOCATION}"


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
        print(f"[enterprise] failed to get gcloud token: {e}", file=sys.stderr)
        return None


def headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def check_license(token: str) -> dict[str, Any]:
    """Probe the API; return ok or license error."""
    url = f"{BASE_URL}/notebooks:listRecentlyViewed"
    r = requests.get(url, headers=headers(token))
    if r.status_code == 200:
        return {"ok": True, "notebooks": r.json().get("notebooks", [])}
    err = r.json().get("error", {})
    return {"ok": False, "code": err.get("code"), "status": err.get("status"), "message": err.get("message")}


def create_notebook(token: str, title: str = "Σ_APΩ") -> dict[str, Any]:
    url = f"{BASE_URL}/notebooks"
    r = requests.post(url, headers=headers(token), json={"title": title})
    if r.status_code != 200:
        return {"ok": False, "error": r.json()}
    return {"ok": True, "notebook": r.json()}


def add_source(token: str, notebook_id: str, source_title: str, drive_doc_id: str) -> dict[str, Any]:
    url = f"{BASE_URL}/notebooks/{notebook_id}/sources"
    body = {
        "displayName": source_title,
        "driveSource": {"driveDocumentId": drive_doc_id},
    }
    r = requests.post(url, headers=headers(token), json=body)
    if r.status_code != 200:
        return {"ok": False, "error": r.json()}
    return {"ok": True, "source": r.json()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Σ_APΩ NotebookLM Enterprise Mode B scaffold")
    parser.add_argument("--check", action="store_true", help="Check license")
    parser.add_argument("--create", action="store_true", help="Create notebook and add 6 sources")
    args = parser.parse_args()

    if not os.environ.get("AX_NOTEBOOKLM_ENTERPRISE_ENABLED"):
        print("[error] AX_NOTEBOOKLM_ENTERPRISE_ENABLED not set.", file=sys.stderr)
        return 1

    token = get_token()
    if not token:
        return 1

    if args.check:
        print(json.dumps(check_license(token), indent=2, ensure_ascii=False))
        return 0

    if args.create:
        lic = check_license(token)
        if not lic["ok"]:
            print(json.dumps(lic, indent=2, ensure_ascii=False), file=sys.stderr)
            return 1
        nb = create_notebook(token)
        print(json.dumps(nb, indent=2, ensure_ascii=False))
        if not nb["ok"]:
            return 1
        notebook_id = nb["notebook"]["notebookId"]
        manifest_path = Path("/Users/andy/.axcanon/memory/notebooklm/drive_manifest.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
        results = []
        for md_name, info in manifest.get("sources", {}).items():
            res = add_source(token, notebook_id, info["title"], info["doc_id"])
            results.append({"md_name": md_name, **res})
        print(json.dumps({"notebook_id": notebook_id, "sources": results}, indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
