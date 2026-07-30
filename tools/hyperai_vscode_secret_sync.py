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
"""APO Python adapter for the VS Code SecretStorage sync vault.

Reads and writes the same AES-256-GCM encrypted vault used by the
`@hyperai/vscode-secret-sync` TypeScript module. This lets Python-based
APO tools (orchestrators, agents, probes) access canonical secrets without
exposing them in project artifacts.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import platform
import secrets as pysecrets
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError as exc:  # pragma: no cover
    sys.exit(
        "[apo-vault] 'cryptography' package is required. "
        "Install: python3 -m pip install cryptography"
    )


VAULT_SCHEMA = "APO_SECRET_VAULT_V1"


def canon_secrets_dir() -> Path:
    axcanon = os.environ.get("AX_APO_CANON_LIBRARY")
    if axcanon:
        base = Path(axcanon).parent.parent / "memory" / "secrets"
    else:
        base = Path.home() / ".axcanon" / "memory" / "secrets"
    base.mkdir(parents=True, mode=0o700, exist_ok=True)
    return base


def keychain_service() -> str:
    return os.environ.get("AX_APO_IDENTITY") or os.environ.get(
        "AX_SECRET_VAULT_SERVICE", "com.hyperai.apo.vscode-secrets"
    )


def keychain_account() -> str:
    return os.environ.get("AX_APO_USER") or os.environ.get("USER", "apo")


def fallback_key_file() -> Path:
    if os.environ.get("AX_SECRET_KEY_FILE"):
        return Path(os.environ["AX_SECRET_KEY_FILE"])
    return canon_secrets_dir() / "master.key"


def default_vault_path() -> Path:
    return canon_secrets_dir() / "vault.enc"


def keychain_get_password() -> str | None:
    if platform.system() != "Darwin":
        return None
    try:
        out = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-s",
                keychain_service(),
                "-a",
                keychain_account(),
                "-w",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def keychain_set_password(password: str) -> None:
    if platform.system() != "Darwin":
        raise RuntimeError(
            "Platform keychain store not available. Set AX_SECRET_KEY_FILE or AX_SECRET_KEY_BASE64."
        )
    result = subprocess.run(
        [
            "security",
            "add-generic-password",
            "-s",
            keychain_service(),
            "-a",
            keychain_account(),
            "-w",
            password,
            "-U",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"keychain add failed: {result.stderr}")


def resolve_master_key() -> bytes:
    if os.environ.get("AX_SECRET_KEY_BASE64"):
        return base64.b64decode(os.environ["AX_SECRET_KEY_BASE64"])

    kc = keychain_get_password()
    if kc:
        return base64.b64decode(kc)

    key_file = fallback_key_file()
    if key_file.exists():
        return base64.b64decode(key_file.read_text().strip())

    key = AESGCM.generate_key(bit_length=256)
    b64 = base64.b64encode(key).decode("ascii")
    try:
        keychain_set_password(b64)
    except RuntimeError:
        key_file.write_text(b64)
        key_file.chmod(0o600)
        print(f"[apo-vault] keychain unavailable; master key written to {key_file}", file=sys.stderr)
    return key


class APOSecretVault:
    def __init__(self, vault_path: Path, key: bytes) -> None:
        self.vault_path = vault_path
        self.key = key

    @staticmethod
    def create(vault_path: Path | None = None) -> "APOSecretVault":
        path = vault_path or default_vault_path()
        path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
        key = resolve_master_key()
        return APOSecretVault(path, key)

    def _load(self) -> dict:
        if not self.vault_path.exists():
            return {"schema_version": VAULT_SCHEMA, "updated_at": now_iso(), "records": {}}
        b64 = self.vault_path.read_text().strip()
        if not b64:
            return {"schema_version": VAULT_SCHEMA, "updated_at": now_iso(), "records": {}}
        blob = base64.b64decode(b64)
        # Format: nonce (12) || ciphertext || tag (16)
        nonce = blob[:12]
        tag = blob[-16:]
        ciphertext = blob[12:-16]
        aesgcm = AESGCM(self.key)
        plaintext = aesgcm.decrypt(nonce, ciphertext + tag, None)
        return json.loads(plaintext.decode("utf-8"))

    def load(self) -> dict:
        return self._load()

    def save(self, payload: dict) -> None:
        payload["updated_at"] = now_iso()
        data = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        # ciphertext includes tag in cryptography AESGCM
        blob = nonce + ciphertext
        b64 = base64.b64encode(blob).decode("ascii")
        tmp = self.vault_path.with_suffix(f"{self.vault_path.suffix}.tmp.{os.getpid()}")
        tmp.write_text(b64)
        tmp.chmod(0o600)
        os.replace(tmp, self.vault_path)

    def get(self, key: str) -> str | None:
        return self._load()["records"].get(key)

    def set(self, key: str, value: str) -> None:
        payload = self._load()
        payload["records"][key] = value
        self.save(payload)

    def delete(self, key: str) -> None:
        payload = self._load()
        if key in payload["records"]:
            del payload["records"][key]
            self.save(payload)

    def keys(self) -> list[str]:
        return sorted(self._load()["records"].keys())


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser(description="APO VS Code SecretStorage sync CLI")
    parser.add_argument("--vault", type=Path, default=default_vault_path(), help="Path to encrypted vault")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_get = sub.add_parser("get", help="Get a secret")
    p_get.add_argument("key")

    p_set = sub.add_parser("set", help="Set a secret")
    p_set.add_argument("key")
    p_set.add_argument("value")

    p_del = sub.add_parser("delete", help="Delete a secret")
    p_del.add_argument("key")

    p_list = sub.add_parser("list", help="List all keys")

    p_export = sub.add_parser("export", help="Export JSON to stdout (raw values)")
    p_export.add_argument("--format", choices=["json", "dotenv"], default="json")

    args = parser.parse_args()

    vault = APOSecretVault.create(args.vault)

    if args.cmd == "get":
        value = vault.get(args.key)
        if value is None:
            print(f"[apo-vault] key '{args.key}' not found", file=sys.stderr)
            sys.exit(1)
        print(value)
    elif args.cmd == "set":
        vault.set(args.key, args.value)
        print(f"[apo-vault] set {args.key}")
    elif args.cmd == "delete":
        vault.delete(args.key)
        print(f"[apo-vault] deleted {args.key} if present")
    elif args.cmd == "list":
        for k in vault.keys():
            print(k)
    elif args.cmd == "export":
        payload = vault.load()
        if args.format == "json":
            json.dump(payload["records"], sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
            print()
        else:
            for k, v in sorted(payload["records"].items()):
                print(f"{k}={v}")


if __name__ == "__main__":
    main()
