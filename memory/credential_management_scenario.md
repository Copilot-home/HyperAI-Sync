# HyperAI Credential Management Scenario

## Mission
Securely manage, validate, and broker key/token capabilities for the AI ecosystem of Nguyễn Đức Cường, aligned with APΩ canon.

## Entrypoint
```bash
cd /Users/andy/HyperAI-Sync

# Start the APΩ credential broker
python tools/hyperai_credentials_service.py
# or
uvicorn tools.hyperai_credentials_service:app --host 127.0.0.1 --port 8765
# or Docker
# docker compose up --build -d hyperai-credentials
```

## Secure storage
- Master credentials are parsed from the creator's credential dump and stored in
  `~/.config/hyperai/credentials.env` (file mode `0600`, directory `0700`).
- This file is **outside** all git repositories and is never written as a project artifact.
- The source dump in `/Users/andy/# Quản lý CREDENTIALS - Hệ thống AI của Nguyễn Đức Cường/`
  should be removed once the secure export is confirmed (explicit approval required).

## APΩ architecture
The broker implements the canon in `memory/APΩ_CREDENTIAL_CANON.md`:
- Ω decides admissibility; the broker is the vault/execution surface that materializes leases.
- A credential \(\kappa\) is not treated as a raw string; it is validated and bound to
  `(node, task, provider, resource, action, scope, TTL)`.
- Plaintext secrets never appear in logs, memory, or API responses.

## Loader behavior
`tools/hyperai_credentials_loader.py`:
1. Reads the creator credential markdown.
2. Extracts and labels keys/tokens by provider (OpenAI, Anthropic, GitHub, Docker, etc.).
3. Decodes `MISC_ENCODED_DATA` (zlib JSON) and flattens it.
4. Sanitizes polluted lines (e.g., Telegram token followed by Markdown links).
5. Deduplicates exact secret values, keeping the first canonical key.
6. Writes a clean `.env` to `~/.config/hyperai/credentials.env` with mode `0600`.
7. `--load` sets `os.environ` for all keys and aliases `GH_TOKEN`/`GITHUB_TOKEN` to the active `GITHUB_PAT`.
8. Never prints secret values; `--summary` only emits key names and counts.

## Broker behavior
`tools/hyperai_credentials_service.py` (FastAPI + uvicorn):
- Loads `~/.config/hyperai/credentials.env` and validates every configured provider.
- For each provider, tries all candidate keys and keeps the first valid one as active.
- `POST /capability` evaluates the Adm\(_\Omega\) function:
  - Identity, Canon, Proof, Policy/Scope, Budget, TTL, Drift.
- If `ALLOW`, issues a lease with `lease_id`, `active_key_ref`, `masked_key`, `scope`, `expires_at`.
- All `/proxy/*` endpoints require `X-Lease-Id`; they verify the lease scope and execute the upstream call.
- The broker records proof metadata (status, endpoint, content SHA-256, timestamp) per call, never the secret.
- Background task expires old leases every 30s.

## API quick reference
```bash
# Broker status
curl http://127.0.0.1:8765/status

# Request a capability lease
curl -s -X POST http://127.0.0.1:8765/capability \
  -H 'Content-Type: application/json' \
  -d '{"node":"hyperai-worker","task":"list-models","provider":"openai","resource":"models","action":"read","scope_req":["read"],"ttl_req":60}'

# Use the returned lease_id to call a proxy endpoint
curl -s -H 'X-Lease-Id: <lease_id>' http://127.0.0.1:8765/proxy/openai/models

# Revoke a lease early
curl -s -X DELETE http://127.0.0.1:8765/capability/<lease_id>

# Read the APΩ canon
curl http://127.0.0.1:8765/canon
```

## Constraints
- No bulk credential harvesting.
- No printing/logging real secrets.
- No hardcoded tokens in source.
- No cloud/Git mutation without explicit gate.
- Real secrets must come from the creator through secure channels.
- Leases are short-lived, task-bound, and never transferable between tasks.

## Current Progress
- [x] HyperAI OODA loop activated and route plan generated.
- [x] MCP-Ecosystem instance configs copied into `runtime/mcp_registry/` with placeholder token redacted.
- [x] `.env.example` templates created in canonical project directories.
- [x] Git remote URL audit: 0 embedded-token leaks found after sanitization.
- [x] `gh` authenticated for `NguyenCuong1989` with a valid classic PAT, broad scopes.
- [x] `gh auth setup-git` configured so `git` HTTPS operations use `gh` keychain.
- [x] `git config user.name` and `user.email` aligned with canonical author identity.
- [x] `hyperai_credentials_loader.py` created and tested; secure credential file generated.
- [x] `hyperai_credentials_service.py` upgraded to APΩ credential broker with lease, admissibility, and proof.
- [x] Docker / docker-compose files created.
- [x] APΩ canon preserved in `memory/APΩ_CREDENTIAL_CANON.md` and served at `/canon`.
- [x] `GITHUB_PAT`, `OPENAI_API_KEY_3`, `TELEGRAM_BOT_TOKEN`, `NOTION_API_KEY`, `MISTRAL_API_KEY`, `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY`, `VERCEL_TOKEN`, `POSTMAN_API_KEY_ALT1` verified live.
- [x] `tools/hyperai_credential_client.py` created for programmatic broker access.
- [x] `tools/hyperai_agent_worker_loop.py` and `tools/hyperai_ooda_loop.py` wired to request capabilities and execute proxy calls through the broker.
- [x] `.devin/skills/hyperai-credential-broker/SKILL.md` created so Devin knows to use the broker instead of reading `.env`.
- [x] HyperAI OODA closure and proof artifacts generated.

## Verified Capabilities
- `python tools/hyperai_credentials_loader.py --load` sets 80+ keys/tokens into the environment.
- `POST /capability` returns `ALLOW`/`DENY` with per-check breakdown.
- `GET /proxy/openai/models` with `X-Lease-Id` returns 123 models and a content-hash proof.
- `GET /proxy/github/user` with `X-Lease-Id` returns `NguyenCuong1989` profile and proof.
- Proxy without `X-Lease-Id` returns `403 lease_required`.
- Bad node / bad action / bad scope returns `DENY` with reason.
- `python tools/hyperai_credential_manager.py --all` reports `ok: true` and `git_leaks_found: 0`.

## Known unhealthy keys (expected)
- `OPENAI_API_KEY` / `_1` / `_2` → 403; broker falls back to `OPENAI_API_KEY_3`.
- `GITHUB_PAT_2` → `_5` (fine-grained) → 401; broker uses `GITHUB_PAT`.
- `GEMINI_API_KEY_1` → `_5` → 400 `API_KEY_INVALID`.
- `DOCKER_ORG_ACCESS_TOKEN` → 401.
- `XAI_API_KEY`, `CLAUDE_ADMIN_KEY` → invalid for the tested endpoints.

## Next Action
- Confirm deletion or encryption of the original plaintext credential dump.
- Rotate the broken/expired tokens when convenient.
- Start Docker Desktop and run `docker compose up --build -d hyperai-credentials` to verify containerized broker.
- Wire HyperAI agents/skills to request capabilities through `POST /capability` instead of reading `.env` directly.
