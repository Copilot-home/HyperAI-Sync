# AIOS Local LLM x Telegram Coordination

Date: 2026-04-18

## Purpose

This artifact locks the next phase after Telegram mastery:

```text
Local_Model_Coordination_for_Telegram
```

The goal is not to add a new product or packet. The goal is to connect existing
local systems so packet success rate increases under the same proof-only law.

## Coordination Topology

```text
Router -> Specialist -> Verifier -> Telegram Executor -> Auditor
```

Roles:

- Router
  - classify runtime input into the active packet state
- Specialist
  - produce packet-local drafts or structured evidence
- Verifier
  - reject claims or actions that exceed proof or packet order
- Telegram Executor
  - execute only after verifier allow
- Auditor
  - record proof status, no-progress, blocker, and next action

## Phase Rules

- no new product line
- no sixth packet
- no bot-as-oracle
- no authority without `ooda_control_contract`
- no claim beyond proof

## Binding To Current Telegram Mastery Phase

The active packet remains controlled by:

- `runtime/federation_orchestrator/telegram_mastery_equation.json`
- `runtime/federation_orchestrator/ooda_control_contract.json`

Local model coordination must never override:

- `current_variable`
- `current_packet`
- `blocking_factor`
- `success_condition`

It may only improve:

- packet parsing quality
- blocker clarity
- draft quality
- verification rigor
- audit trace closure

## Default Local Role Assignment

- router model
  - `qwen3:4b`
- specialist model
  - `qwen2.5-coder:1.5b`
- verifier surface
  - `codex_operator_runtime`
- auditor model
  - `deepseek-r1:1.5b`
- telegram executor
  - `telegram_bot_lane`

These defaults are subordinate to proof and runtime availability.
