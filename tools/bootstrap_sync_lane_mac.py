#!/usr/bin/env python3
"""Bootstrap the MacBook SyncLane from the materialized Titan lane."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TITAN_LANE_ROOT = Path(r"C:\Users\pc\HyperAI-Sync")
OUTPUT_PATH = ROOT / "runtime" / "lineage" / "sync_lane_inventory_mac_20260421.json"
DEFAULT_MAC_HOST = "andy.local"
DEFAULT_MAC_USER = "andy"
DEFAULT_MAC_LANE_ROOT = "/Users/andy/HyperAI-Sync"
DEFAULT_IDENTITY = Path.home() / ".ssh" / "hyperai_titan_to_macbook_ed25519"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def detect_binary(name: str, known_paths: list[Path]) -> Path | None:
    found = shutil.which(name)
    if found:
        return Path(found)
    for path in known_paths:
        if path.exists():
            return path
    return None


def run_command(command: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def build_seed_archive() -> Path:
    archive_dir = ROOT / "runtime" / "lineage"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / "sync_lane_titan_seed_20260421.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(TITAN_LANE_ROOT.rglob("*")):
            if not path.is_file():
                continue
            if ".git" in path.parts:
                continue
            zf.write(path, arcname=path.relative_to(TITAN_LANE_ROOT).as_posix())
    return archive_path


def remote_target(user: str, host: str) -> str:
    return f"{user}@{host}"


def ssh_base(ssh_path: Path, identity_path: Path, user: str, host: str) -> list[str]:
    return [
        str(ssh_path),
        "-i",
        str(identity_path),
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "ConnectTimeout=10",
        remote_target(user, host),
    ]


def scp_base(scp_path: Path, identity_path: Path) -> list[str]:
    return [
        str(scp_path),
        "-i",
        str(identity_path),
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "ConnectTimeout=10",
    ]


def run_remote_python(ssh_path: Path, identity_path: Path, user: str, host: str, script: str) -> tuple[int, str, str]:
    remote_command = "python3 - <<'PY'\n" + script + "\nPY"
    return run_command(ssh_base(ssh_path, identity_path, user, host) + [remote_command])


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap the MacBook SyncLane from Titan.")
    parser.add_argument("--mac-host", default=DEFAULT_MAC_HOST)
    parser.add_argument("--mac-user", default=DEFAULT_MAC_USER)
    parser.add_argument("--mac-lane-root", default=DEFAULT_MAC_LANE_ROOT)
    parser.add_argument("--identity", default=str(DEFAULT_IDENTITY))
    args = parser.parse_args()

    ssh_path = detect_binary(
        "ssh",
        [
            Path(r"C:\Program Files\Git\usr\bin\ssh.exe"),
            Path(r"C:\Users\pc\.espressif\tools\idf-git\2.39.2\usr\bin\ssh.exe"),
        ],
    )
    scp_path = detect_binary("scp", [Path(r"C:\Program Files\Git\usr\bin\scp.exe")])
    if not ssh_path or not scp_path:
        raise SystemExit("ssh/scp binary not found")

    identity_path = Path(args.identity)
    if not identity_path.exists():
        raise SystemExit(f"identity file missing: {identity_path}")
    if not TITAN_LANE_ROOT.exists():
        raise SystemExit(f"titan lane missing: {TITAN_LANE_ROOT}")

    archive_path = build_seed_archive()
    remote_zip = f"/tmp/{archive_path.name}"

    preflight_script = f"""
from pathlib import Path
lane = Path({args.mac_lane_root!r})
lane.mkdir(parents=True, exist_ok=True)
existing = [p for p in lane.iterdir() if p.name != '.git']
if existing:
    print("EXISTS_NONEMPTY")
else:
    print("EMPTY_OK")
"""
    code, stdout, stderr = run_remote_python(ssh_path, identity_path, args.mac_user, args.mac_host, preflight_script)
    if code != 0:
        raise SystemExit(stderr.strip() or stdout.strip())
    if stdout.strip() != "EMPTY_OK":
        raise SystemExit(f"remote lane is not empty: {stdout.strip()}")

    code, stdout, stderr = run_command(
        scp_base(scp_path, identity_path) + [str(archive_path), f"{remote_target(args.mac_user, args.mac_host)}:{remote_zip}"]
    )
    if code != 0:
        raise SystemExit(stderr.strip() or stdout.strip())

    remote_script = f"""
import hashlib, json, subprocess, zipfile
from datetime import datetime, timezone
from pathlib import Path

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

lane = Path({args.mac_lane_root!r})
zip_path = Path({remote_zip!r})
lane.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path) as zf:
    zf.extractall(lane)
if not (lane / ".git").exists():
    subprocess.run(["git", "init"], cwd=lane, check=True, capture_output=True, text=True)
status = subprocess.run(["git", "status", "--short"], cwd=lane, check=True, capture_output=True, text=True)
branch = subprocess.run(["git", "branch", "--show-current"], cwd=lane, check=True, capture_output=True, text=True)
files = []
for path in sorted(p for p in lane.rglob("*") if p.is_file() and ".git" not in p.parts):
    rel = path.relative_to(lane).as_posix()
    files.append({{
        "relative_path": rel,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }})
inventory = {{
    "schema_version": "2026-04-21.sync-lane-inventory.v1",
    "created_at": now_iso(),
    "machine_id": "macbook_m2",
    "lane_root": str(lane),
    "whitelist_version": "2026-04-21.v1",
    "file_count": len(files),
    "git": {{
        "branch": branch.stdout.strip(),
        "status_excerpt": status.stdout.strip(),
    }},
    "files": files,
}}
zip_path.unlink(missing_ok=True)
print(json.dumps(inventory, ensure_ascii=True))
"""
    code, stdout, stderr = run_remote_python(ssh_path, identity_path, args.mac_user, args.mac_host, remote_script)
    if code != 0:
        raise SystemExit(stderr.strip() or stdout.strip())
    inventory = json.loads(stdout)
    OUTPUT_PATH.write_text(json.dumps(inventory, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"inventory_path": str(OUTPUT_PATH), "file_count": inventory["file_count"]}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
