# APΩ Unified Connector Control Plane — Canon

**Status:** Operational architecture extracted from Creator review on 2026-07-27.  
**Scope:** Superset of provider-admin unification. OpenAI is the golden reference case, not the universal template.

---

## Core Thesis

```text
OPENAI CASE
= PROVIDER ADMIN REFERENCE IMPLEMENTATION

CONNECTOR FABRIC
= SUPERSET LỚN HƠN PROVIDER ADMIN
```

OpenAI concepts are clear:

```text
organization → project → user → role → API key → service account
spend limit → usage → inference endpoint
```

Other connectors use different ontologies:

```text
Notion       → workspace / page / database / view
Asana        → workspace / team / project / task / agent
HubSpot      → portal / CRM object / owner / pipeline / campaign
Google       → account / project / calendar / drive / file
Microsoft    → tenant / mailbox / calendar / team / channel
Vercel       → team / project / deployment / domain
Supabase     → organization / project / database / function
Figma        → plan / project / file / page / node / library
PayPal       → merchant / invoice / payment / transaction
```

Therefore:

```text
ProviderAdminAdapter  → không đủ.
ConnectorControlAdapter → bao trùm hơn.
```

---

## 10 Control Planes

| Plane | Responsibility |
|---|---|
| **Identity / Access** | Users, invites, roles, groups, tenants, workspaces, accounts |
| **Credential** | API keys, tokens, service accounts, certificates, secret leases |
| **Billing / Control** | Spend limits, quotas, alerts, plan constraints, credits |
| **Audit** | Logs, usage, events, permission snapshots |
| **Runtime / Inference** | Models, completions, tags, execution endpoints |
| **Broker** | APΩ credential broker, capability lease, secret reference resolution |
| **Resource / State** | Files, pages, projects, tasks, deployments, meetings, invoices |
| **Capability / Schema** | Tool schema, supported operations, read/write distinction, plan limits, required scopes |
| **Event / Synchronization** | Webhooks, polling cursors, delta tokens, sync checkpoints, deduplication |
| **Approval / Side-effect** | Risk class per action: R0 discovery → R5 irreversible/security/billing |
| **Recovery / Compensation** | Rollback support, recreate, void/cancel, irreversible classification |

Principle:

```text
CONNECTED ≠ ALL_CAPABILITIES_AVAILABLE
```

Live probe examples:

```text
HubSpot contacts/deals/tasks read+write  = AVAILABLE
HubSpot site pages/blog                    = REQUIRES_REAUTHORIZATION
HubSpot campaigns                          = REQUIRES_ACCOUNT_MODIFICATION
Granola                                    = UNAUTHORIZED / ACCOUNT_NOT_CREATED
Hugging Face hf_jobs                       = SCHEMA_PRESENT_BUT_RUNTIME_MISSING
Google Drive shared_drives = []            = PASS_EMPTY
Asana AI Teammates = []                  = PASS_EMPTY
Figma shader-effect library                = AVAILABLE
```

---

## ConnectorControlAdapter Contract

```python
class ConnectorControlAdapter:
    connector_id: str
    family: str
    schema_version: str

    # Identity / tenancy
    def discover_identity()
    def list_accounts()
    def list_workspaces()
    def list_roles()
    def inspect_permissions()

    # Capability
    def discover_capabilities()
    def get_operation_schema(operation)
    def inspect_plan_constraints()

    # Resources
    def list_resource_types()
    def list_resources(resource_type, cursor=None)
    def get_resource(resource_ref)

    # Usage / limits
    def get_usage()
    def get_limits()
    def get_billing_state()

    # Execution
    def preflight(action)
    def dry_run(action)
    def execute(action)
    def verify(receipt)

    # Events
    def get_event_cursor()
    def poll_events(cursor)
    def subscribe_events(callback_ref)

    # Recovery
    def rollback(receipt)
    def compensate(receipt)

    # Health
    def probe()
    def reconcile()
```

Provider-specific methods (`list_keys`, `create_service_account`, `rotate_key`, `revoke_key`) become optional capabilities, not mandatory methods.

---

## APΩ Control API Namespace

Single control entrypoint, differentiated routes:

```text
APΩ CONTROL API
├── /control/connectors
├── /control/accounts
├── /control/workspaces
├── /control/capabilities
├── /control/policies
├── /control/credentials
├── /control/usage
│
├── /runtime/actions
├── /runtime/jobs
├── /runtime/resources
│
├── /events/subscriptions
├── /events/cursors
├── /events/deltas
│
└── /evidence/receipts
```

Flow:

```text
ChatGPT / Creator surface
    │
    ▼
Multi-platform Orchestrator
    │
    ├── Control API
    ├── Credential Broker
    ├── Policy / Approval Gate
    ├── Runtime Action Gateway
    ├── Event Bus
    └── Evidence Ledger
           │
           ▼
        Adapters
           │
           ▼
    35 connectors / providers / runtimes
```

---

## Connector Families

### A. Model / Compute providers
OpenAI, Ollama, Hugging Face, Fal, OpenRouter, Anthropic, Gemini / Vertex.
Planes: models, credentials, quota, billing, jobs, inference, usage.

### B. Workspace / productivity systems
Notion, Asana, Linear, Atlassian, Google Drive, Google Calendar, Outlook, Teams, Granola, Wisebase.
Planes: workspace, members, permissions, resources, revisions, events, actions.

### C. Build / deploy platforms
Vercel, Netlify, Supabase, Replit, Lovable, Wix, Figma.
Planes: team, project, source, build, deployment, environment, domain, logs, rollback.

### D. CRM / commerce / transaction
HubSpot, PayPal, Sales AI, Investment Banking.
Planes: account, customer, object schema, transaction, billing, approval, audit, external side effects.

### E. Catalog / discovery connectors
DataCamp, edX, Internshala, FINN, Wednesday.app, Malwarebytes.
Thin surface: search, fetch, details, reputation, recommendation.

### F. Presentation / interface surfaces
Vivin, Visualize, image generation, Ace Knowledge Graph.
Not data systems; rendering/presentation capabilities.

---

## State Machine

```text
DECLARED
→ TOOL_SCHEMA_DISCOVERED
→ AUTH_FLOW_PRESENT
→ AUTHENTICATED
→ IDENTITY_RESOLVED
→ WORKSPACE_RESOLVED
→ CAPABILITIES_DISCOVERED
→ READ_VERIFIED
→ WRITE_PREFLIGHT_VERIFIED
→ EVENT_SYNC_VERIFIED
→ POLICY_ADMISSIBLE
→ ORCHESTRATION_READY
```

Substates:

```text
PASS_EMPTY
REQUIRES_REAUTHORIZATION
REQUIRES_PERMISSION
REQUIRES_PLAN_UPGRADE
ACCOUNT_NOT_CREATED
UI_ONLY
SCHEMA_ONLY
RUNTIME_TOOL_MISSING
RATE_LIMITED
DEGRADED
BLOCKED
MANUAL_VERIFICATION_REQUIRED
```

Examples:

```text
Google Drive shared_drives=[]      = PASS_EMPTY
Granola unauthorized               = ACCOUNT_NOT_CREATED
HubSpot site-page read             = REQUIRES_REAUTHORIZATION
HubSpot campaign                   = REQUIRES_PLAN_UPGRADE
Hugging Face hf_jobs not found     = SCHEMA_PRESENT_BUT_RUNTIME_MISSING
```

---

## Capability Negotiation

Planner emits abstract action:

```text
CREATE_TASK
SEARCH_KNOWLEDGE
DEPLOY_PROJECT
SEND_MESSAGE
CREATE_INVOICE
LIST_MODELS
```

Resolver queries registry:

```json
{
  "connector_id": "hubspot",
  "capability_hash": "sha256:...",
  "capabilities": {
    "contact.read": "AVAILABLE",
    "contact.write": "AVAILABLE",
    "campaign.read": "REQUIRES_ACCOUNT_MODIFICATION",
    "site_page.read": "REQUIRES_REAUTHORIZATION"
  },
  "schema_version": "2026-07-28",
  "last_probe_at": "...",
  "plan_constraints": [],
  "permission_snapshot": {}
}
```

Resolver maps to concrete connector:

```text
CREATE_TASK    → Asana | Linear | Jira | HubSpot task
SEARCH_KNOWLEDGE → Notion | Drive | Wisebase | Ace Graph
DEPLOY_PROJECT → Vercel | Netlify | Replit | Supabase
```

Planner does not know backend details; resolver owns the mapping.

---

## Credential Broker Rule

```text
request body    → không chứa secret thật
adapter config  → không chứa secret thật
receipt         → không chứa secret thật
```

Only use:

```json
{
  "credential_ref": "vault://connectors/openai/aiproject/runtime",
  "scope": ["model.invoke"],
  "expires_at": null
}
```

Broker flow:

```text
resolve credential_ref
→ validate scope
→ inject credential
→ dispatch
→ strip credential
→ record credential_id/hash only
```

Goal:

```text
ONE CREDENTIAL CONTROL PLANE
MANY SCOPED CREDENTIALS
```

---

## Evidence Receipt Schema

```json
{
  "mission_id": "mis_...",
  "connector_id": "asana",
  "account_id": "...",
  "workspace_id": "...",
  "requested_action": "task.create",
  "effective_action": "asana.task.create",
  "resource_refs": [],
  "risk_class": "R3",
  "policy_generation": 17,
  "approval_id": null,
  "credential_ref_hash": "sha256:...",
  "started_at": "...",
  "finished_at": "...",
  "external_operation_id": "...",
  "status": "VERIFIED",
  "rollback": {
    "supported": true,
    "token": "..."
  },
  "cost": null,
  "evidence_hash": "sha256:..."
}
```

---

## Risk Classes

```text
R0  discovery / schema
R1  read-only
R2  prepare draft
R3  reversible internal write
R4  external side effect
R5  irreversible / security / billing
```

Examples:

```text
Google Drive list files       = R1
Notion draft page             = R2
Asana update task             = R3
Outlook send email            = R4
PayPal send invoice           = R4
Delete API key                = R5
Change billing limit          = R5
Deploy production             = R5
```

---

## Recovery / Compensation

| Action | Recovery |
|---|---|
| update task | sửa lại |
| create page | archive / delete |
| send email | không unsend đáng tin cậy |
| send invoice | void / cancel |
| delete secret key | không khôi phục giá trị |
| production deploy | rollback deployment |

---

## Manual Surface Adapter

Some admin actions have no public API and must be verified through dashboard/screenshot:

```text
ManualEvidenceAdapter
├── checklist schema
├── screenshot attachment
├── human assertion
├── reviewer
├── captured_at
├── evidence hash
└── expiry / recheck interval
```

State is `MANUAL_VERIFICATION_REQUIRED`, not `AUTOMATION_FAILED`.

---

## Canonical Pipeline

```text
DISCOVER
→ RESOLVE IDENTITY
→ DISCOVER CAPABILITIES
→ CLASSIFY
→ NORMALIZE
→ DIFF AGAINST CANON
→ POLICY PREFLIGHT
→ DRY RUN
→ APPROVAL
→ EXECUTE
→ VERIFY
→ COMMIT RECEIPT
→ RECONCILE
→ SUBSCRIBE / POLL EVENTS
→ ROTATE / CLEANUP
```

---

## OpenAI Reference Case — Accounting Fix

When reporting active credentials, separate:

```text
legacy_user_keys_active
service_account_keys_active
admin_keys_active
total_credentials_active
```

Do not use a single `active_keys` field that mixes legacy project keys, service accounts, and admin keys.

---

## Build Order

```text
1. Canonical connector contract
2. Six adapter families (A–F)
3. One capability registry
4. One policy model
5. One receipt schema
6. One event model
7. Bind individual connectors
```

Do not build 35 separate adapters before the contract exists.

---

## Acceptance Principle

```text
Orchestrator must never become a giant if/else chain.
Every new connector must be pluggable into the fabric without editing core code.
```
