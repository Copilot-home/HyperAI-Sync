# hyperai-credential-broker

## When to use

Use this skill when a HyperAI agent, worker, or tool needs to use an API key, token, or secret for any external provider (OpenAI, GitHub, Telegram, Notion, Mistral, OpenRouter, DeepSeek, Vercel, Postman, etc.).

Do NOT read `.env` files, `~/.config/hyperai/credentials.env`, or any other secret store directly. Always go through the broker.

## What it does

The HyperAI Credential Broker is a FastAPI service at `http://127.0.0.1:8765` that implements the APΩ credential canon (`memory/APΩ_CREDENTIAL_CANON.md`):

- Validates all configured provider keys on startup and keeps the first valid key as active.
- Evaluates an `Admissible_Ω` check for every capability request.
- Issues short-lived, task-bound leases that never contain plaintext secrets.
- Executes upstream API calls on behalf of a lease.
- Records proof metadata (status, endpoint, content SHA-256, timestamp) per call.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Service info |
| GET | `/status` | Active keys, validation health, lease counts |
| GET | `/state` | Credential state-machine counts and active leases |
| GET | `/canon` | Raw APΩ credential canon markdown |
| POST | `/refresh` | Re-validate all provider keys |
| POST | `/capability` | Request a scoped lease |
| GET | `/capability/{lease_id}` | Inspect a lease |
| DELETE | `/capability/{lease_id}` | Revoke a lease early |
| GET | `/proxy/{provider}/{endpoint}` | Execute a provider call using `X-Lease-Id` |

## How to request a capability

```bash
curl -s -X POST http://127.0.0.1:8765/capability \
  -H 'Content-Type: application/json' \
  -d '{
    "node": "hyperai-worker",
    "task": "list-openai-models",
    "provider": "openai",
    "resource": "models",
    "action": "read",
    "scope_req": ["read"],
    "ttl_req": 60
  }'
```

Response (success):

```json
{
  "decision": "ALLOW",
  "lease": {
    "lease_id": "lease-...",
    "active_key_ref": "OPENAI_API_KEY_3",
    "masked_key": "<REDACTED>",
    "expires_at": "...",
    "calls_remaining": 60
  }
}
```

Response (deny):

```json
{
  "decision": "DENY",
  "reason": "checks_failed: identity,policy,scope",
  "checks": { "identity": false, ... }
}
```

## How to execute a provider call

Use the `lease_id` from `/capability`:

```bash
curl -s -H 'X-Lease-Id: lease-...' http://127.0.0.1:8765/proxy/openai/models
```

Allowed proxy routes:

- `/proxy/openai/models`
- `/proxy/github/user`
- `/proxy/telegram/me`
- `/proxy/notion/me`
- `/proxy/openrouter/models`
- `/proxy/mistral/models`
- `/proxy/deepseek/models`
- `/proxy/xai/models`
- `/proxy/postman/me`
- `/proxy/vercel/user`

## Rules

1. Never return or log a plaintext secret.
2. Every proxy call must carry a valid `X-Lease-Id`.
3. A lease is bound to one `(node, task, provider, resource, action)` tuple.
4. If the active key for a provider is broken, the broker tries the next candidate automatically.
5. If no valid key exists, the broker returns `DENY` or `no_active_<provider>_key`.

## Starting the broker

```bash
cd /Users/andy/HyperAI-Sync
python tools/hyperai_credentials_service.py
```

or with Docker (when Docker Desktop is running):

```bash
docker compose up --build -d hyperai-credentials
```

## Python access

```python
from tools.hyperai_credentials_service import manager, CapabilityRequest
import asyncio

req = CapabilityRequest(
    node="hyperai-worker",
    task="list-models",
    provider="openai",
    resource="models",
    action="read",
    scope_req=["read"],
    ttl_req=60,
)

async def main():
    lease_or_decision = await manager.issue_lease(req)
    print(lease_or_decision)

asyncio.run(main())
```
