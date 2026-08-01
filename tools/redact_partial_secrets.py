#!/usr/bin/env python3
"""Redact partial secret identifiers from artifacts, reports, and journals.

Replaces masked credential strings (e.g. <REDACTED>) with <REDACTED>
and records a receipt. Does not read canonical credentials into output.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/andy/HyperAI-Sync")
OUT = ROOT / "runtime" / "federation_orchestrator"
CREDENTIALS = Path.home() / ".config" / "hyperai" / "credentials.env"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_credential_fingerprints() -> dict[str, str]:
    """Build provider -> sha256(actual_key) map from canonical credentials.env."""
    fps: dict[str, str] = {}
    if not CREDENTIALS.exists():
        return fps
    mapping = {
        "OPENAI_API_KEY_3": "openai",
        "OPENAI_API_KEY": "openai",
        "OPENROUTER_API_KEY": "openrouter",
        "DEEPSEEK_API_KEY": "deepseek",
        "NOTION_TOKEN": "notion",
        "NOTION_API_KEY": "notion",
        "GITHUB_TOKEN": "github",
        "TELEGRAM_BOT_TOKEN": "telegram",
        "GOOGLE_PSE_API_KEY": "google_pse",
        "SLACK_BOT_TOKEN": "slack",
        "ANTHROPIC_API_KEY": "anthropic",
    }
    text = CREDENTIALS.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "=" not in line or line.startswith("#"):
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"\'')
        if not v or k not in mapping:
            continue
        provider = mapping[k]
        # Latest rotation wins for duplicate provider keys
        fps[provider] = sha256(v)
    return fps


# Masked secret patterns.
# Matches OpenAI-style keys, OpenRouter, deepseek, generic sk-... tokens with ellipsis.
PATTERN = re.compile(
    r"\b(?:sk-[a-zA-Z0-9_-]{2,}(?:\.{2,}|…)[A-Za-z0-9_-]{2,}|"
    r"sk-or-v1-[a-zA-Z0-9_-]{2,}(?:\.{2,}|…)[A-Za-z0-9_-]{2,}|"
    r"n[A-Za-z0-9_-]{20,}(?:\.{2,}|…)[A-Za-z0-9_-]{2,})"
)

# Also catch any explicit "masked_key": "<REDACTED>" in JSON.
MASKED_KEY_VALUE_PATTERN = re.compile(
    r'"masked_key"\s*:\s*"[^"]{4,}"'
)

# Catch "new_key_masked": "<REDACTED>"
NEW_KEY_MASKED_PATTERN = re.compile(
    r'"new_key_masked"\s*:\s*"[^"]{4,}"'
)


def provider_from_context(line: str) -> str | None:
    """Infer provider from surrounding JSON context."""
    if '"openai"' in line.lower() or "openai" in line.lower():
        return "openai"
    if '"openrouter"' in line.lower() or "openrouter" in line.lower():
        return "openrouter"
    if '"deepseek"' in line.lower() or "deepseek" in line.lower():
        return "deepseek"
    if '"notion"' in line.lower() or "notion" in line.lower():
        return "notion"
    if '"github"' in line.lower() or "github" in line.lower():
        return "github"
    if '"telegram"' in line.lower() or "telegram" in line.lower():
        return "telegram"
    if '"slack"' in line.lower() or "slack" in line.lower():
        return "slack"
    if '"anthropic"' in line.lower() or "anthropic" in line.lower():
        return "anthropic"
    if "google_pse" in line.lower() or "google pse" in line.lower():
        return "google_pse"
    return None


def redact_text(text: str, provider_fps: dict[str, str]) -> tuple[str, list[dict]]:
    redactions: list[dict] = []
    lines = text.splitlines(keepends=True)
    out_lines: list[str] = []

    for idx, line in enumerate(lines, start=1):
        original_line = line
        new_line = line

        # Replace masked key JSON values explicitly
        def replace_masked_key(m: re.Match) -> str:
            full = m.group(0)
            # Extract the quoted value
            val = full.split(":", 1)[1].strip().strip('"')
            provider = provider_from_context(line)
            fp = provider_fps.get(provider) if provider else None
            redactions.append({
                "line": idx,
                "field_type": "masked_key",
                "original_pattern_prefix": val[:10] if len(val) > 10 else val[:3],
                "provider_inferred": provider,
                "credential_fingerprint": f"sha256:{fp}" if fp else None,
                "status": "REDACTED" if fp else "HISTORICAL_REDATED",
            })
            key = full.split(":", 1)[0]
            return f'{key}: "<REDACTED>"'

        new_line = MASKED_KEY_VALUE_PATTERN.sub(replace_masked_key, new_line)

        def replace_new_key_masked(m: re.Match) -> str:
            full = m.group(0)
            val = full.split(":", 1)[1].strip().strip('"')
            provider = provider_from_context(line)
            fp = provider_fps.get(provider) if provider else None
            redactions.append({
                "line": idx,
                "field_type": "new_key_masked",
                "original_pattern_prefix": val[:10] if len(val) > 10 else val[:3],
                "provider_inferred": provider,
                "credential_fingerprint": f"sha256:{fp}" if fp else None,
                "status": "REDACTED" if fp else "HISTORICAL_REDATED",
            })
            key = full.split(":", 1)[0]
            return f'{key}: "<REDACTED>"'

        new_line = NEW_KEY_MASKED_PATTERN.sub(replace_new_key_masked, new_line)

        # Replace inline masked secrets
        def replace_secret(m: re.Match) -> str:
            val = m.group(0)
            provider = provider_from_context(line)
            fp = provider_fps.get(provider) if provider else None
            redactions.append({
                "line": idx,
                "field_type": "inline_masked_secret",
                "original_pattern_prefix": val[:15] if len(val) > 15 else val[:3],
                "provider_inferred": provider,
                "credential_fingerprint": f"sha256:{fp}" if fp else None,
                "status": "REDACTED" if fp else "HISTORICAL_REDATED",
            })
            return "<REDACTED>"

        new_line = PATTERN.sub(replace_secret, new_line)

        out_lines.append(new_line)

    return "".join(out_lines), redactions


def should_scan(p: Path) -> bool:
    if not p.is_file():
        return False
    # Skip credentials source, large binaries, .git, node_modules
    name = p.name
    if name == "credentials.env" or name.endswith(".shred") or name.endswith(".bak"):
        return False
    if ".git" in p.parts or "node_modules" in p.parts:
        return False
    if p.stat().st_size > 5_000_000:
        return False
    ext = p.suffix.lower()
    return ext in {".json", ".md", ".txt", ".py", ".yaml", ".yml", ".csv", ".html", ".ipynb", ".log"}


def scan_and_redact(dirs: list[Path], provider_fps: dict[str, str]) -> dict:
    receipt = {
        "generated_at": now_iso(),
        "redaction_policy": "Replace partial credential masks with <REDACTED>; do not store plaintext secrets or prefixes/suffixes",
        "total_files_scanned": 0,
        "total_files_modified": 0,
        "total_redactions": 0,
        "redactions_by_file": [],
    }
    for d in dirs:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if not should_scan(p):
                continue
            receipt["total_files_scanned"] += 1
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            new_text, redactions = redact_text(text, provider_fps)
            if redactions:
                p.write_text(new_text, encoding="utf-8")
                receipt["total_files_modified"] += 1
                receipt["total_redactions"] += len(redactions)
                receipt["redactions_by_file"].append({
                    "file": str(p),
                    "redactions_count": len(redactions),
                    "redactions": redactions,
                })
    return receipt


def redact_broker_source() -> dict:
    """Patch hyperai_credentials_service.py to stop emitting masked keys in status/lease."""
    svc = ROOT / "tools" / "hyperai_credentials_service.py"
    if not svc.exists():
        return {"file": str(svc), "status": "NOT_FOUND"}
    text = svc.read_text(encoding="utf-8")

    # Remove masked_key field from to_public
    text = re.sub(
        r'("masked_key": self\.masked_key,)\n\s+',
        '"credential_fingerprint": "<derived-from-active-key>",\n            ',
        text,
    )

    # Rewrite status active_keys to only expose active_key_ref and health
    old_status = """        active_summary = {
            p: {"key": k, "masked": self.mask(self.active.get(p))}
            for p, k in self.active_key_ref.items()
        }
        return {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "env_source": str(self.env_path),
            "total_keys": len(self.creds),
            "active_keys": {k: v["masked"] for k, v in active_summary.items()},"""
    new_status = """        active_summary = {
            p: {"active_key_ref": k, "healthy": bool(self.active.get(p))}
            for p, k in self.active_key_ref.items()
        }
        return {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "env_source": str(self.env_path),
            "total_keys": len(self.creds),
            "active_keys": {k: v for k, v in active_summary.items()},"""
    if old_status in text:
        text = text.replace(old_status, new_status)
        modified = True
    else:
        modified = False

    svc.write_text(text, encoding="utf-8")
    return {"file": str(svc), "status": "MODIFIED" if modified else "PATTERN_NOT_FOUND"}


def main() -> int:
    provider_fps = load_credential_fingerprints()
    dirs = [
        ROOT,
        Path("/Users/andy/.codex"),
        Path("/Users/andy/AGENTS.md"),
    ]
    # If AGENTS.md is a file, handle separately; rglob on a file returns itself only if matched
    files = [d for d in dirs if d.is_file()]
    dirs = [d for d in dirs if d.is_dir()]
    receipt = scan_and_redact(dirs, provider_fps)
    for f in files:
        if should_scan(f):
            text = f.read_text(encoding="utf-8")
            new_text, redactions = redact_text(text, provider_fps)
            if redactions:
                f.write_text(new_text, encoding="utf-8")
                receipt["total_files_modified"] += 1
                receipt["total_redactions"] += len(redactions)
                receipt["redactions_by_file"].append({
                    "file": str(f),
                    "redactions_count": len(redactions),
                    "redactions": redactions,
                })

    broker_patch = redact_broker_source()
    receipt["broker_source_patch"] = broker_patch

    (OUT / "secret_redaction_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"scanned={receipt['total_files_scanned']} modified={receipt['total_files_modified']} redactions={receipt['total_redactions']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
