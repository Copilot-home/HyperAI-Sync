# AIOS Tool Runtime Surface Matrix

Date: 2026-04-15

This matrix maps active and observed AIOS surfaces into the model-native runtime contract.

| Surface | Runtime role | Current status | Allowed role | Forbidden role | Proof source | Next safe action |
| --- | --- | --- | --- | --- | --- | --- |
| Titan GT77 Windows root | root-host substrate | active root host | preserve, read-only probe, evidence ledger | OS reset, purge, destructive repair | local command/runtime artifacts | keep root conservation gate |
| `hyperai-user-control-system/backend/server.js` | app backend authority | live on `5000` | runtime truth for app backend | cloud/provider authority | runtime manifest and port probe | preserve process-first checks |
| Frontend static server | app frontend authority | live on `4173` | browser shell proof surface | backend authority | runtime manifest and port probe | smoke only when route/UI changes |
| QuantumReason fakeAPI | provider fabric | source exists in `C:\Users\pc\aidev\quantumreason_v3` | OpenAI-compatible local facade | deception, provider identity bypass, cloud authority | `api_server.py`, `llm_orchestrator.py` | route provider requests through facade |
| Ollama local models | local model substrate | model list observed | local inference candidates | shell authority, proof authority | `ollama list` | inventory only until request-specific proof |
| Docker Desktop | infrastructure substrate | client installed, daemon pipe unavailable | degraded observation | expansion base, reset/purge target | `docker version` error | no Docker repair in this phase |
| WSL / HCS | infrastructure substrate | unavailable/degraded | degraded observation, route-around trigger | `wsl --unregister`, WSL reset, HCS destructive repair | copied terminal error and local status | route execution to remote/API/tool substrate |
| VS Code / Insiders | operator/tool surface | installed and extension-heavy | approval intake, editor surface, read-only support | shell authority by label | prior logs and policies | keep degraded-shell policy |
| Codex desktop/runtime | operator cockpit | active conversation surface | governed local work execution | OS/cloud authority | current session and local skill rules | reduce creator manual burden safely |
| Gemini extensions | tool-extension substrate | multiple repos observed, mostly dirty install metadata | preserve extension graph | uninstall/normalize by default | git inventory | classify before sync |
| Postman/API clients | API probe surface | not live-probed in this phase | endpoint verification, collection replay, contract evidence | authority or evidence recorder by label | exported collection/run result when available | classify when evidence exists |
| MCP connectors | tool bridge / capability node | active workspace contract, connector-specific | task-specific read/write under contract, docs/proof bridge | connector deletion, hidden authority promotion, broad cleanup | MCP operation log or generated artifact | preserve and bind outputs to proof/memory |
| SSH remote hosts | remote execution host | not inventoried in this phase | host identity probe, bounded command, artifact pullback | destructive remote repair, credential extraction, root mutation without rollback | future command transcript and host identity | inventory only after explicit target exists |
| GitHub Codespaces | disposable cloud dev substrate | not inventoried in this phase | isolated build/test/proof in clean clone | root-host replacement, secret exfiltration, dirty repo override | future repo/branch/commit and command transcript | use for proof when local Docker/WSL blocks build substrate |
| GitHub Actions | CI proof substrate | CI contract exists, remote run not queried in this phase | workflow proof, build/test artifact | runtime authority without deployment contract | future workflow run URL/log/artifact | keep as proof lane, not runtime authority |
| Git | sync transport | many repos, many dirty | compare, ledger, sync transport | automatic authority, dirty pull/push/reset | git inventory | MacBook same-schema inventory |
| GCP cloud substrate | observed cloud substrate | MacBook copied evidence, Titan `gcloud` not in PATH | read-only inventory, bounded proof jobs after contract | direct execution authority, IAM/billing/service mutation by assumption | copied terminal log and cloud observation artifact | same-schema cloud inventory |
| MacBook | secondary workstation | copied evidence only | peer inventory source | Titan live truth replacement | creator-provided log | produce same-schema read-only inventory |
| Archive/vault copies | archive-sediment | many duplicate nested strata | preserve, classify, compare | delete/merge/normalize | git inventory | no direct sync |

## Model-Native Rule

Each surface must be mapped as `phi_i(M)` before execution. A surface may be useful without being authority.

## Current Constraints

- Docker is degraded and cannot be used as runtime expansion base.
- Docker/WSL degradation must route execution to cloud/SSH/Codespaces/MCP/Postman/API substrates when a proof contract exists.
- GCP is observed-only until live/same-schema inventory exists.
- Dirty Git repos cannot be pulled, pushed, reset, or cleaned.
- Physical folder standardization remains logical-registry only.

## Route-Around Rule

When local container or VM substrates are unavailable, keep the app runtime alive and choose the narrowest alternate lane:

```text
reuse_default_runtime
-> local fakeAPI/provider facade
-> Postman/API probe
-> MCP connector
-> GitHub Actions/Codespaces proof
-> SSH remote host
-> cloud provider substrate
```

Each route requires evidence output and must not silently mutate root host, cloud authority, Git state, or extension graph.
