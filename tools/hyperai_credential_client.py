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

"""HyperAI Credential Broker client — APΩ-safe key usage for agents.

This module lets HyperAI agents request scoped capabilities and call provider
endpoints through the broker without ever touching plaintext secrets.
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any


DEFAULT_BROKER = os.environ.get("HYPERAI_CREDENTIAL_BROKER", "http://127.0.0.1:8765")


def _http(method: str, path: str, payload: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
    url = f"{DEFAULT_BROKER}{path}"
    data = None
    req_headers = {"Accept": "application/json", **(headers or {})}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except Exception:
            return {"error": body, "status_code": e.code}
    except Exception as e:
        return {"error": str(e)}


def request_capability(
    node: str,
    task: str,
    provider: str,
    resource: str,
    action: str = "read",
    scope_req: list[str] | None = None,
    ttl_req: int = 600,
) -> dict[str, Any]:
    payload = {
        "node": node,
        "task": task,
        "provider": provider,
        "resource": resource,
        "action": action,
        "scope_req": scope_req or [action],
        "ttl_req": ttl_req,
    }
    return _http("POST", "/capability", payload)


def proxy_get(lease_id: str, provider: str, endpoint: str) -> dict[str, Any]:
    """Call a broker proxy endpoint with a lease. `endpoint` is the broker path, e.g. '/proxy/openai/models'."""
    return _http("GET", endpoint, headers={"X-Lease-Id": lease_id})


def get_status() -> dict[str, Any]:
    return _http("GET", "/status")


def revoke_lease(lease_id: str) -> dict[str, Any]:
    return _http("DELETE", f"/capability/{lease_id}")


def lease_is_allowed(response: dict[str, Any]) -> bool:
    return response.get("decision") == "ALLOW" and "lease" in response


def get_lease_id(response: dict[str, Any]) -> str | None:
    return response.get("lease", {}).get("lease_id")


def discover_providers(task_text: str) -> list[str]:
    """Naive provider keyword detection for routing OODA tasks to the broker."""
    providers = [
        "openai", "github", "telegram", "notion", "gemini", "openrouter",
        "mistral", "deepseek", "xai", "postman", "vercel", "docker", "anthropic",
    ]
    lowered = task_text.lower()
    return [p for p in providers if p in lowered]


def execute_task(
    node: str,
    task: str,
    provider: str,
    resource: str,
    endpoint: str,
    ttl: int = 60,
) -> dict[str, Any]:
    """One-shot: request capability, then call the proxy endpoint. Returns full broker response."""
    cap = request_capability(node, task, provider, resource, "read", ["read"], ttl)
    if not lease_is_allowed(cap):
        return {"ok": False, "phase": "capability_request", "capability": cap}
    lease_id = get_lease_id(cap)
    result = proxy_get(lease_id or "", provider, endpoint)
    result["lease_id"] = lease_id
    result["capability"] = cap.get("lease")
    result["ok"] = "data" in result
    return result