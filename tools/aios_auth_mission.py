#!/usr/bin/env python3
"""AUTH-causal mission: broker issues lease; lease is used to verify OpenAI access.

This proves AUTH lane is on the causal path of a cross-lane mission.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path("/Users/andy/HyperAI-Sync")
OUT = ROOT / "runtime" / "federation_orchestrator"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    log: dict = {"mission_id": f"auth-mission-{now_iso()}", "started_at": now_iso(), "stages": {}}

    # WAKE
    log["stages"]["WAKE"] = {"state_path": str(ROOT / "memory" / "project_state.json"), "note": "no prior state consumed"}

    # OBSERVE
    broker_status = httpx.get("http://127.0.0.1:8765/status", timeout=10)
    log["stages"]["OBSERVE"] = {
        "broker_status": {"url": "http://127.0.0.1:8765/status", "status": broker_status.status_code, "ok": broker_status.status_code == 200, "body_preview": broker_status.text[:120]},
    }

    # SELECT PURPOSE
    log["stages"]["SELECT_PURPOSE"] = {"purpose": "verify AUTH lane can issue a scoped lease and the lease works for OpenAI"}

    # ASSIGN MISSIONS
    log["stages"]["ASSIGN_MISSIONS"] = {
        "AUTH": "request capability lease for openai",
        "EXECUTE": "use lease to call OpenAI /v1/models",
        "VERIFICATION": "verify 200 and non-empty model list",
        "MEMORY": "record lease id and result",
    }

    # AUTH: request lease
    lease_req = {"node": "local", "task": "verify_openai_lease", "provider": "openai", "resource": "models", "action": "read", "ttl_req": 60}
    try:
        r = httpx.post("http://127.0.0.1:8765/capability", json=lease_req, timeout=15)
        auth_ok = r.status_code == 200
        lease = r.json() if auth_ok else {"error": r.text[:200]}
    except Exception as e:
        auth_ok = False
        lease = {"error": str(e)}
    log["stages"]["AUTH"] = {
        "request": lease_req,
        "response_status": r.status_code if 'r' in dir() else 0,
        "ok": auth_ok,
        "lease_id": lease.get("lease", {}).get("lease_id") if auth_ok else None,
    }

    # EXECUTE: use broker proxy with X-Lease-Id header
    if auth_ok and isinstance(lease, dict):
        lease_id = lease.get("lease", {}).get("lease_id")
        try:
            r2 = httpx.get("http://127.0.0.1:8765/proxy/openai/models", headers={"X-Lease-Id": lease_id}, timeout=30)
            exec_ok = r2.status_code == 200
            resp = r2.json()
            # broker wraps upstream response in `data`
            upstream = resp.get("data", {}) if exec_ok and isinstance(resp, dict) else {}
            models = upstream.get("data", [])[:3] if isinstance(upstream, dict) else []
        except Exception as e:
            exec_ok = False
            models = []
            r2 = None
    else:
        exec_ok = False
        models = []
        r2 = None

    log["stages"]["EXECUTE"] = {
        "url": "http://127.0.0.1:8765/proxy/openai/models",
        "status": r2.status_code if r2 else 0,
        "ok": exec_ok,
        "models_count": len(models),
        "models_preview": [m.get("id") for m in models] if models else [],
    }

    # VERIFY
    verified = auth_ok and exec_ok and len(models) > 0
    log["stages"]["VERIFY"] = {"verified": verified, "criteria": "broker lease 200 and OpenAI /models returns non-empty list"}

    # LEARN
    log["stages"]["LEARN"] = {
        "auth_lane_issuing_lease": auth_ok,
        "lease_token_usable_for_openai": exec_ok,
        "openai_access_verified": verified,
    }

    # UPDATE MEMORY
    (OUT / "auth_mission_execution_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")

    # SELECT NEXT ACTION
    next_action = "verify OPENAI_API_KEY_3 rotation persists and broker still healthy on next cycle"
    log["stages"]["UPDATE_MEMORY"] = {"auth_mission_execution_log": str(OUT / "auth_mission_execution_log.json")}
    log["stages"]["SELECT_NEXT_ACTION"] = {"next_action": next_action}
    log["completed_at"] = now_iso()
    (OUT / "auth_mission_execution_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"auth mission verified={verified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
