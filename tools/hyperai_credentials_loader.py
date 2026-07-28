#!/usr/bin/env python3
"""Load and manage the central AI-ecosystem credential dump.

This tool reads Andy's credential master file and produces a clean,
gitignored `.env.credentials` file. It never prints secret values.
"""

from __future__ import annotations

import base64
import os
import re
import shlex
import zlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "# QUẢN LÝ CREDENTIALS - HỆ THỐNG AI CỦA NGUYỄN ĐỨC CƯỜNG" / "# QUẢN LÝ CREDENTIALS - HỆ THỐNG AI CỦA NGUYỄN ĐỨC CƯỜNG.md"
# Keep secrets outside the project tree; the credential file is loaded from the user config dir.
DEFAULT_OUT = Path.home() / ".config" / "hyperai" / "credentials.env"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


SECTIONS: dict[str, str] = {
    "openai": "OPENAI",
    "anthropic": "ANTHROPIC",
    "claude": "ANTHROPIC",
    "gemini": "GEMINI",
    "google gemini": "GEMINI",
    "các llm khác": "LLM_OTHERS",
    "telegram bots": "TELEGRAM",
    "database": "DATABASE",
    "github": "GITHUB",
    "docker": "DOCKER",
    "monitoring & observability": "MONITORING",
    "grafana": "MONITORING",
    "sentry": "MONITORING",
    "axiom": "MONITORING",
    "other services": "SERVICES",
    "redis": "REDIS",
    "local services": "REDIS",
    "ssh keys": "SSH",
    "recovery": "ACCOUNT",
    "misc / encoded data": "MISC",
    "misc": "MISC",
    "hướng dẫn sử dụng": "INSTRUCTIONS",
}

# If a parsed key exactly matches one of these, use the alias instead.
KEY_ALIASES: dict[str, str] = {
    "BET": "BET_WEBHOOK_SECRET",
    "LMSTUDIO": "LMSTUDIO_API_KEY",
    "MISTRAL_API_KEY": "MISTRAL_API_KEY",  # identity, ensures tab stripped
    "FIREWALL_IS_ENABLED_STATE": None,  # drop
    "HTTPS": None,  # ambiguous, drop; correct keys are remapped below
}


def _clean_key(raw: str) -> str:
    """Turn a raw label into a safe env-var key."""
    raw = raw.strip()
    raw = re.sub(r"^#+\s*", "", raw)
    raw = re.sub(r"\*+", "", raw)
    raw = re.sub(r"[^A-Za-z0-9_ ]+", " ", raw)
    raw = re.sub(r"\s+", "_", raw.strip())
    key = raw.upper().rstrip("_")
    if key and key[0].isdigit():
        key = "_" + key
    return key


def _clean_value(raw: str) -> str:
    """Strip surrounding quotes, shell operators, markdown, and trailing whitespace.

    Also removes a lone leading/trailing quote that is not paired (handles
    malformed source like `KEY='value` or `KEY=value'`).
    """
    raw = raw.strip()
    # Surrounding matching quotes
    if (raw.startswith("'") and raw.endswith("'")) or (raw.startswith('"') and raw.endswith('"')):
        raw = raw[1:-1]
    else:
        # Malformed source: a single leading or trailing quote
        if raw.startswith("'") or raw.startswith('"'):
            raw = raw[1:]
        if raw.endswith("'") or raw.endswith('"'):
            raw = raw[:-1]
    # Strip surrounding markdown bold markers
    raw = re.sub(r"^\*+|\*+$", "", raw)
    # Drop shell trailing like `&& export ...`
    raw = re.split(r"\s+&&\s+", raw, maxsplit=1)[0]
    raw = re.split(r"\s+\|\|\s+", raw, maxsplit=1)[0]
    # Drop trailing markdown and comments
    raw = raw.split("  ", 1)[0].split("#", 1)[0].strip()
    return raw


def _sanitize_token_value(key: str, value: str) -> str:
    """If a token-like value contains trailing text, extract the first clean token."""
    if not value:
        return value
    token_suffixes = ("_API_KEY", "_TOKEN", "_SECRET", "_PAT", "_DSN", "_AUTH_TOKEN", "_PASSWORD")
    description_keys = ("DESCRIPTION", "LABEL", "EXPIRES", "URL", "LINK", "FREQUENCY", "ARCH",
                          "ADDED", "FINGERPRINT", "BIND_ADDR", "PUBLIC_KEY", "ACCOUNT", "RECOVERY")
    if any(d in key for d in description_keys):
        return value
    if not key.upper().endswith(token_suffixes):
        return value
    # If the value already has no spaces/newlines, it's clean
    if re.fullmatch(r"\S+", value):
        return value
    # Try to extract first plausible token segment
    first = value.split()[0]
    # Telegram bot token: digits:alphanum
    if re.fullmatch(r"\d+:[A-Za-z0-9_-]{30,}", first):
        return first
    # Generic token-ish first segment (alphanum + - _)
    if re.fullmatch(r"[A-Za-z0-9_\-=:+./]+", first) and len(first) > 20:
        return first
    return value


def _find_section(line: str) -> str | None:
    lowered = line.lower()
    for marker, section in SECTIONS.items():
        if marker in lowered:
            return section
    return None


def _looks_like_secret(value: str) -> bool:
    """Heuristic: a value is a secret if it is reasonably long and not plain boolean/number."""
    value = value.strip()
    if not value or len(value) < 6:
        return False
    if value in ("true", "false", "True", "False", "0", "1"):
        return False
    return True


def _remap_https_line(key: str, value: str, section: str | None) -> tuple[str, str] | None:
    """Remap lines like https://webhook.sh=whsec_... to correct env keys."""
    if key.lower().startswith("https://webhook") and value.startswith("whsec_"):
        return ("OPENAI_WEBHOOK_SECRET" if section == "OPENAI" else "BET_WEBHOOK_SECRET", value)
    if key.lower().startswith("https://withpersona") and "inquiry-id=" in key.lower():
        inquiry = re.search(r"inquiry-id=([A-Za-z0-9_\-]+)", key)
        if inquiry:
            return ("OPENAI_PERSONA_INQUIRY_ID", inquiry.group(1))
    return None


def _guess_key_from_token(token: str, section: str | None) -> str | None:
    """Return a canonical env key for a bare token based on its prefix."""
    token = token.strip()
    if not token:
        return None

    if section == "GITHUB" or token.startswith(("ghp_", "github_pat_")):
        if token.startswith("ghp_"):
            return "GITHUB_PAT"
        if token.startswith("github_pat_"):
            return "GITHUB_PAT"

    if token.startswith("sk-admin-"):
        return "OPENAI_ADMIN_KEY"
    if token.startswith("sk-proj-"):
        return "OPENAI_API_KEY"
    if token.startswith("sk-ant-admin01-") or token.startswith("sk-ant-"):
        return "CLAUDE_ADMIN_KEY"
    if token.startswith("sk-or-v1-"):
        return "OPENROUTER_API_KEY"
    if token.startswith("sk_e") and len(token) > 20:
        return "CLINE_API_KEY"
    if token.startswith("sk-lm-"):
        return "LMSTUDIO_API_KEY"
    if re.fullmatch(r"sk-58[0-9a-z]{30,}", token):
        return "DEEPSEEK_API_KEY"

    if re.fullmatch(r"\d{5,20}:AA[0-9A-Za-z_-]{30,}", token):
        return "TELEGRAM_BOT_TOKEN"
    if token.startswith("AIza"):
        return "GEMINI_API_KEY"
    if token.startswith("dckr_oat_"):
        return "DOCKER_ORG_ACCESS_TOKEN"
    if token.startswith("ntn_"):
        return "NOTION_API_KEY"
    if token.startswith("PMAK-"):
        return "POSTMAN_API_KEY"
    if token.startswith("lin_api_"):
        return "LINEAR_API_KEY"
    if token.startswith("vcp_"):
        return "VERCEL_TOKEN"
    if token.startswith("ls-"):
        return "LOCALSTACK_AUTH_TOKEN"
    if token.startswith("xaat-"):
        return "AXIOM_MCP_TOKEN"
    if token.startswith("sntry"):
        return "SENTRY_DSN"
    if token.startswith("glc_"):
        return "GCLOUD_RW_API_KEY"
    if token.startswith("whsec_"):
        return "BET_WEBHOOK_SECRET" if section == "ACCOUNT" or section == "MISC" else "OPENAI_WEBHOOK_SECRET"
    if token.startswith("ctx7sk-"):
        return "CONTEXT7_API_KEY"
    if token.startswith("apk_user_"):
        return "DEVIN_API_KEY"
    if token.startswith("xai-"):
        return "XAI_API_KEY"
    if token.startswith("org-"):
        return "OPENAI_ORGANIZATION_ID"
    if token.startswith("dop_v") or token.startswith("dop_"):
        return "DIGITALOCEAN_TOKEN"

    return None


def _decode_misc(encoded: str) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        raw = zlib.decompress(base64.b64decode(encoded))
        data = raw.decode("utf-8")
        if data.startswith("{"):
            obj = _loose_json(data)
            for k, v in obj.items():
                out[f"MISC_{k.upper()}"] = str(v)
        out["MISC_DECODED_RAW"] = data
    except Exception:
        out["MISC_DECODE_ERROR"] = "true"
    return out


def _loose_json(text: str) -> dict[str, Any]:
    import json
    try:
        return json.loads(text)
    except Exception:
        return {}


def _extract_kv_assignments(text: str, section: str | None) -> dict[str, str]:
    """Extract KEY=VALUE pairs, handling export chains and quoted values."""
    out: dict[str, str] = {}
    # Split shell chains like `KEY=v && export KEY2='v2' && export KEY3="v3"`
    parts = re.split(r"\s*&&\s*", text)
    for part in parts:
        part = re.sub(r"^\s*export\s+", "", part).strip()
        if "=" not in part:
            continue
        raw_key, val = part.split("=", 1)
        # Remap https://...=token lines before normalizing the key
        remapped = _remap_https_line(raw_key.strip(), val.strip(), section)
        if remapped:
            key, val = remapped
        else:
            key = _clean_key(raw_key)
        val = _clean_value(val)
        if not key or not val:
            continue
        if key in KEY_ALIASES:
            alias = KEY_ALIASES[key]
            if alias is None:
                continue
            key = alias

        if _looks_like_secret(val):
            val = _sanitize_token_value(key, val)
            out[key] = val
    return out


def parse_credential_file(path: Path) -> dict[str, str]:
    """Parse the messy markdown credential dump into a clean KEY=VALUE dict."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # Split concatenated tokens/URLs that are glued together on one line
    text = re.sub(r"(?<=[A-Za-z0-9_-])(?=https?://)", "\n", text)
    lines = text.splitlines()

    current_section: str | None = None
    explicit: dict[str, str] = {}
    bare_tokens: list[tuple[str | None, str]] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Section detection
        if stripped.startswith("#") or re.match(r"^\d+\.\s+", stripped):
            sec = _find_section(stripped)
            if sec:
                current_section = sec
            continue

        handled = False

        # Multi-value env line: GCLOUD_...="..." GCLOUD_...="..."
        if '="' in stripped and stripped.count("=") > 1 and not stripped.startswith("-"):
            pairs = re.findall(r'([A-Z_][A-Z0-9_]*)\s*=\s*"([^"]*)"', stripped)
            if len(pairs) > 1:
                for k, v in pairs:
                    ck = _clean_key(k)
                    if ck in KEY_ALIASES:
                        alias = KEY_ALIASES[ck]
                        if alias is None:
                            continue
                        ck = alias
                    explicit[ck] = v
                handled = True

        # Azure / general quoted/unquoted KEY="value" or KEY=value assignments on one line
        if not handled and "=" in stripped and not stripped.startswith(("-", "*", "|", "`")):
            kv = _extract_kv_assignments(stripped, current_section)
            explicit.update(kv)

        # RapidAPI key line: `x-rapidapi-key: c95cd...`
        m = re.search(r"x-rapidapi-key[:\s=]+([0-9a-z]{40,})", stripped, re.IGNORECASE)
        if m:
            explicit["RAPIDAPI_KEY"] = m.group(1)
            continue

        # Decode MISC_ENCODED_DATA if present
        if "MISC_ENCODED_DATA" in stripped:
            m = re.search(r"MISC_ENCODED_DATA\s*=\s*([A-Za-z0-9+/=]+)", stripped)
            if m:
                explicit["MISC_ENCODED_DATA"] = m.group(1)
            continue

        # Bare token extraction (only if not already captured)
        seen_values = set(explicit.values())
        token_candidates: set[str] = set()
        token_candidates.update(re.findall(r"\b(ghp_[A-Za-z0-9_]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(github_pat_[A-Za-z0-9_]{60,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk-admin-[A-Za-z0-9_-]{50,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk-proj-[A-Za-z0-9_-]{100,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk-ant-admin01-[A-Za-z0-9_-]{80,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk-or-v1-[A-Za-z0-9_-]{50,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk_[A-Za-z0-9]{40,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk-lm-[A-Za-z0-9_:.-]{20,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sk-58[0-9a-z]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(dckr_oat_[A-Za-z0-9_]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(ntn_[A-Za-z0-9_]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(PMAK-[A-Za-z0-9-]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(lin_api_[A-Za-z0-9_]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(vcp_[A-Za-z0-9_]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(ls-[A-Za-z0-9-]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(xaat-[0-9a-f-]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(sntry[u]?_[A-Za-z0-9_]{50,})\b", stripped))
        token_candidates.update(re.findall(r"\b(glc_[A-Za-z0-9_=\-]{100,})(?=\s|$|[,;])", stripped))
        token_candidates.update(re.findall(r"\b(whsec_[A-Za-z0-9_=\-]{30,})(?=\s|$|[,;])", stripped))
        token_candidates.update(re.findall(r"\b(ctx7sk-[0-9a-f-]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(apk_user_[A-Za-z0-9+/=]{50,})\b", stripped))
        token_candidates.update(re.findall(r"\b(xai-[A-Za-z0-9_-]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(org-[A-Za-z0-9]{10,})\b", stripped))
        token_candidates.update(re.findall(r"\b(\d{5,20}:AA[0-9A-Za-z_-]{30,})\b", stripped))
        token_candidates.update(re.findall(r"\b(AIza[0-9A-Za-z_-]{30,})\b", stripped))

        for tok in token_candidates:
            if tok in seen_values:
                continue
            bare_tokens.append((current_section, tok))

    # Post-process: rename keys when the value makes it obvious, drop noise,
    # remap glued HTTPS URLs, and deduplicate exact values.
    renamed: dict[str, str] = {}
    for k, v in explicit.items():
        if v.startswith("sk-admin-"):
            renamed.setdefault("OPENAI_ADMIN_KEY", v)
            continue
        if v.startswith("org-"):
            renamed.setdefault("OPENAI_ORGANIZATION_ID", v)
            continue
        if v.startswith("whsec_") and current_section == "OPENAI":
            renamed.setdefault("OPENAI_WEBHOOK_SECRET", v)
            continue
        if v.startswith("whsec_") and (k == "BET" or k == "BET_WEBHOOK_SECRET"):
            renamed.setdefault("BET_WEBHOOK_SECRET", v)
            continue
        if k.startswith("HTTPS_") or k.startswith("HTTP_"):
            if v.startswith("whsec_"):
                renamed.setdefault("OPENAI_WEBHOOK_SECRET", v)
            elif v.startswith("inq_"):
                renamed.setdefault("OPENAI_PERSONA_INQUIRY_ID", v)
            continue
        if "PERMISSIONS" in k or "ADMINISTRATION_API" in k or "READ_ALL" in k or "VERIFY_BUSINESS" in k:
            # These are noise keys from the glued OpenAI header line
            continue
        if k in KEY_ALIASES:
            alias = KEY_ALIASES[k]
            if alias is None:
                continue
            k = alias
        renamed.setdefault(k, v)

    # Deduplicate with suffixes
    final: dict[str, str] = {}
    counts: dict[str, int] = defaultdict(int)

    def _add(key: str, value: str) -> None:
        if not key or not value:
            return
        if key in final:
            if final[key] == value:
                return
            counts[key] += 1
            key = f"{key}_ALT{counts[key]}"
        final[key] = value

    for k, v in renamed.items():
        _add(k, v)

    for section, tok in bare_tokens:
        if tok in final.values():
            continue
        guessed = _guess_key_from_token(tok, section)
        if guessed:
            _add(guessed, tok)
        else:
            _add(f"{section or 'UNKNOWN'}_TOKEN" if section else "UNKNOWN_TOKEN", tok)

    if "MISC_ENCODED_DATA" in final:
        decoded = _decode_misc(final["MISC_ENCODED_DATA"])
        del final["MISC_ENCODED_DATA"]
        for k, v in decoded.items():
            _add(k, v)

    # Final deduplication: exact same secret value under multiple keys
    # keeps only the first (alphabetically) canonical key.
    seen_values: set[str] = set()
    deduped: dict[str, str] = {}
    for key in sorted(final):
        value = final[key]
        if value in seen_values:
            continue
        seen_values.add(value)
        deduped[key] = value

    return deduped


def write_env_file(creds: dict[str, str], out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lines = [
        "# HyperAI ecosystem credentials",
        f"# Generated from central credential dump at {_now()}",
        "# DO NOT COMMIT. This file is gitignored via .gitignore.",
        "# Load with: python tools/hyperai_credentials_loader.py --load",
        "",
    ]
    for key in sorted(creds):
        value = creds[key]
        # shlex.quote produces a shell-safe word (single-quoted if needed),
        # preventing syntax errors from parentheses, brackets, dollar signs, etc.
        lines.append(f"{key}={shlex.quote(value)}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(out_path, 0o600)
    return out_path


def load_env_file(path: Path | None = None) -> dict[str, str]:
    path = path or DEFAULT_OUT
    if not path.exists():
        raise FileNotFoundError(path)
    creds: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        val = val.strip()
        # Use shlex to safely unquote shell-quoted values, including those
        # with parentheses, brackets, dollar signs, or embedded quotes.
        try:
            parts = shlex.split(val)
            if parts:
                val = parts[0]
        except ValueError:
            pass
        creds[key] = val
        os.environ[key] = val
    # Expose the active GitHub PAT under the two env aliases used by gh/git and libraries.
    if "GITHUB_PAT" in creds:
        for alias in ("GH_TOKEN", "GITHUB_TOKEN"):
            os.environ[alias] = creds["GITHUB_PAT"]
    return creds


def summary(creds: dict[str, str]) -> dict[str, Any]:
    groups: dict[str, list[str]] = defaultdict(list)
    for k in creds:
        prefix = k.split("_")[0]
        groups[prefix].append(k)
    return {
        "total_keys": len(creds),
        "groups": {g: len(v) for g, v in groups.items()},
        "sample_keys": sorted(creds.keys())[:30],
    }


def main() -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="HyperAI credential loader")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Source markdown file")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output .env file")
    parser.add_argument("--load", action="store_true", help="Load .env.credentials into os.environ")
    parser.add_argument("--summary", action="store_true", help="Print safe summary")
    args = parser.parse_args()

    if args.load:
        creds = load_env_file(args.out)
        if args.summary:
            print(json.dumps(summary(creds), ensure_ascii=True, indent=2))
        return 0

    if not args.source.exists():
        print(f"Source not found: {args.source}")
        return 1

    creds = parse_credential_file(args.source)
    write_env_file(creds, args.out)
    if args.summary:
        print(json.dumps(summary(creds), ensure_ascii=True, indent=2))
    else:
        print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
