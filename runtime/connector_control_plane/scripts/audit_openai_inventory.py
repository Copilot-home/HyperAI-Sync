import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

RUNTIME_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(RUNTIME_ROOT)
sys.path.insert(0, RUNTIME_ROOT)
sys.path.insert(0, REPO_ROOT)

import requests
from connector_control_plane.credential_resolver import CredentialResolver


def get_key() -> str:
    return CredentialResolver().resolve("env:OPENAI_ADMIN_KEY")


def get(path: str, admin_key: str) -> Any:
    r = requests.get(f"https://api.openai.com/v1/{path}", headers={"Authorization": f"Bearer {admin_key}"}, timeout=30)
    if r.status_code == 200:
        return r.json()
    return {"_error": r.status_code, "_text": r.text[:200]}


def usage_path(resource: str, start: int, end: int) -> str:
    return f"organization/usage/{resource}?start_time={start}&end_time={end}"


def collect_inventory(admin_key: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    now_ts = int(now.timestamp())
    start_ts = now_ts - 30 * 24 * 3600
    now_iso = now.isoformat()

    users = get("organization/users", admin_key)
    admin_keys = get("organization/admin_api_keys", admin_key)
    projects = get("organization/projects", admin_key)
    spend_limit = get("organization/spend_limit", admin_key)
    spend_alerts = get("organization/spend_alerts", admin_key)
    usage_completions = get(usage_path("completions", start_ts, now_ts), admin_key)
    usage_embeddings = get(usage_path("embeddings", start_ts, now_ts), admin_key)
    usage_audio_speeches = get(usage_path("audio_speeches", start_ts, now_ts), admin_key)
    usage_audio_transcriptions = get(usage_path("audio_transcriptions", start_ts, now_ts), admin_key)
    usage_images = get(usage_path("images", start_ts, now_ts), admin_key)
    usage_costs = get(f"organization/costs?start_time={start_ts}&end_time={now_ts}", admin_key)
    usage_moderations = get(usage_path("moderations", start_ts, now_ts), admin_key)
    usage_web_search = get(usage_path("web_search_calls", start_ts, now_ts), admin_key)
    invites = get("organization/invites", admin_key)
    audit_logs = get("organization/audit_logs?limit=10", admin_key)

    project_details = []
    for project in projects.get("data", []):
        pid = project.get("id")
        project_api_keys = get(f"organization/projects/{pid}/api_keys", admin_key)
        service_accounts = get(f"organization/projects/{pid}/service_accounts", admin_key)
        project_details.append({
            "project": project,
            "api_keys": project_api_keys,
            "service_accounts": service_accounts,
        })

    return {
        "collected_at": now_iso,
        "period_start_ts": start_ts,
        "period_end_ts": now_ts,
        "users": users,
        "admin_api_keys": admin_keys,
        "projects": projects,
        "project_details": project_details,
        "spend_limit": spend_limit,
        "spend_alerts": spend_alerts,
        "usage": {
            "completions": usage_completions,
            "embeddings": usage_embeddings,
            "audio_speeches": usage_audio_speeches,
            "audio_transcriptions": usage_audio_transcriptions,
            "images": usage_images,
            "moderations": usage_moderations,
            "web_search_calls": usage_web_search,
        },
        "costs": usage_costs,
        "invites": invites,
        "audit_logs_sample": audit_logs,
    }


def classify_keys(admin_key_list: List[Dict], project_details: List[Dict]) -> Dict[str, Any]:
    admin_user_keys = 0
    admin_service_keys = 0
    legacy_user_keys = 0
    unused_keys = 0
    keys_without_expiry = 0

    for k in admin_key_list:
        owner_type = k.get("owner", {}).get("type", "user")
        if owner_type == "service_account":
            admin_service_keys += 1
        else:
            admin_user_keys += 1
        if k.get("last_used_at") is None:
            unused_keys += 1
        if k.get("expires_at") is None:
            keys_without_expiry += 1

    for detail in project_details:
        legacy_user_keys += len(detail["api_keys"].get("data", []))

    return {
        "legacy_user_keys_active": legacy_user_keys,
        "service_account_keys_active": admin_service_keys,
        "admin_keys_active": admin_user_keys,
        "unused_keys": unused_keys,
        "keys_without_expiry": keys_without_expiry,
    }


def summarize(data: Dict[str, Any]) -> Dict[str, Any]:
    user_list = data["users"].get("data", [])
    admin_key_list = data["admin_api_keys"].get("data", [])
    project_list = data["projects"].get("data", [])

    roles = {}
    for u in user_list:
        roles[u.get("role", "unknown")] = roles.get(u.get("role", "unknown"), 0) + 1

    key_metrics = classify_keys(admin_key_list, data["project_details"])

    spend_enforcement = data["spend_limit"].get("enforcement", {}).get("status", "unknown")
    threshold_cents = data["spend_limit"].get("threshold_amount")
    threshold_usd = threshold_cents / 100.0 if threshold_cents else None

    usage_status = {}
    for k, v in data["usage"].items():
        if "_error" in v:
            usage_status[k] = v["_error"]
        elif "data" in v and isinstance(v["data"], list):
            usage_status[k] = {"ok": True, "data_points": len(v["data"])}
        else:
            usage_status[k] = {"ok": True, "keys": list(v.keys())[:5]}

    costs_data = data["costs"]
    cost_summary: Any
    if "_error" in costs_data:
        cost_summary = costs_data["_error"]
    elif "data" in costs_data and isinstance(costs_data["data"], list):
        cost_summary = {"ok": True, "data_points": len(costs_data["data"])}
    else:
        cost_summary = {"ok": True, "keys": list(costs_data.keys())[:5]}

    invites_data = data["invites"]
    invite_count = len(invites_data.get("data", [])) if "_error" not in invites_data else None

    return {
        "users": {"total": len(user_list), "roles": roles},
        "projects": {"total": len(project_list), "names": [p.get("name") for p in project_list]},
        "keys": key_metrics,
        "spend": {
            "limit_usd": threshold_usd,
            "enforcement_status": spend_enforcement,
            "alert_count": len(data["spend_alerts"].get("data", [])),
        },
        "usage": usage_status,
        "costs": cost_summary,
        "invites": {"ok": "_error" not in invites_data, "count": invite_count},
        "period": {"start_ts": data["period_start_ts"], "end_ts": data["period_end_ts"]},
    }


def main():
    admin_key = get_key()
    data = collect_inventory(admin_key)
    summary = summarize(data)
    output = {"summary": summary, "raw": data}
    print(json.dumps(output, indent=2, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
