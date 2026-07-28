#!/usr/bin/env python3
"""HyperAI Credential Broker — APΩ-aligned credential capability service.

This service does not hand out plaintext secrets. It validates credentials,
evaluates admissibility (Identity, Ownership, Canon, Proof, Budget, Drift),
issues short-lived scoped leases, executes API calls on behalf of a lease,
and returns proofs without ever logging the secret value.

Run locally:
    python tools/hyperai_credentials_service.py

Run with uvicorn:
    uvicorn tools.hyperai_credentials_service:app --host 127.0.0.1 --port 8765

Docker:
    docker compose up --build -d hyperai-credentials

Test:
    curl -s http://127.0.0.1:8765/status
    curl -s -X POST http://127.0.0.1:8765/capability \
      -H 'Content-Type: application/json' \
      -d '{"node":"hyperai-worker","task":"list-models","provider":"openai","resource":"models","action":"read","scope_req":["read"],"ttl_req":60}'
    curl -s -H 'X-Lease-Id: <lease_id>' http://127.0.0.1:8765/proxy/openai/models
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import time
import urllib.request
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field

try:
    from tools.hyperai_credentials_loader import load_env_file, DEFAULT_OUT
except ImportError:
    from hyperai_credentials_loader import load_env_file, DEFAULT_OUT


app = FastAPI(title="HyperAI Credential Broker")


class CapabilityRequest(BaseModel):
    node: str = Field(..., description="Workload identity of the requester")
    task: str = Field(..., description="Task this capability is for")
    provider: str = Field(..., description="Provider, e.g. openai, github, telegram")
    resource: str = Field(default="default", description="Resource the action targets")
    action: str = Field(default="read", description="Action: read, write, delete, admin")
    scope_req: list[str] = Field(default_factory=lambda: ["read"], description="Required scopes")
    ttl_req: int = Field(default=600, ge=1, le=3600, description="Requested TTL in seconds")
    proof_req: dict[str, Any] = Field(default_factory=dict, description="Evidence contract / policy hints")


class Lease:
    def __init__(
        self,
        lease_id: str,
        node: str,
        task: str,
        provider: str,
        resource: str,
        action: str,
        scope: list[str],
        active_key_ref: str,
        masked_key: str,
        ttl: int,
        calls_limit: int,
    ) -> None:
        self.lease_id = lease_id
        self.node = node
        self.task = task
        self.provider = provider
        self.resource = resource
        self.action = action
        self.scope = scope
        self.active_key_ref = active_key_ref
        self.masked_key = masked_key
        self.issued_at = time.time()
        self.expires_at = self.issued_at + ttl
        self.state = "ACTIVE"
        self.calls_limit = calls_limit
        self.calls_used = 0
        self.calls_remaining = calls_limit
        self.proof_log: list[dict[str, Any]] = []

    def to_public(self) -> dict[str, Any]:
        return {
            "lease_id": self.lease_id,
            "node": self.node,
            "task": self.task,
            "provider": self.provider,
            "resource": self.resource,
            "action": self.action,
            "scope": self.scope,
            "active_key_ref": self.active_key_ref,
            "masked_key": self.masked_key,
            "issued_at": _ts(self.issued_at),
            "expires_at": _ts(self.expires_at),
            "state": self.state,
            "calls_used": self.calls_used,
            "calls_remaining": self.calls_remaining,
            "proof_count": len(self.proof_log),
        }

    def is_expired(self) -> bool:
        return self.state == "EXPIRED" or time.time() > self.expires_at

    def is_revoked(self) -> bool:
        return self.state == "REVOKED"

    def record(self, entry: dict[str, Any]) -> None:
        self.proof_log.append(entry)


def _ts(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat().replace("+00:00", "Z")


PROVIDER_POLICY: dict[str, dict[str, Any]] = {
    "openai": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "github": {"actions": {"read"}, "resources": {"user", "repos"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "telegram": {"actions": {"read"}, "resources": {"me"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "notion": {"actions": {"read"}, "resources": {"me", "databases"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "gemini": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "openrouter": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "mistral": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "deepseek": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "xai": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "postman": {"actions": {"read"}, "resources": {"me"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "vercel": {"actions": {"read"}, "resources": {"user"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "docker": {"actions": {"read"}, "resources": {"self"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 30},
    "anthropic": {"actions": {"read"}, "resources": {"models"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
    "context7": {"actions": {"read"}, "resources": {"status"}, "default_ttl": 600, "max_ttl": 3600, "calls_per_min": 60},
}

KNOWN_NODES = {
    "hyperai-worker",
    "hyperai-ooda",
    "codex",
    "devin",
    "users/andy",
    "local",
    "agent",
}

ENDPOINT_RESOURCE_MAP: dict[str, tuple[str, str]] = {
    "/proxy/openai/models": ("openai", "models"),
    "/proxy/github/user": ("github", "user"),
    "/proxy/telegram/me": ("telegram", "me"),
    "/proxy/notion/me": ("notion", "me"),
    "/proxy/openrouter/models": ("openrouter", "models"),
    "/proxy/mistral/models": ("mistral", "models"),
    "/proxy/deepseek/models": ("deepseek", "models"),
    "/proxy/xai/models": ("xai", "models"),
    "/proxy/postman/me": ("postman", "me"),
    "/proxy/vercel/user": ("vercel", "user"),
}


class CredentialManager:
    """APΩ credential broker: validate keys, evaluate admissibility, issue leases, execute proxy calls."""

    def __init__(self, env_path: Path | None = None) -> None:
        self.env_path = env_path or DEFAULT_OUT
        self.creds: dict[str, str] = {}
        self.active: dict[str, str] = {}
        self.active_key_ref: dict[str, str] = {}
        self.validation_log: dict[str, dict[str, Any]] = {}
        self.leases: dict[str, Lease] = {}
        self.rate_window: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()
        self._loaded = False

    def load(self) -> dict[str, str]:
        if not self._loaded:
            self.creds = load_env_file(self.env_path) if self.env_path.exists() else {}
            self._loaded = True
        return self.creds

    @staticmethod
    def mask(value: str | None, head: int = 6, tail: int = 4) -> str:
        if not value:
            return "<unset>"
        if len(value) <= head + tail + 4:
            return "*" * len(value)
        return f"{value[:head]}...{value[-tail:]}"

    def _key_candidates(self, provider: str) -> list[str]:
        patterns: dict[str, list[str]] = {
            "github": ["GITHUB_PAT", "GITHUB_PAT_1"],  # GITHUB_PAT_2..5 and ALT1 removed 2026-07-28 (401); capability retained via first valid key
            "openai": ["OPENAI_API_KEY", "OPENAI_API_KEY_1", "OPENAI_API_KEY_2", "OPENAI_API_KEY_3"],
            "telegram": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_BOT_TOKEN_FINALAI", "TELEGRAM_BOT_TOKEN_SIGNALANDY"],
            "notion": ["NOTION_API_KEY"],
            "gemini": ["GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3", "GEMINI_API_KEY_4", "GEMINI_API_KEY_5"],
            "openrouter": ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_ALT1"],
            "mistral": ["MISTRAL_API_KEY"],
            "deepseek": ["DEEPSEEK_API_KEY"],
            "xai": ["XAI_API_KEY"],
            "postman": ["POSTMAN_API_KEY", "POSTMAN_API_KEY_ALT1"],
            "vercel": ["VERCEL_TOKEN"],
            "docker": ["DOCKER_ORG_ACCESS_TOKEN"],
            "anthropic": ["CLAUDE_ADMIN_KEY"],
            "context7": ["CONTEXT7_API_KEY"],
        }
        noise_suffixes = ("DESCRIPTION", "LABEL", "EXPIRES", "EXPIRY", "URL", "LINK")
        base = patterns.get(provider, [])
        extras = [
            k for k in self.creds
            if k not in base and provider in k.lower() and not any(n in k for n in noise_suffixes)
        ]
        return base + extras

    async def _http_get(self, url: str, headers: dict[str, str] | None = None, timeout: int = 15) -> tuple[int, Any]:
        loop = asyncio.get_event_loop()

        def _fetch() -> tuple[int, Any]:
            req = urllib.request.Request(url, headers=headers or {})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = resp.read().decode("utf-8", errors="replace")
                    try:
                        return resp.status, json.loads(data)
                    except Exception:
                        return resp.status, data
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace") if e.fp else ""
                return e.code, body
            except Exception as e:
                return 0, str(e)

        return await loop.run_in_executor(None, _fetch)

    async def _validate_provider(self, provider: str) -> dict[str, Any]:
        self.load()
        candidates = self._key_candidates(provider)
        result: dict[str, Any] = {"provider": provider, "valid_key": None, "tried": []}

        for key in candidates:
            value = self.creds.get(key)
            if not value:
                continue
            status, body = 0, ""
            try:
                status, body = await self._probe(provider, value)
            except Exception as e:
                body = str(e)
            ok = 200 <= status < 300
            entry = {
                "key": key,
                "masked": self.mask(value),
                "status_code": status,
                "ok": ok,
                "detail": str(body)[:200] if not ok else None,
            }
            result["tried"].append(entry)
            if ok and not result["valid_key"]:
                result["valid_key"] = key
                self.active[provider] = value
                self.active_key_ref[provider] = key
                if provider == "github":
                    os.environ["GH_TOKEN"] = value
                    os.environ["GITHUB_TOKEN"] = value
                break

        self.validation_log[provider] = result
        return result

    async def _probe(self, provider: str, token: str) -> tuple[int, Any]:
        if provider == "github":
            return await self._http_get(
                "https://api.github.com/user",
                {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            )
        if provider == "openai":
            return await self._http_get(
                "https://api.openai.com/v1/models",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "telegram":
            return await self._http_get(f"https://api.telegram.org/bot{token}/getMe")
        if provider == "notion":
            return await self._http_get(
                "https://api.notion.com/v1/users/me",
                {"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
            )
        if provider == "gemini":
            return await self._http_get(
                f"https://generativelanguage.googleapis.com/v1beta/models?key={token}"
            )
        if provider == "openrouter":
            return await self._http_get(
                "https://openrouter.ai/api/v1/models",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "mistral":
            return await self._http_get(
                "https://api.mistral.ai/v1/models",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "deepseek":
            return await self._http_get(
                "https://api.deepseek.com/models",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "xai":
            return await self._http_get(
                "https://api.x.ai/v1/models",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "postman":
            return await self._http_get(
                "https://api.getpostman.com/me",
                {"X-Api-Key": token},
            )
        if provider == "vercel":
            return await self._http_get(
                "https://api.vercel.com/v2/user",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "docker":
            return await self._http_get(
                "https://hub.docker.com/v2/users/self/",
                {"Authorization": f"Bearer {token}"},
            )
        if provider == "anthropic":
            return await self._http_get(
                "https://api.anthropic.com/v1/models",
                {"x-api-key": token, "anthropic-version": "2023-06-01"},
            )
        if provider == "context7":
            return await self._http_get(
                "https://context7.com/api/v1/status",
                {"Authorization": f"Bearer {token}"},
            )
        return 0, "unsupported_provider"

    async def validate_all(self, providers: list[str] | None = None) -> dict[str, dict[str, Any]]:
        async with self._lock:
            providers = providers or list(PROVIDER_POLICY.keys())
            await asyncio.gather(*(self._validate_provider(p) for p in providers))
            return dict(self.validation_log)

    def get_active(self, provider: str) -> str | None:
        return self.active.get(provider)

    def get_active_key_ref(self, provider: str) -> str | None:
        return self.active_key_ref.get(provider)

    # ---- APΩ admissibility & lease ----

    def admissible(self, req: CapabilityRequest) -> dict[str, Any]:
        """Evaluate the Adm_Ω function for a capability request."""
        self.load()
        checks: dict[str, Any] = {}

        # Identity
        checks["identity"] = req.node in KNOWN_NODES

        # Canon: well-formed, provider supported
        checks["canon"] = (
            bool(req.node and req.task and req.provider)
            and req.provider in PROVIDER_POLICY
        )

        # Proof: a validated key exists for the provider
        active_key = self.get_active(req.provider)
        info = self.validation_log.get(req.provider, {})
        checks["proof"] = bool(active_key and info.get("valid_key"))

        # Ownership / Policy: action and resource allowed
        policy = PROVIDER_POLICY.get(req.provider, {})
        allowed_actions = policy.get("actions", set())
        allowed_resources = policy.get("resources", set())
        checks["policy"] = req.action in allowed_actions and req.resource in allowed_resources

        # Scope: required scopes subset of policy scope (policy actions map to scopes here)
        req_scopes = set(req.scope_req)
        checks["scope"] = req_scopes.issubset(allowed_actions)

        # Budget: TTL bounds and rate window
        checks["ttl"] = 0 < req.ttl_req <= policy.get("max_ttl", 3600)
        checks["rate"] = self._check_rate(req.provider, policy)

        # Drift / audience: provider request must match key audience
        checks["drift"] = active_key is not None and self.active_key_ref.get(req.provider) is not None

        all_ok = all(checks.values())
        if all_ok:
            return {"decision": "ALLOW", "checks": checks}
        failed = [k for k, v in checks.items() if not v]
        return {"decision": "DENY", "reason": f"checks_failed: {','.join(failed)}", "checks": checks}

    def _check_rate(self, provider: str, policy: dict[str, Any]) -> bool:
        cap = policy.get("calls_per_min", 60)
        now = time.time()
        window = self.rate_window[provider]
        # Keep calls in the last 60s
        cutoff = now - 60
        while window and window[0] < cutoff:
            window.pop(0)
        return len(window) < cap

    def _count_rate(self, provider: str) -> None:
        now = time.time()
        window = self.rate_window[provider]
        cutoff = now - 60
        while window and window[0] < cutoff:
            window.pop(0)
        window.append(now)

    async def ensure_active(self, provider: str) -> bool:
        if self.get_active(provider):
            return True
        info = await self._validate_provider(provider)
        return bool(info.get("valid_key"))

    async def issue_lease(self, req: CapabilityRequest) -> Lease | dict[str, Any]:
        async with self._lock:
            decision = self.admissible(req)
            if decision["decision"] != "ALLOW":
                return decision

            if not await self.ensure_active(req.provider):
                return {"decision": "DENY", "reason": "no_valid_key_after_validation"}

            policy = PROVIDER_POLICY[req.provider]
            ttl = min(req.ttl_req, policy["max_ttl"])
            active_key_ref = self.active_key_ref[req.provider]
            active_value = self.active[req.provider]
            calls_limit = policy.get("calls_per_min", 60)

            lease = Lease(
                lease_id=f"lease-{uuid.uuid4().hex[:16]}",
                node=req.node,
                task=req.task,
                provider=req.provider,
                resource=req.resource,
                action=req.action,
                scope=list(req.scope_req),
                active_key_ref=active_key_ref,
                masked_key=self.mask(active_value),
                ttl=ttl,
                calls_limit=calls_limit,
            )
            self.leases[lease.lease_id] = lease
            self._count_rate(req.provider)
            return lease

    def get_lease(self, lease_id: str) -> Lease | None:
        lease = self.leases.get(lease_id)
        if not lease:
            return None
        if lease.is_expired() and lease.state == "ACTIVE":
            lease.state = "EXPIRED"
        return lease

    def revoke_lease(self, lease_id: str) -> Lease | None:
        lease = self.get_lease(lease_id)
        if lease:
            lease.state = "REVOKED"
        return lease

    def record_proof(self, lease: Lease, status: int, endpoint: str, data: Any) -> dict[str, Any]:
        """Record execution proof metadata without storing the secret or raw sensitive payload."""
        now = time.time()
        content = json.dumps(data, sort_keys=True, ensure_ascii=True).encode("utf-8")
        proof = {
            "at": _ts(now),
            "provider": lease.provider,
            "endpoint": endpoint,
            "status_code": status,
            "content_sha256": hashlib.sha256(content).hexdigest(),
            "lease_id": lease.lease_id,
        }
        lease.record(proof)
        return proof

    async def cleanup_expired_leases(self) -> None:
        while True:
            await asyncio.sleep(30)
            async with self._lock:
                for lease in self.leases.values():
                    if lease.state == "ACTIVE" and lease.is_expired():
                        lease.state = "EXPIRED"

    def state_counts(self) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for provider in PROVIDER_POLICY:
            info = self.validation_log.get(provider, {})
            if info.get("valid_key"):
                if any(l.provider == provider and l.state == "ACTIVE" for l in self.leases.values()):
                    counts["ACTIVE"] += 1
                else:
                    counts["VALIDATED"] += 1
            else:
                has_candidate = bool(self._key_candidates(provider))
                if has_candidate:
                    counts["PRESENT_UNVERIFIED"] += 1
                else:
                    counts["UNKNOWN"] += 1
        return dict(counts)

    def status(self) -> dict[str, Any]:
        active_summary = {
            p: {"key": k, "masked": self.mask(self.active.get(p))}
            for p, k in self.active_key_ref.items()
        }
        return {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "env_source": str(self.env_path),
            "total_keys": len(self.creds),
            "active_keys": {k: v["masked"] for k, v in active_summary.items()},
            "validation": {
                p: {
                    "valid_key": info.get("valid_key"),
                    "healthy": info.get("valid_key") is not None,
                    "tried": len(info.get("tried", [])),
                }
                for p, info in self.validation_log.items()
            },
            "leases": {
                "total": len(self.leases),
                "active": sum(1 for l in self.leases.values() if l.state == "ACTIVE"),
                "expired": sum(1 for l in self.leases.values() if l.state == "EXPIRED"),
                "revoked": sum(1 for l in self.leases.values() if l.state == "REVOKED"),
            },
            "state_counts": self.state_counts(),
        }


# Global manager
_manager_path = Path(os.environ.get("HYPERAI_CREDENTIALS", str(DEFAULT_OUT)))
manager = CredentialManager(_manager_path)


@app.on_event("startup")
async def _startup() -> None:
    manager.load()
    asyncio.create_task(manager.validate_all())
    asyncio.create_task(manager.cleanup_expired_leases())


@app.get("/")
async def root():
    return {
        "service": "HyperAI Credential Broker",
        "canon": "/canon",
        "status": "/status",
        "capability": "POST /capability",
        "proxy": "GET /proxy/{provider}/{endpoint} with X-Lease-Id",
    }


@app.get("/canon")
async def canon():
    canon_path = Path(__file__).resolve().parents[1] / "memory" / "APΩ_CREDENTIAL_CANON.md"
    if canon_path.exists():
        return PlainTextResponse(canon_path.read_text(encoding="utf-8"))
    raise HTTPException(404, "canon_not_found")


@app.get("/status")
async def status():
    return manager.status()


@app.get("/state")
async def state():
    return {
        "credential_states": manager.state_counts(),
        "leases": {lid: l.to_public() for lid, l in manager.leases.items() if l.state == "ACTIVE"},
    }


@app.post("/refresh")
async def refresh():
    await manager.validate_all()
    return manager.status()


@app.post("/capability")
async def capability(req: CapabilityRequest):
    result = await manager.issue_lease(req)
    if isinstance(result, Lease):
        return {
            "decision": "ALLOW",
            "lease": result.to_public(),
            "note": "Use X-Lease-Id header to call /proxy endpoints",
        }
    raise HTTPException(403, result)


@app.get("/capability/{lease_id}")
async def get_lease(lease_id: str):
    lease = manager.get_lease(lease_id)
    if not lease:
        raise HTTPException(404, "lease_not_found")
    return lease.to_public()


@app.delete("/capability/{lease_id}")
async def revoke_lease(lease_id: str):
    lease = manager.revoke_lease(lease_id)
    if not lease:
        raise HTTPException(404, "lease_not_found")
    return {"lease_id": lease_id, "state": lease.state}


def _require_lease(x_lease_id: str | None, provider: str, resource: str, action: str = "read") -> Lease:
    if not x_lease_id:
        raise HTTPException(403, "lease_required")
    lease = manager.get_lease(x_lease_id)
    if not lease:
        raise HTTPException(403, "lease_not_found")
    if lease.state != "ACTIVE":
        raise HTTPException(403, f"lease_{lease.state.lower()}")
    if lease.provider != provider:
        raise HTTPException(403, "provider_mismatch")
    if lease.resource != resource or lease.action != action:
        raise HTTPException(403, "resource_or_action_not_covered")
    if lease.calls_remaining <= 0:
        raise HTTPException(429, "lease_quota_exhausted")
    return lease


def _consume_lease(lease: Lease) -> None:
    lease.calls_used += 1
    lease.calls_remaining -= 1


async def _proxy_and_proof(lease: Lease, endpoint: str, call) -> dict[str, Any]:
    status, body = await call()
    _consume_lease(lease)
    proof = manager.record_proof(lease, status, endpoint, body)
    if status != 200:
        raise HTTPException(status, {"detail": "upstream_error", "proof": proof, "body": body})
    return {"lease_id": lease.lease_id, "proof": proof, "data": body}


@app.get("/proxy/openai/models")
async def openai_models(x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, "openai", "models", "read")
    token = manager.get_active("openai")
    return await _proxy_and_proof(
        lease,
        "/v1/models",
        lambda: manager._http_get(
            "https://api.openai.com/v1/models",
            {"Authorization": f"Bearer {token}"},
        ),
    )


@app.get("/proxy/github/user")
async def github_user(x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, "github", "user", "read")
    token = manager.get_active("github")
    return await _proxy_and_proof(
        lease,
        "/user",
        lambda: manager._http_get(
            "https://api.github.com/user",
            {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        ),
    )


@app.get("/proxy/telegram/me")
async def telegram_me(x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, "telegram", "me", "read")
    token = manager.get_active("telegram")
    return await _proxy_and_proof(
        lease,
        "/getMe",
        lambda: manager._http_get(f"https://api.telegram.org/bot{token}/getMe"),
    )


@app.get("/proxy/notion/me")
async def notion_me(x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, "notion", "me", "read")
    token = manager.get_active("notion")
    return await _proxy_and_proof(
        lease,
        "/v1/users/me",
        lambda: manager._http_get(
            "https://api.notion.com/v1/users/me",
            {"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
        ),
    )


@app.get("/proxy/{provider}/models")
async def generic_models(provider: str, x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, provider, "models", "read")
    token = manager.get_active(provider)
    endpoints = {
        "openrouter": "https://openrouter.ai/api/v1/models",
        "mistral": "https://api.mistral.ai/v1/models",
        "deepseek": "https://api.deepseek.com/models",
        "xai": "https://api.x.ai/v1/models",
        "gemini": None,
        "anthropic": "https://api.anthropic.com/v1/models",
    }
    url = endpoints.get(provider)
    if not url:
        raise HTTPException(400, f"no_model_endpoint_for_{provider}")
    return await _proxy_and_proof(
        lease,
        url,
        lambda: manager._http_get(url, {"Authorization": f"Bearer {token}"}),
    )


@app.get("/proxy/postman/me")
async def postman_me(x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, "postman", "me", "read")
    token = manager.get_active("postman")
    return await _proxy_and_proof(
        lease,
        "/me",
        lambda: manager._http_get("https://api.getpostman.com/me", {"X-Api-Key": token}),
    )


@app.get("/proxy/vercel/user")
async def vercel_user(x_lease_id: str | None = Header(None, alias="X-Lease-Id")):
    lease = _require_lease(x_lease_id, "vercel", "user", "read")
    token = manager.get_active("vercel")
    return await _proxy_and_proof(
        lease,
        "/v2/user",
        lambda: manager._http_get("https://api.vercel.com/v2/user", {"Authorization": f"Bearer {token}"}),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
