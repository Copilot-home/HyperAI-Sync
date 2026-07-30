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

"""HyperAI Credential Manager — safe, non-harvesting credential hygiene for local ecosystem.

This script does NOT scan filesystems for keys. It performs defensive audits on known
config surfaces (git remote URLs) and creates `.env.example` templates. Real secrets
must be supplied by the creator through secure channels (macOS Keychain, 1Password,
Bitwarden, or a manually populated `.env` file that is never committed).
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SECURE_CRED_STORE = Path.home() / ".config" / "hyperai" / "credentials.env"
HOME = Path.home()
CRED_LOG = ROOT / "runtime" / "federation_orchestrator" / "credential_manager_audit.json"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _run(cmd: list[str], cwd: Path | None = None, timeout_s: int = 30) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, timeout=timeout_s)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


TOKEN_IN_URL_RE = re.compile(r"https?://[^:@\s]+:([^@\s]+)@")
X_ACCESS_TOKEN_RE = re.compile(r"x-access-token:([^\s@]+)", re.IGNORECASE)


def audit_git_remotes(max_depth: int = 4) -> dict[str, Any]:
    """Audit `.git/config` files under HOME for embedded tokens in remote URLs."""
    leaks: list[dict[str, Any]] = []
    scanned = 0

    try:
        proc = subprocess.run(
            ["find", str(HOME), "-maxdepth", str(max_depth), "-path", "*/.git/config", "-type", "f"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        configs = [Path(p) for p in proc.stdout.splitlines() if p.strip()]
    except Exception as e:
        return {"ok": False, "error": f"find_failed: {e}", "leaks": [], "scanned": 0}

    for cfg in configs:
        scanned += 1
        try:
            cp = configparser.ConfigParser()
            cp.read(cfg, encoding="utf-8")
            for sec in cp.sections():
                if sec.startswith("remote ") and cp.has_option(sec, "url"):
                    url = cp.get(sec, "url")
                    if TOKEN_IN_URL_RE.search(url) or X_ACCESS_TOKEN_RE.search(url):
                        # Do NOT print the token. Redact the URL before storing.
                        redacted = TOKEN_IN_URL_RE.sub(r"https://<TOKEN>@", url)
                        redacted = X_ACCESS_TOKEN_RE.sub(r"x-access-token:<TOKEN>", redacted)
                        leaks.append({
                            "config": str(cfg),
                            "remote": sec[7:-1],
                            "redacted_url": redacted,
                        })
        except Exception:
            continue

    return {"ok": True, "scanned": scanned, "leak_count": len(leaks), "leaks": leaks}


def sanitize_git_remote(repo_dir: Path, remote: str = "origin") -> dict[str, Any]:
    """Set a git remote URL to HTTPS without embedded credentials."""
    cfg_path = repo_dir / ".git" / "config"
    if not cfg_path.exists():
        return {"ok": False, "error": "no_git_config"}
    try:
        cp = configparser.ConfigParser()
        cp.read(cfg_path, encoding="utf-8")
        sec = f"remote \"{remote}\""
        if not cp.has_section(sec) or not cp.has_option(sec, "url"):
            return {"ok": False, "error": f"remote {remote} not found"}
        url = cp.get(sec, "url")
        # Convert https://token@host/owner/repo.git -> https://host/owner/repo.git
        clean = re.sub(r"https?://[^:@\s]+:([^@\s]+)@", r"https://", url)
        clean = re.sub(r"https?://x-access-token:[^@\s]+@", r"https://", clean, flags=re.IGNORECASE)
        if clean == url:
            return {"ok": True, "changed": False, "url": url}
        cp.set(sec, "url", clean)
        with open(cfg_path, "w", encoding="utf-8") as f:
            cp.write(f)
        return {"ok": True, "changed": True, "old_url_redacted": re.sub(r":([^@\s]+)@", r":<TOKEN>@", url), "new_url": clean}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def build_env_templates(target_dirs: list[Path]) -> dict[str, Any]:
    """Create or update `.env.example` templates for target projects."""
    template = (
        "# Environment variables for this project\n"
        "# Copy this file to .env and fill in real values.\n"
        "# NEVER commit .env to Git.\n\n"
        "# GitHub / Git\n"
        "GITHUB_TOKEN=\n"
        "GITHUB_USER=\n"
        "GH_TOKEN=\n\n"
        "# AI Providers\n"
        "OPENAI_API_KEY=\n"
        "ANTHROPIC_API_KEY=\n"
        "GOOGLE_API_KEY=\n"
        "GEMINI_API_KEY=\n\n"
        "# Cloud / Deployment\n"
        "AZURE_OPENAI_API_KEY=\n"
        "AZURE_OPENAI_ENDPOINT=\n"
        "VERCEL_TOKEN=\n"
        "CLOUDFLARE_API_TOKEN=\n\n"
        "# Local / Custom\n"
        "CHROMADB_TOKEN=\n"
        "OLLAMA_BASE_URL=http://127.0.0.1:11434\n"
    )
    created = []
    for d in target_dirs:
        if not d.is_dir():
            continue
        env_example = d / ".env.example"
        if not env_example.exists():
            env_example.write_text(template, encoding="utf-8")
            created.append(str(env_example))
    return {"ok": True, "created": created}


def check_gh_auth() -> dict[str, Any]:
    """Check current gh auth status and report only account names/modes."""
    # If a secure credential store exists, ensure gh uses a valid token instead
    # of a stale or invalid GITHUB_TOKEN that may be present in the environment.
    if SECURE_CRED_STORE.exists():
        try:
            # Try package import first, then same-dir import when run as a script.
            try:
                from tools.hyperai_credentials_loader import load_env_file
            except ImportError:
                from hyperai_credentials_loader import load_env_file
            load_env_file(SECURE_CRED_STORE)
        except Exception:
            pass
    code, out, err = _run(["gh", "auth", "status"])
    text = (out + "\n" + err).strip()
    accounts: list[dict[str, Any]] = []
    current_host: str | None = None
    current_account: dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if line in ("github.com", "gitlab.com") or line.startswith("ghe."):
            current_host = line.split()[0]
            continue
        if line.startswith("- Active account:"):
            active = "true" in line.lower()
            current_account["active"] = active
            # Apply active flag to the most recently added account for this host block.
            if accounts and accounts[-1]["host"] == (current_host or "unknown") and "active" not in accounts[-1]:
                accounts[-1]["active"] = active
            continue
        m = re.search(r"[✓X]\s+.*\baccount\s+(\S+)", line)
        if m:
            current_account = {
                "host": current_host or "unknown",
                "account": m.group(1),
                "status": "logged_in" if line.startswith("✓") else "failed",
                "active": current_account.get("active", False),
            }
            accounts.append(current_account)
            current_account = {}
    return {"ok": code == 0, "accounts": accounts}


def main() -> int:
    parser = argparse.ArgumentParser(description="HyperAI Credential Manager")
    parser.add_argument("--audit", action="store_true", help="Audit git remotes for embedded tokens")
    parser.add_argument("--sanitize-repo", type=Path, help="Sanitize remote URL of a single repo")
    parser.add_argument("--build-env-templates", action="store_true", help="Create .env.example templates for known projects")
    parser.add_argument("--all", action="store_true", help="Run audit + templates + gh status")
    args = parser.parse_args()

    results: dict[str, Any] = {"run_at": _now()}

    if args.audit or args.all:
        results["git_remote_audit"] = audit_git_remotes()

    if args.sanitize_repo:
        results["sanitize"] = sanitize_git_remote(args.sanitize_repo)

    if args.build_env_templates or args.all:
        target_dirs = [
            HOME / "HyperAI-Sync",
            HOME / "HyperAI",
            HOME / "DAIOF-Framework",
            HOME / "tr-gi-p",
            HOME / "my_too_test",
        ]
        results["env_templates"] = build_env_templates(target_dirs)

    if args.all:
        results["gh_auth_status"] = check_gh_auth()

    # Write audit log (redacted)
    CRED_LOG.parent.mkdir(parents=True, exist_ok=True)
    CRED_LOG.write_text(json.dumps(results, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    # Print compact summary without secrets
    summary = {
        "ok": all(v.get("ok", True) for v in results.values() if isinstance(v, dict)),
        "audit_log": str(CRED_LOG),
        "git_leaks_found": results.get("git_remote_audit", {}).get("leak_count", 0),
        "env_templates_created": len(results.get("env_templates", {}).get("created", [])),
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())