# AIOS Local FakeAPI Provider Fabric

Date: 2026-04-15

## Purpose

This canon binds provider, cloud, and reasoning substrates to a local-first API facade.

In this system, `fakeAPI` means an OpenAI-compatible / Chat-Completions-shaped local fabric adapter. It does not mean deception, model ownership fabrication, or bypassing provider identity. It is a compatibility layer so AIOS can speak one local API contract while preserving provider evidence underneath.

## Canonical Local API Shape

The current proven source substrate is:

```text
source_root = C:\Users\pc\aidev\quantumreason_v3
facade = QuantumReason v3.1
primary_endpoint = /api/v2/chat/completions
health_endpoint = /api/v2/health
stats_endpoint = /api/v2/stats
contract_shape = OpenAI-compatible chat completion response
```

Observed implementation facts:

- `api_server.py` exposes `/api/v2/chat/completions`.
- `api_server.py` returns `object = chat.completion`.
- `api_server.py` records provider, cache mode, request id, and resolved model when available.
- `llm_orchestrator.py` supports `openai`, `anthropic`, `google`, and `local`.
- Local provider is preferred for code/debug/general tasks.
- Google/Gemini provider is a downstream provider lane, not shell authority.

## Cloud Substrate Binding

GCP projects observed in `memory/AIOS_GCP_CLOUD_SUBSTRATE_OBSERVATION_20260415.md` should be connected through the local facade as observed provider/cloud substrate.

Default route:

```text
creator / agent request
-> local fakeAPI facade
-> provider router
-> local model first
-> optional cloud provider only when explicitly enabled and proof-gated
-> response with provider/cache/evidence metadata
```

This keeps the local AI API as the system's coordination interface while allowing cloud resources to remain part of the ecosystem.

## Routing Rules

- All reasoning requests should target the local fakeAPI facade first.
- Cloud projects are not direct execution authority.
- GCP services may be classified as provider substrate, data substrate, or infrastructure substrate.
- Gemini/Vertex services may become provider candidates only after read-only reconciliation and credential/proof gates.
- Container/GKE/Artifact services remain infrastructure substrate, not runtime target, until a separate deployment contract exists.
- IAM, billing, service enablement, and deployment are blocked from this binding.

## Required Metadata

Every local facade response or route decision should preserve:

- request id
- provider name
- resolved model when available
- cache mode
- result class
- failure class if degraded
- proof or health source

## Authority Separation

```text
local_fakeapi_fabric = reasoning/API compatibility surface
gcp_cloud_observed = observed cloud substrate
hyperai-user-control-system = product runtime surface
backend/server.js = current backend runtime truth
runtime manifests = operational truth
proof artifacts = verification truth
```

No cloud substrate may become shell authority through API compatibility alone.

## Stop Rules

Do not use this binding to:

- deploy to GCP
- mutate IAM
- enable or disable GCP services
- change billing
- create service accounts
- start Docker/WSL recovery
- override local runtime authority
- claim model ownership from application or project names

## Next Safe Reconciliation

The next safe step is a read-only contract registry that maps:

```text
cloud_project -> substrate_class -> allowed_fakeapi_role -> blocked_roles -> proof_gap
```

No live cloud call is required for that mapping when using creator-provided copied evidence.

## Delta 2026-04-16 Local-First Quota Mitigation

The fakeOpenAPI facade is now the default quota-protection route for operator app runtimes.

Proof captured:

- `127.0.0.1:8000` is listening under the local Python runtime.
- `/api/v2/health` returns `status = healthy`.
- `/api/v2/chat/completions` returns `provider = local` and resolves `qwen2.5-coder:1.5b`.
- The auth shim accepts both `X-API-Key` and OpenAI-compatible `Authorization: Bearer`.

VS Code Insiders was adjusted to preserve extensions and MCP nodes while disabling automatic Copilot/Gemini/GitLens quota lanes. The governing policy is `memory/AIOS_LOCAL_FIRST_QUOTA_POLICY.md` and the machine registry is `runtime/federation_orchestrator/local_first_quota_policy.json`.
