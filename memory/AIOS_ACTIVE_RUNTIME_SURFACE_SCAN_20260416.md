# AIOS Active Runtime Surface Scan 2026-04-16

## Scope

Read-only host scan using `tools/aios_runtime_surface_scan.py`.

Output artifact:

```text
runtime/federation_orchestrator/active_runtime_surface_scan_20260416.json
```

## Scan Result

Total AI/runtime-related surfaces detected: `60`.

Class distribution:

| runtime_class | count | interpretation |
| --- | ---: | --- |
| `local_model_substrate` | 18 | AIServer, Ollama, Ollama/AIServer WebView children, local model serving substrate |
| `tool_bridge` | 24 | MCP / Playwright / connector bridge processes |
| `desktop_operator_runtime` | 6 | Codex app runtime and subprocesses |
| `cloud_ai_operator_surface` | 7 | Microsoft Copilot / M365 Copilot and WebView children; observer/user surface only |
| `operator_control_surface` | 2 | OpenClaw gateway/control wrapper surface |
| `provider_facade` | 1 | QuantumReason fakeOpenAPI on `8000` |
| `app_backend_runtime` | 1 | HyperAI backend `backend/server.js` on `5000` |
| `app_frontend_runtime` | 1 | HyperAI frontend static shell on `4173` |

No `unknown_process` remains after tightening scanner heuristics.

## Durable Runtime Anchors

```text
5000  -> HyperAI backend runtime truth, backend/server.js
4173  -> HyperAI frontend static shell
8000  -> QuantumReason fakeOpenAPI provider facade
11434 -> AIServer/Ollama local model substrate
18789 -> OpenClaw gateway
18791 -> OpenClaw browser sidecar
```

## Interpretation

AIServer and Ollama are local model substrate under the provider fabric. They should be connected through:

```text
AIServer/Ollama 11434
-> QuantumReason local provider
-> fakeOpenAPI 8000
-> app/runtime clients
```

Codex and VS Code/Insiders remain operator/cockpit surfaces. MCP/Playwright processes are tool bridges. Microsoft Copilot/M365 Copilot are observed cloud AI operator surfaces and must not be treated as local quota-free provider substrate.

## Promotion Rule

Every detected surface remains closed for authority promotion unless:

```text
Proof(X)=valid
phi_X(M) mapped
Gate(X)=open
```

## Safety Result

The scan did not:

- kill processes
- restart services
- delete extensions
- reset Docker
- reset WSL
- mutate OS state
- mutate cloud state

## Next Safe Action

Use `tools/aios_runtime_surface_scan.py --print-summary` as the default pre-task host scan whenever a task needs to attach, route, or normalize local app runtimes. New high-signal surfaces should be added to the heuristic map before being promoted into the ecosystem registry.
