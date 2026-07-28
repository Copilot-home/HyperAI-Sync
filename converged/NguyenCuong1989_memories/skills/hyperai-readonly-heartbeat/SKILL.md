---
name: hyperai-readonly-heartbeat
description: Run a read-only HyperAI or AIOS heartbeat when the task asks for router verification, MCP anchor checks, local Ollama reachability, queue inspection, or delta-only packetized output.
argument-hint: "[automation-id]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# HyperAI Read-Only Heartbeat

## When to use

Use for `hyperai-autonomous-runtime-heartbeat` style tasks and similar read-only heartbeat checks under `/Users/andy`.

Do not use for runtime repair, service restarts, queue mutation, or cloud-backed investigation.

## Inputs / context to gather

1. Read the matching automation memory first:
   - default: `$CODEX_HOME/automations/hyperai-autonomous-runtime-heartbeat/memory.md`
   - if `$ARGUMENTS` provides another automation id, switch to that memory path.
2. Confirm the user still wants read-only behavior and delta-only reporting.
3. Resolve the named anchors:
   - `AIOS_MISSION_ROUTER`
   - `127.0.0.1:11434/api/tags`
   - `127.0.0.1:11435/api/tags`
   - `127.0.0.1:9999/health`
   - `/Users/andy/HyperAI-Sync/memory/runtime_execution_todo.md`

## Procedure

1. Read the automation memory first and recover prior deltas/broken anchors.
2. Verify the router/tool surface:
   - confirm `AIOS_MISSION_ROUTER` is available
   - run `aios_memory_load`, `aios_verify_run`, and `aios_eec_check` when exposed
3. Probe the local endpoints with narrow curls only.
4. Read the queue head from `runtime_execution_todo.md`.
5. Compare against the prior run and report only:
   - deltas
   - broken anchors
   - next single safe step
6. If the workflow requires an automation memory append, write a compact note with anchor status and next step only.

## Efficiency plan

- Do not broaden scope beyond router, endpoints, and queue.
- Reuse prior memory notes to focus on deltas instead of restating the whole system state.
- If no tool output is available, stop at the contract/checklist level and avoid implying verification.

## Pitfalls and fixes

- Symptom: the heartbeat turns into a broad system audit.
  - Likely cause: the named check list was treated as optional.
  - Fix: stay on router, MCP, Ollama, and queue only.
- Symptom: a rollout contains the heartbeat request but no probe output.
  - Likely cause: the transcript preserved instructions, not execution.
  - Fix: record the checklist and constraints only; do not claim success.
- Symptom: the report becomes a long narrative.
  - Likely cause: delta-only output was ignored.
  - Fix: emit concise packetized fields and one next action.

## Verification checklist

- Automation memory was read first.
- Router/tool availability and the three local endpoints were checked or explicitly marked unverified.
- Queue head was inspected at `runtime_execution_todo.md`.
- Output contains only deltas, broken anchors, and next single safe step.
- Any memory append is compact and delta-only.

