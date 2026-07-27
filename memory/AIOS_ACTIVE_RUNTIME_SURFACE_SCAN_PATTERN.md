# AIOS Active Runtime Surface Scan Pattern

Date: 2026-04-16

## Purpose

This pattern makes active app/runtime discovery repeatable. It prevents important local AI apps such as AIServer, Ollama, Codex, OpenClaw, MCP bridges, VS Code surfaces, and HyperAI product runtimes from being missed or treated as unrelated processes.

## Rule

Every active process is only a candidate surface until it has:

```text
process proof + port proof + path proof + phi_i(M) mapping + open gate
```

Authority remains:

```text
Authority(X)=1 iff Proof(X)=valid and phi_X(M) mapped and Gate(X)=open
```

## Scan Pipeline

```text
Win32_Process
-> listening TCP ports
-> command line / executable path
-> package or repo path
-> runtime_class
-> lane_class
-> allowed roles
-> forbidden roles
-> proof hints
-> memory registry
```

## Runtime Classes

- `app_backend_runtime`: product backend, for example `backend/server.js` on `5000`.
- `app_frontend_runtime`: product frontend/static shell, for example `4173`.
- `provider_facade`: local fakeOpenAPI or compatibility API, for example QuantumReason on `8000`.
- `local_model_substrate`: local model host, for example AIServer/Ollama on `11434`.
- `operator_control_surface`: control runtime, for example OpenClaw on `18789`.
- `desktop_operator_runtime`: Codex/ChatGPT-like local operator app.
- `editor_operator_surface`: VS Code/Insiders extension host and WebView surface.
- `tool_bridge`: MCP, Playwright, Postman, or connector process.
- `script_runtime`: Node/Python process that needs path-specific classification.

## Required Tool

Run:

```powershell
python tools\aios_runtime_surface_scan.py --print-summary
```

Default output:

```text
runtime/federation_orchestrator/active_runtime_surface_scan_20260416.json
```

## Safety

The scanner is read-only. It must not:

- kill processes
- restart services
- delete extensions
- reset Docker
- reset WSL
- mutate OS state
- mutate cloud state

## Binding Rule

Newly detected surfaces are appended to ecosystem memory only after readback proof. A process name alone is not enough. A port alone is not enough. A package label alone is not enough.

## Next Use

Use this pattern before broad claims like:

```text
all app runtimes are connected
all AI servers are local-first
provider fabric is complete
```

If a surface is detected but unmapped, classify it as `observed_process` and leave authority closed.
