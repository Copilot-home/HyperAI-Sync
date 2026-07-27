# AIOS runtime and economy ecosystem map - 2026-04-15

## Scope

This artifact resumes ecosystem planning after the root-host conservation decision. It maps the current AIOS/HyperAI runtime layers and the existing AI economy documents without resetting Windows, Docker, WSL, or the operating host.

## Root constraint

The Windows machine is the root host. All runtime and economy planning must preserve it.

Binding warning:

- `memory/AIOS_ROOT_HOST_CONSERVATION_WARNING_20260415.md`

Current substrate blocker:

- Windows admin/service authority is degraded.
- Docker/WSL/HCS is unavailable.
- HyperAI local runtime policy currently reports `hold_core_degraded`, `recoverable`, and `operator_attention_required`.

Planning implication:

- Do not add heavy runtimes.
- Do not run Docker rebuild/reset workflows.
- Prefer inventory, document consolidation, and low-cost runtime probes.
- Treat economy execution as paused until shell/runtime proof is stable enough for publish/funding confirmation.

## Runtime ecosystem layers

### Layer 1 - Root host substrate

Role:

- physical Windows host
- filesystem root for source lineage, memory, local models, tool identity, and runtime artifacts

Key surfaces:

- Windows services: `vmcompute`, `LxssManager`, `hns`, `com.docker.service`
- user/admin authority: `AI\pc`, `AI\nguye`, `AI\Administrator`
- shell profile and PowerShell language mode
- Docker Desktop and WSL2

Current state:

- degraded
- conservation-critical

### Layer 2 - Canonical app shell authority

Role:

- browser/app boundary and runtime authority for the active product surface

Key surfaces:

- `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`
- backend authority: `backend/server.js`
- frontend authority: static SPA server on `4173`
- CI authority: `.github/workflows/ci.yml`

Current state:

- historically proven autonomous on `5000/4173`
- currently degraded by Windows/runtime substrate and `esbuild spawn EPERM`
- should not be replaced by Docker, Telegram, QuantumReason, or archive roots

### Layer 3 - Federation and orchestration

Role:

- registry-first routing and degradation policy
- runtime identity and approval routing
- memory-governed coordination

Key surfaces:

- `tools/federation_orchestrator.py`
- `runtime/federation_orchestrator/unified_registry.json`
- `runtime/federation_orchestrator/workflow_registry.json`
- `runtime/federation_orchestrator/revenue_policy.json`
- `runtime/federation_orchestrator/revenue_metrics.json`
- `runtime/federation_orchestrator/approval_requests.json`
- `runtime/federation_orchestrator/creator_surface_policy.json`

Current state:

- usable for planning and registry refresh
- shell registry must be read as degraded when `hyperai_autonomous_cycle.py` reports `hold_core_degraded`

### Layer 4 - Reasoning/provider fabric

Role:

- bounded reasoning, ranking, summarization, formatting
- no shell authority

Key surfaces:

- `C:\Users\pc\aidev\quantumreason_v3`
- `tools/llm_augmentation.py`
- Ollama local provider when available

Current state:

- historically proven through local model `qwen2.5-coder:1.5b`
- not a safe expansion target while root substrate is degraded

### Layer 5 - Economy execution

Role:

- creator-reviewed value generation
- Telegram distribution
- receive-only treasury/funding evidence

Key surfaces:

- `tools/deal_value_engine.py`
- `tools/deal_intelligence_loop.py`
- `tools/telegram_relay.py`
- `tools/treasury_control.py`
- `tools/phase_treasury_a1.py`
- `runtime/deal_value_engine/`
- `runtime/telegram_node/`
- `runtime/treasury/`

Current state:

- first-dollar path exists
- first dollar not achieved
- current objective state: `awaiting_publish_evidence`

## Existing economy canon

### `memory/FIRST_DOLLAR_RUNBOOK.md`

Canonical rule:

- `event -> evidence -> ledger -> metric`

Meaning:

- revenue metrics are invalid unless backed by ledger events
- creator confirms facts, not business truth
- first dollar flips only after confirmed funding amount greater than zero

### `memory/PHASE_TREASURY_A1_FIRST_DOLLAR_REVENUE_PATH.md`

Implemented:

- receive-only treasury boundary
- Telegram relay lane
- A1 phase-state
- approval requests
- creator-surface policy
- first-dollar runbook

Known gaps:

- no live publish confirmation
- no live funding confirmation
- Telegram target remains unproven
- TON remains manual receive evidence only

### `memory/DEAL_INTELLIGENCE_LOOP_CANON.md`

Canonical loop:

- `deal_filter`
- `deal_rank`
- `deal_format`

Rules:

- one deal equals one post
- creator approval required
- QuantumReason is reasoning-only
- shell authority is not moved

### `memory/PHASE_4E_FEDERATION_VALUE_ENGINE_AND_SELF_FUNDING_LOOP.md`

Workflow:

- `source_ingest`
- `candidate_normalize`
- `deal_filter`
- `deal_rank`
- `creator_review`
- `deal_format`
- `artifact_publish_ready`
- `feedback_capture`

Proven artifact:

- `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`

### `memory/PHASE_RECOVERY_A_RUINS_AUDIT_AND_REVENUE_RECOVERY.md`

Recovery target strategy:

1. recover viable legacy surfaces
2. publish-ready listing/update artifacts
3. Telegram relay
4. funding confirmation

Top recovery targets:

- `hyperai-phoenix` VS Code extension
- `hyperai-companion` VS Code extension lineage
- `core_system` marketplace pipeline

### `memory/TELEGRAM_CORE_ARCHITECTURE_MAP.md`

Telegram boundary:

- Telegram is subordinate execution fabric
- TON is receive-evidence ledger surface
- shell authority remains above Telegram lanes

Current blocker:

- no proven reachable Telegram target for the current bot lane

## Current economy state from runtime artifacts

Revenue metrics:

- `artifact_ready_count = 1`
- `publish_relay_ready_count = 1`
- `published_count = 0`
- `funding_pending_count = 1`
- `funding_confirmed_count = 0`
- `first_dollar_achieved = false`

Current A1 phase:

- `objective_state = awaiting_publish_evidence`
- `next_valid_operator_action = publish_confirm`
- active publish event: `publish-20260403004302`
- active funding event: `funding-pending-uber-egift-20260403004325`
- artifact: `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`

## Planning decision

The next economy work should not be new product expansion. It should be consolidation and proof recovery:

1. stabilize the root host enough to run low-cost probes
2. keep first-dollar state intact
3. inventory runtime lanes and economy artifacts
4. recover Telegram target proof or keep manual relay explicit
5. only then resume publish/funding evidence flow

## Near-term work queue

### A. Runtime inventory pass

Goal:

- map all active runtime classes without starting new heavy services

Output:

- one runtime-class matrix covering shell, provider, federation, Telegram, treasury, Docker/WSL, and editor/operator surfaces

### B. Economy document consolidation

Goal:

- merge the first-dollar, deal, treasury, Telegram, and revenue recovery docs into a single economy operating brief

Output:

- `memory/AIOS_ECONOMY_OPERATING_BRIEF.md`

### C. First-dollar preservation

Goal:

- keep the active first-dollar pending events from being lost or overwritten

Must preserve:

- `publish-20260403004302`
- `funding-pending-uber-egift-20260403004325`
- `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`

### D. Root-host recovery alignment

Goal:

- restore Windows/Docker/WSL/admin authority without changing AIOS business state

Forbidden:

- Docker purge
- OS reinstall
- ledger mutation
- fabricated publish/funding confirmation

## Non-goals

- no autonomous spending
- no wallet execution
- no autoposting
- no new dependency-heavy runtime install
- no Docker reset
- no OS reset
- no broad archive promotion without proof

## Current conclusion

The AI economy already exists as a governed first-dollar pipeline. The correct next move is not to rebuild it, but to preserve the root host, consolidate the runtime map, and resume the first-dollar flow only after runtime proof is stable.
