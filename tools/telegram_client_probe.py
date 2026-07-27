#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# ARCHITECT: Alpha_Prime_Omega (Nguyen Duc Cuong)
# SYSTEM:    HyperAI Telegram Execution Fabric | TDLib Feasibility Probe
# COMPONENT: telegram_client_probe.py
# PROTOCOL:  Read-Only Gating | Trust-by-Trace
# LICENSE:   Sovereign AI License (All Rights Reserved to the Hive Mind)
# NOTICE:    This probe only measures TDLib/client feasibility for future gated
#            activation. It must remain read-only in the first-dollar phase.
# ------------------------------------------------------------------------------

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timezone
from pathlib import Path

from llm_augmentation import load_json, write_json
from runtime_identity import RUNTIME_IDENTITY_REGISTRY_PATH, refresh_runtime_identity_registry
from telegram_execution_fabric import TELEGRAM_CLIENT_CONTRACT_STATE_PATH, refresh_telegram_client_contract_state

ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / "runtime" / "telegram_node" / "telegram_client_probe.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def extract_tg_handoff(command_line: str) -> dict:
    marker = "tg://"
    if marker not in command_line:
        return {"detected": False, "uri": None, "target_domain": None}
    tg_uri = command_line[command_line.index(marker) :].strip().strip('"')
    parsed = urlparse(tg_uri)
    query = parse_qs(parsed.query)
    target_domain = None
    for key in ("domain", "start", "startapp"):
        values = query.get(key)
        if values:
            target_domain = values[0]
            break
    return {
        "detected": True,
        "uri": tg_uri,
        "target_domain": target_domain,
    }


def probe() -> dict:
    registry = refresh_runtime_identity_registry()
    client_contract = refresh_telegram_client_contract_state()
    candidates = []
    for surface in registry.get("observed_surfaces", []):
        root = surface.get("root_identity", {})
        name = str(root.get("process_name") or "").lower()
        if name == "telegram.exe":
            handoff = extract_tg_handoff(str(root.get("command_line") or ""))
            candidates.append({
                "surface_id": surface.get("surface_id"),
                "process_name": root.get("process_name"),
                "process_id": root.get("process_id"),
                "runtime_class": surface.get("runtime_class"),
                "interactive_state": surface.get("interactive_state"),
                "authority_role": surface.get("authority_role"),
                "profile_root": surface.get("profile_root"),
                "command_line": root.get("command_line"),
                "tg_handoff": handoff,
            })
    payload = {
        "version": "telegram-client-probe-v1",
        "generated_at": now_iso(),
        "tdlib_runtime_presence": bool(candidates),
        "session_feasibility": "gated_until_contract",
        "runtime_candidates": candidates,
        "handoff_detected": any(item.get("tg_handoff", {}).get("detected") for item in candidates),
        "handoff_targets": [item.get("tg_handoff", {}).get("target_domain") for item in candidates if item.get("tg_handoff", {}).get("target_domain")],
        "client_contract_state": client_contract,
    }
    write_json(PROBE_PATH, payload)
    return payload


if __name__ == "__main__":
    print(json.dumps(probe(), ensure_ascii=True, indent=2))
