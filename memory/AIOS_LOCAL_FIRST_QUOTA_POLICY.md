# AIOS Local-First Quota Policy

Date: 2026-04-16

## Purpose

This policy prevents AIOS app runtimes, VS Code extensions, MCP sampling lanes, and editor copilots from silently falling back to quota-limited cloud accounts when local AI substrate is available.

The default model route is:

```text
app/runtime request
-> local fakeOpenAPI facade
-> local provider router
-> Ollama/local model
-> proof metadata
-> optional cloud only after explicit gate
```

## Current Proof

Measured local substrate:

- Ollama listens on `127.0.0.1:11434`.
- QuantumReason fakeOpenAPI listens on `127.0.0.1:8000`.
- Product backend remains live on `127.0.0.1:5000`.
- Product frontend remains live on `127.0.0.1:4173`.
- `GET /api/v2/health` on the fakeOpenAPI facade returns `status = healthy`.
- `POST /api/v2/chat/completions` resolves `qwen2.5-coder:1.5b` with `provider = local`.
- The fakeOpenAPI auth shim accepts both `X-API-Key` and `Authorization: Bearer` for the same local API key.
- AIServer is present as a packaged local model substrate on `11434` with an internal runner health endpoint observed on `51852`.

## Quota-Pressure Sources

These surfaces are preserved but must not auto-consume cloud quota by default:

- GitHub Copilot completion and next edit suggestions.
- Copilot chat autofix and Copilot-hosted web search.
- MCP server sampling with `copilot/*` models.
- Gemini Code Assist automatic inline suggestions and YOLO agent mode.
- GitLens AI defaults that route to Copilot or Gemini.

## AIServer Binding

`AI Server` / `LocalAIs.com.AIServer` is part of the local substrate, not a cloud quota lane.

Current role:

```text
AIServer/Ollama 11434
-> QuantumReason local provider
-> fakeOpenAPI 8000
-> app runtime clients
```

It should be preserved and routed through the facade unless a task explicitly needs direct Ollama-compatible calls. Detailed trace: `memory/AIOS_AISERVER_RUNTIME_TRACE_20260416.md`.

## Default Operator Settings

VS Code Insiders should prefer the local OpenAI-compatible facade:

```text
chatgpt.gpt3.provider = custom
chatgpt.gpt3.apiBaseUrl = http://127.0.0.1:8000/api/v2
chatgpt.gpt3.reasoning.provider = custom
chatgpt.gpt3.reasoning.apiBaseUrl = http://127.0.0.1:8000/api/v2
```

Quota-heavy auto lanes should be disabled, not uninstalled:

```text
github.copilot.enable.* = false
github.copilot.nextEditSuggestions.enabled = false
github.copilot.chat.agent.autoFix = false
github.copilot.chat.anthropic.tools.websearch.enabled = false
geminicodeassist.inlineSuggestions.enableAuto = false
geminicodeassist.agentYoloMode = false
chat.mcp.serverSampling.*.allowedModels = []
```

GitLens cloud model defaults should be absent unless a task explicitly opens a cloud lane with proof.

## Auth Compatibility Rule

Local fakeOpenAPI must accept both common client shapes:

```text
X-API-Key: <local key>
Authorization: Bearer <local key>
```

This prevents OpenAI-compatible extensions from failing local auth and then falling back to quota-limited provider accounts.

## Allowed Cloud Use

Cloud provider calls are allowed only when all are true:

- The task is bound to a mission.
- Local facade or local model cannot satisfy the task.
- The cloud lane has an open gate.
- The provider, model, project, and expected quota cost are explicit.
- Evidence is written after the call.

## Blocked Defaults

Do not allow by default:

- Hidden cloud fallback after a local auth mismatch.
- Automatic Copilot/Gemini sampling from MCP servers.
- Auto-fix loops that call cloud models without a mission.
- Web search tools that consume cloud quota without explicit intent.
- Extension uninstall, MCP deletion, Docker reset, WSL reset, or OS mutation as a quota fix.

## Failure Classes

- `local_facade_down`: port `8000` or `/api/v2/health` is unavailable.
- `local_auth_mismatch`: local facade rejects common OpenAI-compatible auth.
- `quota_lane_leak`: a preserved extension still auto-calls Copilot, Gemini, or another cloud model.
- `provider_route_drift`: app settings point local but provider metadata reports cloud.
- `proof_missing`: quota mitigation is claimed without a port, health, or completion probe.

## Next Safe Action

Keep the local fakeOpenAPI process alive for active operator sessions and add app-specific local facade bindings only after each app's configuration schema is read. Preserve all extension and MCP nodes while preventing hidden cloud auto-use.
