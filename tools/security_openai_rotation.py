#!/usr/bin/env python3
"""Rotate a compromised OpenAI project API key.

Does not print plaintext secrets. Uses OPENAI_ADMIN_KEY from credential broker's
loaded environment to create a new project key, update credentials.env, restart
the local credential broker, and delete the old key.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
import psutil

# Load broker creds without re-reading env directly from here.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.hyperai_credentials_loader import load_env_file  # noqa: E402


def mask(value: str, head: int = 6, tail: int = 4) -> str:
    if not value or len(value) <= head + tail + 4:
        return "<unset>"
    return f"{value[:head]}...{value[-tail:]}"


async def main() -> int:
    creds_path = Path.home() / ".config" / "hyperai" / "credentials.env"
    creds = load_env_file(creds_path)
    admin_key = creds.get("OPENAI_ADMIN_KEY")
    if not admin_key:
        print("ERROR: OPENAI_ADMIN_KEY not available in broker env", file=sys.stderr)
        return 1

    project_id = "proj_QeO1HsgWepb5Sz6LDyWjjcJ8"  # discovered via admin API listing
    old_key_id = "key_PkJCYiZB6uUHrKmg"  # HyperAI Runtime, redacted suffix ezMA

    headers = {"Authorization": f"Bearer {admin_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. create new project service account (returns an API key)
        new_name = f"HyperAI Runtime Rotated {datetime.now(timezone.utc).isoformat()[:19]}"
        r = await client.post(
            f"https://api.openai.com/v1/organization/projects/{project_id}/service_accounts",
            headers=headers,
            json={"name": new_name},
        )
        if r.status_code != 200:
            print(f"ERROR create key: {r.status_code} {r.text[:200]}", file=sys.stderr)
            return 1
        new_data = r.json()
        new_key_id = new_data["api_key"]["id"]
        new_key_value = new_data["api_key"]["value"]

        print(f"created new key id={new_key_id} redacted={mask(new_key_value)}")

    # 2. preserve evidence / backup
    backup_path = creds_path.with_suffix(f".env.bak.{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}")
    shutil.copy2(creds_path, backup_path)
    os.chmod(backup_path, 0o600)
    print(f"backed up credentials.env to {backup_path}")

    # 3. update credentials.env: overwrite OPENAI_API_KEY_3 with new value
    lines = creds_path.read_text(encoding="utf-8").splitlines(keepends=True)
    new_lines = []
    replaced = False
    for ln in lines:
        if ln.startswith("OPENAI_API_KEY_3="):
            new_lines.append(f"OPENAI_API_KEY_3={new_key_value}\n")
            replaced = True
        else:
            new_lines.append(ln)
    if not replaced:
        new_lines.append(f"\nOPENAI_API_KEY_3={new_key_value}\n")
    creds_path.write_text("".join(new_lines), encoding="utf-8")
    os.chmod(creds_path, 0o600)
    print("updated OPENAI_API_KEY_3 in credentials.env")

    # 4. restart credential broker
    broker_pid = None
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = p.info.get("cmdline") or []
            if any("hyperai_credentials_service" in part for part in cmd):
                broker_pid = p.info["pid"]
                break
        except Exception:
            continue
    if broker_pid:
        print(f"restarting credential broker pid={broker_pid}")
        os.kill(broker_pid, signal.SIGTERM)
        for _ in range(20):
            if not psutil.pid_exists(broker_pid):
                break
            time.sleep(0.5)
        if psutil.pid_exists(broker_pid):
            os.kill(broker_pid, signal.SIGKILL)
    else:
        print("WARNING: no running credential broker found")

    # start new broker
    subprocess.Popen(
        [sys.executable, str(ROOT / "tools" / "hyperai_credentials_service.py")],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    print("started new credential broker")

    # 5. wait for broker and verify openai
    for attempt in range(20):
        time.sleep(1.0)
        try:
            r = httpx.get("http://127.0.0.1:8765/status", timeout=5)
            if r.status_code == 200:
                status = r.json()
                openai_info = status.get("validation", {}).get("openai", {})
                if openai_info.get("healthy") and openai_info.get("valid_key"):
                    print(f"broker verified: openai active_key_ref={openai_info.get('valid_key')} masked={status.get('active_keys', {}).get('openai')}")
                    break
        except Exception:
            continue
    else:
        print("WARNING: broker did not verify openai in time", file=sys.stderr)

    # 6. delete old key
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.delete(
            f"https://api.openai.com/v1/organization/projects/{project_id}/api_keys/{old_key_id}",
            headers=headers,
        )
        if r.status_code == 200:
            print(f"deleted old key id={old_key_id}")
        else:
            print(f"WARNING delete old key: {r.status_code} {r.text[:200]}", file=sys.stderr)

    # 7. write incident receipt
    receipt = {
        "incident_id": f"sec-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "class": "exposed_api_key",
        "provider": "openai",
        "old_key_id": old_key_id,
        "old_key_masked": "<REDACTED>",
        "new_key_id": new_key_id,
        "new_key_masked": mask(new_key_value),
        "project_id": project_id,
        "credentials_file": str(creds_path),
        "backup_file": str(backup_path),
        "broker_restarted": True,
        "old_key_deleted": r.status_code == 200 if isinstance(r, httpx.Response) else False,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    receipt_path = ROOT / "runtime" / "federation_orchestrator" / "security_incident_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"wrote {receipt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
