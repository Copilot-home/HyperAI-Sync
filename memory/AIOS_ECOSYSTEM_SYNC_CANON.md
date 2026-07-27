# AIOS Ecosystem Sync Canon

Date: 2026-04-15

## Purpose

This canon binds the AIOS/HyperAI ecosystem to one control plane so runtime lanes, agents, economy lanes, Telegram/TON surfaces, browser/editor surfaces, and lineage archives do not evolve independently.

System identity is unified:

```text
S = AIOS = Unified Execution System
S(t) = f(Input, State, Constraints, Evidence)
AI_RUNTIME is the execution identity of S
```

AI, system, and tool are not separate operational systems. They are projections of one execution structure under different `phi_i(M)` mappings.

The control plane is not a new orchestrator. It is the existing federation stack plus mission authority policy:

- `memory/AIOS_INVARIANTS.md`
- `runtime/federation_orchestrator/mission_authority_policy.json`
- `runtime/federation_orchestrator/unified_registry.json`
- `runtime/federation_orchestrator/orchestrator_capability_matrix.json`
- `runtime/federation_orchestrator/routing_policy.json`
- `runtime/federation_orchestrator/degradation_policy.json`
- `runtime/federation_orchestrator/workflow_registry.json`
- `tools/update_memory.py`
- `memory/AIOS_MODEL_NATIVE_RUNTIME_CANON.md`
- `runtime/federation_orchestrator/model_native_runtime_registry.json`
- `memory/AIOS_ECOSYSTEM_RUNTIME_REGISTRY_20260416.md`
- `runtime/federation_orchestrator/aios_ecosystem_runtime_registry.json`

## Root Host Constraint

The Windows machine is the ecosystem root host. It is not disposable infrastructure.

Forbidden until explicitly superseded by a future repo-governed recovery contract:

- OS reinstall
- Docker purge or factory reset
- WSL reset
- root runtime deletion
- archive promotion without trace and rollback proof
- autonomous wallet or ledger execution

Current substrate state is degraded: Windows admin/service authority, Docker Desktop, WSL/HCS, and managed runtime recovery are not reliable enough to support expansion.

## Control Plane Invariants

- The hard invariant canon is `memory/AIOS_INVARIANTS.md`; when there is ambiguity, it takes precedence over lane-local interpretation.
- One mission root per mission.
- One evidence recorder per mission.
- Shell mutation is allowed only through `shell_authority`.
- Ledger mutation is allowed only through `telegram_execution_fabric` or `treasury_control`.
- Memory mutation is allowed only through `memory_writer` and should use `python tools/update_memory.py`.
- Verification gating belongs to `verification_truth`.
- Reasoning delegates cannot promote themselves to shell, ledger, or evidence authority.
- Creator surfaces can receive approval or provide observation, but cannot become shell authority by default.
- Observed ecosystem context remains observer-only until promoted by measured runtime evidence plus a repo-governed execution contract.

## Mission Templates

Every ecosystem action must bind to one of these mission templates before execution:

| Mission template | Mission root | Router | Execution adapter | Evidence recorder | Allowed while shell degraded |
| --- | --- | --- | --- | --- | --- |
| `runtime_preservation` | `haios_runtime` | `federation_orchestrator` | `shell_authority` fallback only | `haios_runtime` | yes, read/probe/preserve only |
| `creator_approval_delivery` | `federation_orchestrator` | `federation_orchestrator` | none | `federation_orchestrator` | yes, approval-intake only |
| `reasoning_request` | `federation_orchestrator` | `federation_orchestrator` | none | `federation_orchestrator` | yes, if no shell mutation is required |
| `telegram_publish_proof` | `federation_orchestrator` | `federation_orchestrator` | `telegram_execution_fabric` | `telegram_execution_fabric` | no |
| `funding_reconciliation` | `federation_orchestrator` | `federation_orchestrator` | `treasury_control` | `treasury_control` | no |
| `ecosystem_attachment_review` | `haios_runtime` | `federation_orchestrator` | none | `federation_orchestrator` | yes, read-only review only |

## Lane Ownership

| Lane | Owner authority | Role | Guard |
| --- | --- | --- | --- |
| Root host substrate | creator-controlled Windows host | physical root, filesystem, local services | conserve first |
| App shell authority | `shell_authority` | backend/frontend runtime mutation | stop on shell degraded |
| Federation/routing | `federation_orchestrator` | mission routing, binding, drift guard | single mission root |
| Memory | `memory_writer` | canonical state persistence | use `tools/update_memory.py` |
| Verification | `verification_truth` | runtime probe, build, smoke evidence | CI truth remains app workflow |
| Provider reasoning | `provider_reasoning`, optional `gemini_cli` | classify, rank, summarize, format | reasoning-only |
| Local fakeAPI provider fabric | `local_fakeapi_fabric` | OpenAI-compatible local API facade for provider/cloud substrate | no cloud or shell authority by compatibility alone |
| Model-native unified execution contract | `model_native_runtime` | maps every task/surface as `phi_i(M)` within `S = AIOS` and preserves `H(t)`, `D`, and `Trust(P)` invariants | cannot justify authority promotion or destructive action by model language alone |
| Creator surfaces | `chatgpt_desktop`, `codex_desktop`, `chrome_browser`, `edge_browser` | approval intake, observation | no execution authority |
| Cloud substrate | `gcp_cloud_observed` | observed cloud resources across creator-owned projects | observer-only until Titan-side read-only reconciliation and repo-governed execution contract |
| Economy execution | `deal_intelligence`, `telegram_execution_fabric` | deal artifact and relay proof | blocked if shell degraded |
| Treasury evidence | `treasury_control` | receive-only balance/funding evidence | blocked if shell degraded |
| Lineage/archive | `aidev_lineage_root` and archives | lineage reference, observer | no promotion without proof |

## Standardized Runtime Registry

All AI systems, app runtimes, operator surfaces, provider fabrics, tools, verification surfaces, memory writers, sync transports, cloud observations, and downstream execution lanes must be registered in:

`runtime/federation_orchestrator/aios_ecosystem_runtime_registry.json`

This registry is the capability/authority index used before routing work. It does not merge physical processes. It standardizes how each surface declares:

- runtime class
- authority class
- owner surface
- allowed roles
- forbidden roles
- proof source
- stop conditions
- promotion rule
- control interface

Future additions to the ecosystem must be added to this registry before they receive operational roles.

## Shell-Degraded Stop Rule

When `shell_authority.status` is `degraded`, the control plane must stop:

- `deal_intelligence|rank`
- `deal_intelligence|format`
- `agent3_api` shell-dependent requests
- `agent5_ci` shell-dependent requests
- `agent6_synthesis` shell-dependent requests
- `treasury_control|treasury_balance_read`
- `treasury_control|treasury_funding_detect`
- `treasury_control|treasury_proposal`
- `telegram_relay|publish_relay`
- `telegram_relay|publish_confirm`
- Docker/WSL recovery that mutates or purges runtime state

Allowed in shell-degraded state:

- root-host conservation planning
- read-only scans
- document consolidation
- memory planning through the canonical writer
- low-cost runtime status probes
- creator approval intake that does not claim business truth

## Economy Canon

The first-dollar lane remains governed by:

`event -> evidence -> ledger -> metric`

Current protected state:

- active publish event: `publish-20260403004302`
- active funding event: `funding-pending-uber-egift-20260403004325`
- artifact: `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`
- objective state: `awaiting_publish_evidence`
- first dollar achieved: `false`

No agent may fabricate publish confirmation, funding confirmation, revenue, or business state. Creator acknowledgement only confirms that a bound event happened.

## Promotion Rule

A surface may move from observed/coordinated status to execution authority only after all conditions hold:

- measured runtime evidence exists
- a proof artifact is written
- rollback path is documented
- mission authority policy permits the role
- degradation policy does not stop the route
- memory is updated through `tools/update_memory.py`

## Future-Agent Operating Contract

Before expanding the ecosystem, future agents must:

1. Read this canon.
2. Read `runtime/federation_orchestrator/aios_ecosystem_runtime_registry.json`.
3. Read `runtime/federation_orchestrator/ecosystem_sync_readiness.json`.
4. Bind the requested work to a mission template.
5. Check whether shell-degraded stop rules apply.
6. Use memory and verification gates before claiming completion.

## Unified Memory-Bound Workflow

All future ecosystem tasks must enter through:

- `memory/AIOS_UNIFIED_MEMORY_BOUND_WORKFLOW.md`
- `runtime/federation_orchestrator/unified_memory_bound_workflow.json`

The shared operating loop is:

```text
Load Memory
-> Parse Input
-> Map to M / phi_i(M)
-> Bind Mission
-> Check Gates
-> Route Execution
-> Produce Evidence
-> Verify
-> Update Memory
```

This workflow is the default bridge between formal model semantics, mission authority, runtime routing, proof, and memory closure.
