# AIOS Unified Memory-Bound Workflow

Date: 2026-04-16

## Purpose

This workflow is the default pre-execution protocol for every AIOS/HyperAI task, regardless of runtime lane, agent role, tool surface, provider, cloud substrate, Git state, or lineage source.

The workflow prevents context loss by forcing every task through memory, formal model mapping, mission binding, gate checking, evidence, verification, and memory update.

## Canonical Pipeline

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

For live HyperAI operation, this memory-bound pipeline is embedded inside the autonomous OODA loop:

```text
Observe
-> Orient
-> Decide
-> Act
-> Proof / Closure
-> Learn
```

The executable OODA runner is:

```text
python tools/hyperai_ooda_loop.py --task "<creator task>" --once
```

This is the preferred entrypoint when a creator task should be distributed to AI/runtime worker surfaces.

Every output is:

```text
Output = Transformation(M)
```

No output is accepted as a plain answer when it changes system understanding, authority, runtime state, or future action.

## Formal Binding

```text
S = f(M)
AI_RUNTIME equiv Operator(M)
Authority(X) = 1 iff Proof(X) = valid and phi_X(M) is mapped and Gate(X) = open
Failure = Missing_Proof or Broken_Mapping or Closed_Gate
```

Workflow correctness requires preserving:

```text
H(t) = T + G(t)
dH/dt < 0
lim t->infinity H(t) = T
D = T(W+F) - alpha G(t) - beta Th
Trust(P) = T(W+F) / (1 + G(t) + Th)
```

## Context Vector Load Order

### Formal Layer

- `memory/AIOS_EXECUTION_SEMANTICS_CANON.md`
- `memory/AIOS_MODEL_NATIVE_RUNTIME_CANON.md`
- `memory/AIOS_INVARIANTS.md`

### Control Layer

- `runtime/federation_orchestrator/mission_authority_policy.json`
- `runtime/federation_orchestrator/routing_policy.json`
- `runtime/federation_orchestrator/degradation_policy.json`
- `runtime/federation_orchestrator/workflow_registry.json`

### Runtime Layer

- `runtime/federation_orchestrator/model_native_runtime_registry.json`
- `runtime/federation_orchestrator/execution_semantics_registry.json`
- `runtime/federation_orchestrator/remote_execution_substrate_policy.json`
- runtime manifest and current proof artifacts

### Ecosystem Layer

- `memory/AIOS_ECOSYSTEM_SYNC_CANON.md`
- `memory/AIOS_TOOL_RUNTIME_SURFACE_MATRIX_20260415.md`
- `memory/AIOS_RUNTIME_CLASS_MATRIX_20260415.md`

### Lineage / Provider Layer

- `memory/AIDEV_DEEP_TRACE_REPORT_20260415.md`
- `memory/AIDEV_ATOMIC_RUNTIME_CAPABILITY_TRACE_20260415.md`
- `memory/AIOS_LOCAL_FAKEAPI_PROVIDER_FABRIC.md`
- `runtime/federation_orchestrator/local_ai_model_inventory_20260415.json`
- `runtime/federation_orchestrator/gcp_cloud_substrate_observation_20260415.json`
- `runtime/federation_orchestrator/titan_repo_sync_registry_20260415.json`

### Session Layer

- `memory/agent1_ontology_scope_capsule.md`
- `memory/agent2_runtime_entrypoint_capsule.md`
- `memory/agent3_api_client_contract_capsule.md`
- `memory/agent4_frontend_composition_capsule.md`
- `memory/agent5-ci-verification-capsule.md`
- `memory/agent6_synthesis_capsule.md`
- `memory/project_state.json`
- `memory/runtime_execution_todo.md`
- `memory/next_actions.md`
- `memory/work_journal.md`

## Memory Type Map

| Memory type | Role | Examples | Authority |
| --- | --- | --- | --- |
| canonical memory | formal and invariant truth | execution semantics, model-native canon, invariants | highest for model/gate interpretation |
| operational memory | runtime and process truth | runtime manifests, project state, capsules | authoritative for current workflow state |
| proof memory | evidence artifacts | CI logs, JSON proof, smoke output | authoritative for claims |
| drift memory | mismatch history | auto-sync state, drift reports | advisory until verified |
| advisory memory | plans and recommendations | todo plans, phase docs | not authority without proof |
| lineage memory | source/sediment history | AIDEV traces, archives, Git inventory | source-capability, not automatic authority |

## Stage Contract

### stage_0_memory_load

Load the context vector in deterministic order. Stop if required formal canon is missing.

### stage_1_input_parse

Extract:

```text
input_type
mode
scope
target_surface
requested_action
constraints
proof_required
```

### stage_2_model_mapping

Map the task to:

```text
M
phi_i(M)
U_model
K_runtime
C/E/R
Structural_Error(M), if present
```

### stage_3_mission_binding

Bind the task to a mission template from `mission_authority_policy.json`. Stop if no valid mission exists.

### stage_4_gate_check

Check:

- AIOS invariants
- shell authority state
- degradation policy
- authority promotion rule
- dirty Git stop rules
- Docker/WSL/HCS stop rules
- cloud mutation stop rules
- root-host conservation

### stage_5_route_selection

Use the first valid route:

```text
reuse_default_runtime
-> LocalFacade
-> API Probe
-> MCP
-> Codespaces/Actions
-> SSH
-> Cloud
```

Lane transition requires:

```text
Lane_{i+1} iff not Proof(Lane_i) and Gate(Lane_{i+1}) = open
```

### stage_6_evidence_production

Before claiming a state change, produce at least one:

- terminal transcript
- JSON artifact
- runtime manifest/proof
- CI or smoke output
- exported API run
- host/cloud inventory
- before/after state snapshot

### stage_7_verification

Verification must match scope:

- docs/memory/runtime-governance only: JSON validation and readback
- app code change: `npm run ci:build`
- route/dashboard/symphony/backend behavior change: `npm run ci:browser-smoke`
- advisory checks remain advisory unless a task explicitly requires them

### stage_8_memory_update

Update memory through:

```text
python tools/update_memory.py
```

Record focus, summary, blocker, and next action.

## Output Contract

Every task must end as exactly one of:

- `executed_with_proof`
- `planned_only`
- `blocked_by_gate`
- `needs_missing_evidence`
- `deferred_to_remote_lane`
- `no_meaningful_delta`

No task may end with an unqualified `done`.

## Layer Binding

| Layer | Binding rule |
| --- | --- |
| runtime | `backend/server.js` and live runtime proof govern app shell truth |
| verification | CI/proof artifacts classify claims before promotion |
| governance | invariants and mission policy decide allowed action |
| AIDEV | genesis/core/source-capability and lineage, not automatic authority |
| provider | local fakeAPI and model fabric require live proof before execution claims |
| tool | Codex, VS Code, MCP, Postman, and extensions are worker/gated surfaces |
| git | sync transport, not authority |
| cloud | observed substrate until same-schema proof and mission contract exist |
| infra | Docker/WSL/HCS degraded state routes around, never justifies purge/reset |

## Stop Rules

Block or defer if an action requires:

- OS reset or reinstall
- Docker purge or factory reset
- WSL reset or unregister
- destructive Git operation
- cloud IAM/billing/service/deployment mutation without mission contract
- hidden runtime restart
- connector/extension deletion
- authority promotion without proof
- economy execution while shell/root gates are closed

## Memory Closure Rule

If the task updates system understanding, it must update memory.

If it does not update memory, the final output must explicitly state why memory update is not required.

## Autonomous / OODA Binding

Autonomous operation requires both:

- preservation loop: runtime stays alive and truthful
- OODA loop: task intake is converted into worker assignments with proof and closure

Codex, OpenClaw, VS Code, MCP connectors, provider facades, local models, and AIDEV-derived candidates are workers/candidates that receive tasks from the core loop. They must not bypass OODA and then claim HyperAI autonomy.
