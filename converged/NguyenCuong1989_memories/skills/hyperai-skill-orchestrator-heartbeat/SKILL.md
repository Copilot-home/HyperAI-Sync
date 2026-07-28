---
name: hyperai-skill-orchestrator-heartbeat
description: Run the HyperAI skill-orchestrator heartbeat when the task mentions event-bus-first queue validation, HEARTBEAT_NO_EVENT, find-skills reachability, or the fixed EVENT_PACKET -> ACK_PACKET report shape.
argument-hint: "[automation-id-or-default]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# HyperAI Skill-Orchestrator Heartbeat

## When to use

Use for `hyperai-skill-orchestrator` heartbeat and queue-validation runs under `/Users/andy`.

Do not use for broad runtime repair, queue mutation, or cloud-backed routing work.

## Inputs / context to gather

1. Read the automation memory first:
   - default: `$CODEX_HOME/automations/hyperai-skill-orchestrator/memory.md`
   - if `$ARGUMENTS` provides another automation id, switch to that memory path.
2. Validate the required skill anchors:
   - `/Users/andy/.agents/skills/hyperai-runtime-orchestrator/SKILL.md`
   - `/Users/andy/.agents/skills/find-skills/SKILL.md`
3. Resolve the queue and telemetry anchors:
   - `/Users/andy/HyperAI-Sync/memory/runtime_execution_todo.md`
   - `/Users/andy/HyperAI-Sync/runtime/telemetry_router/reports/loop-summary.json`
   - `/Users/andy/HyperAI-Sync/runtime/telemetry_router/reports/router-run-report.json`

## Procedure

1. Read automation memory before any other probe.
2. Preserve the skill-first order:
   - execute `hyperai-runtime-orchestrator` first
   - then validate `find-skills` reachability
3. Fail fast on missing anchors with `SKILL_ANCHOR_MISSING`.
4. Run the lightweight router verification:
   - `python3 /Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py verify.run`
5. Use `npx skills --help` as the minimal live probe for `find-skills`.
6. Inspect the queue anchor for executable pending-event fields:
   - `event_id`
   - `status=pending`
   - `priority`
   - `intent`
7. If the queue lacks that schema, return `HEARTBEAT_NO_EVENT` and stop.
8. Emit the fixed output order:
   - `EVENT_PACKET`
   - `SKILL_ROUTING_TABLE`
   - `ACTION_PACKET`
   - `VERIFY_PACKET`
   - `ACK_PACKET`
   - `Next single action`
9. If the workflow expects it, append a compact run note to the automation memory.

## Efficiency plan

- Stop immediately after anchor validation if a required skill path is missing.
- Stop immediately after queue inspection when the pending-event schema is absent.
- Use telemetry files as health/status evidence only; do not treat them as runnable events.
- Reuse `verify.run` plus `npx skills --help` instead of widening into shell-first scanning.

## Pitfalls and fixes

- Symptom: queue file contains mission notes but no executable packet.
  - Likely cause: the heartbeat is running without a real pending event.
  - Fix: return `HEARTBEAT_NO_EVENT`; do not mutate the queue or widen the scan.
- Symptom: `find-skills` seems unavailable from shell.
  - Likely cause: the stable live probe in this environment is not a direct shell alias.
  - Fix: use `npx skills --help`.
- Symptom: telemetry shows `status: pass`, but no event is runnable.
  - Likely cause: router health was mistaken for queue readiness.
  - Fix: require the explicit pending-event schema before treating the queue as actionable.
- Symptom: automation memory patch fails at end of file.
  - Likely cause: the file tail changed between reads.
  - Fix: re-read the tail and append a new dated block instead of patching from a stale excerpt.

## Verification checklist

- Automation memory was read first.
- Both required skill anchors were checked.
- `verify.run` and `npx skills --help` were used or explicitly marked unverified.
- Queue inspection explicitly checked for `event_id`, `status=pending`, `priority`, and `intent`.
- Terminal state is one of `SKILL_ANCHOR_MISSING`, `EVENT_SCHEMA_INVALID`, `HEARTBEAT_NO_EVENT`, or `NO_SKILL_DELTA`.
- Output stayed packetized and ended with one next action.
