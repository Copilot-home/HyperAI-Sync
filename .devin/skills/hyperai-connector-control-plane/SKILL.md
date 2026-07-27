# hyperai-connector-control-plane

## When to use

Use this skill whenever the task involves the APΩ unified connector control plane, multi-platform connector administration, capability negotiation, connector registry, adapter families, state machine, evidence receipts, credential reference broker integration, control API namespace, manual connector verification, or any request to discover/administrate multiple providers (OpenAI, Ollama, OpenRouter, Anthropic, Google, Azure, HubSpot, Notion, Asana, Vercel, etc.) through a single canonical contract.

Trigger phrases: "connector control plane", "unified adapter", "capability negotiation", "connector registry", "APΩ connector fabric", "state machine", "evidence receipt", "credential reference", "control API", "connector family", "manual adapter", "multi-platform provider admin", "bind a connector", "pluggable connector", "adapter family".

Do NOT use this skill for single-provider, single-API troubleshooting unless the user explicitly wants it placed inside the control-plane contract.

## What it does

This skill turns the user's request into a governed, packetized run through the APΩ connector control plane:

- Loads the canonical contract from `HyperAI-Sync/memory/APΩ_CONNECTOR_CONTROL_PLANE_CANON.md`.
- Classifies the connector or provider by family and plane.
- Discovers identity, capabilities, resources, and state.
- Produces a normalized capability registry and state-machine verdict.
- Runs policy preflight and dry-run before any side effect.
- Executes only after an approval gate is open.
- Commits an evidence receipt after execution.
- Reconciles against the canon and emits the next queue item.

## Canonical contract

Read first:

```text
HyperAI-Sync/memory/APΩ_CONNECTOR_CONTROL_PLANE_CANON.md
```

Key takeaways:

```text
10 planes:
  Identity / Credential / Billing / Audit / Runtime / Broker / Resource / Capability / Event / Approval / Recovery

6 families:
  A Model/Compute, B Workspace/Productivity, C Build/Deploy, D CRM/Commerce, E Catalog/Discovery, F Presentation

Adapter contract: ConnectorControlAdapter (base class in runtime/connector_control_plane/adapters/base.py)

State machine: DECLARED → ... → ORCHESTRATION_READY, with substates PASS_EMPTY, REQUIRES_REAUTHORIZATION, etc.

Credential rule: use credential_ref only; plaintext secrets never in request body, adapter config, or receipt.

Receipt schema: mission_id, connector_id, requested_action, effective_action, risk_class, credential_ref_hash, status, rollback, evidence_hash.
```

## Code scaffold

Implementation scaffold lives in:

```text
HyperAI-Sync/runtime/connector_control_plane/
├── schemas/
│   ├── connector_state.json
│   ├── capability.json
│   └── receipt.json
├── adapters/
│   ├── base.py
│   ├── __init__.py
│   └── openai.py
├── registry.py
├── state.py
├── capability.py
├── receipt.py
├── control_api.py
└── scripts/
    └── discover.py
```

Run discovery against OpenAI (reference implementation):

```bash
cd /Users/andy/HyperAI-Sync
OPENAI_ADMIN_KEY=env:<varname> python runtime/connector_control_plane/scripts/discover.py openai
```

## Pipeline

Always follow this sequence:

```text
DISCOVER → RESOLVE IDENTITY → DISCOVER CAPABILITIES → CLASSIFY → NORMALIZE
→ DIFF AGAINST CANON → POLICY PREFLIGHT → DRY RUN → APPROVAL → EXECUTE
→ VERIFY → COMMIT RECEIPT → RECONCILE → SUBSCRIBE/POLL EVENTS → ROTATE/CLEANUP
```

## Rules

1. Never put plaintext secrets in request body, adapter config, or receipt.
2. Always use `credential_ref`; resolve it through the APΩ credential broker or an approved resolver.
3. Use `ConnectorControlAdapter` contract; do not write provider-specific `if/else` ladders in core orchestrator.
4. Report state with risk class (R0–R5) and recovery/compensation status.
5. Manual dashboard-only surfaces produce `MANUAL_VERIFICATION_REQUIRED`, not `AUTOMATION_FAILED`.
6. Every side-effect action must produce an evidence receipt.
7. Prefer read-only / dry-run / preflight before any mutation.
8. OpenAI is the golden reference case; other providers are adapter-family variations.

## Output format

For each mission produce:

```text
MISSION_PACKET
SKILL_ROUTING_TABLE
MEMORY_CONTEXT
ACTION_PACKET
VERIFY_PACKET
ROLLBACK_PACKET
QUEUE_UPDATE
APPROVAL_GATE
```

## Starting the control plane API

```bash
cd /Users/andy/HyperAI-Sync
python runtime/connector_control_plane/control_api.py
```

It exposes `/control/*`, `/runtime/*`, `/events/*`, and `/evidence/*` routes.
