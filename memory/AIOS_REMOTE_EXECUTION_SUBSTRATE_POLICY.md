# AIOS Remote Execution Substrate Policy

Date: 2026-04-15

## Purpose

This policy binds the execution-routing rule for degraded local infrastructure substrates.

Docker, WSL, and HCS failures do not stop `S = AIOS = Unified Execution System`. They reduce trust in the local container substrate and force execution to route through safer proven surfaces.

The correct response is not local destructive repair. The correct response is substrate substitution:

```text
degraded local substrate
-> classify
-> choose remote/API/tool substrate
-> prove access
-> execute bounded task
-> record evidence
-> update memory
```

## Model-Native Mapping

Each alternate platform is a valid `phi_i(M)` projection only after role and proof classification:

```text
surface -> phi_i(M) -> role_class -> proof_source -> allowed_action
```

Runtime priority remains:

```text
Structure > Problem > Constraint > Evidence > Action
```

Personal phrasing is ignored unless it changes safety, authority, or scope.

## Degraded Local Substrate Rule

When Docker Desktop, WSL, or HCS is degraded:

- Do not reset Docker Desktop.
- Do not purge Docker data.
- Do not unregister WSL distributions.
- Do not reinstall or reset Windows.
- Do not block the whole system just because one local substrate is unavailable.
- Route eligible execution through cloud, SSH, Codespaces, MCP, Postman/API clients, GitHub Actions, or provider facades when a proof contract exists.

## Remote Execution Lanes

| Lane | Role | Allowed use | Blocked use | Proof required |
| --- | --- | --- | --- | --- |
| Cloud substrate | remote infrastructure / provider substrate | read-only inventory, explicit proof jobs, bounded deployment candidate | IAM/billing mutation, service enable/disable, deploy by assumption | live inventory artifact or copied evidence marked observer-only |
| SSH remote host | remote execution host | health probe, bounded command, artifact pullback | destructive repair, credential extraction, root mutation without rollback | host identity, command log, rollback path |
| GitHub Codespaces | disposable cloud dev substrate | build/test/proof in isolated clone | authority replacement for root host, secret exfiltration | repo/branch/commit, command transcript, artifact path |
| GitHub Actions | CI proof substrate | workflow proof, build/test artifact | runtime authority without deployment contract | workflow run URL/log/artifact |
| Postman/API client | API probe surface | endpoint verification, collection replay, contract evidence | business truth or authority by label | exported collection/run result |
| MCP connectors | tool bridge / capability node | docs, Figma, browser, filesystem-safe proof, connector-specific read/write under contract | connector deletion, hidden authority promotion | connector log or generated artifact |
| Local fakeAPI facade | provider normalization surface | route provider/model requests through local-compatible API | provider identity bypass or cloud authority | source trace plus live health/inference proof |

## Routing Decision

Use this route order when local Docker/WSL is degraded:

1. Reuse current healthy app runtime if ports and proof are healthy.
2. Use local API/provider facade for model/provider work when live proof exists.
3. Use Postman/API clients for contract verification.
4. Use MCP connectors for task-specific capabilities.
5. Use GitHub Actions or Codespaces for build/test/proof that cannot run locally.
6. Use SSH remote hosts for bounded execution only after host identity and rollback are explicit.
7. Use cloud provider substrate only after read-only inventory and mission binding.

## Promotion Rule

No remote lane becomes authority by existence.

Promotion requires:

- mission template
- target surface
- proof artifact
- rollback path
- memory update
- no conflict with root-host conservation

## Evidence Contract

Every remote execution must produce at least one of:

- terminal transcript
- exported API run
- CI/workflow artifact
- remote host identity proof
- before/after state snapshot
- generated JSON proof artifact under `runtime/`

Copied logs are valid evidence, but they remain observed-only until same-schema live inventory exists.

## Current State Binding

- Titan app runtime is healthy on `5000/4173` and should be reused.
- Docker Desktop is degraded and must not be used as expansion base.
- WSL/HCS is degraded and must not be reset in this phase.
- GCP is observed substrate from MacBook evidence until Titan/MacBook same-schema inventory exists.
- AIDEV is backend/source substrate and may be used as source proof, not auto-executed without gates.
- Git is sync transport, not authority.

## Stop Conditions

Stop and record blocker if a proposed route requires:

- credential disclosure
- destructive Git operation
- Docker/WSL reset or purge
- OS reinstall or reset
- cloud IAM/billing/service mutation
- hidden runtime restart
- untracked authority promotion

## Next Safe Action

Build a `Remote Execution Capability Matrix` that lists each cloud/SSH/Codespaces/MCP/Postman lane with:

```text
surface_id
role_class
access_status
allowed_actions
blocked_actions
proof_command_or_artifact
promotion_condition
rollback_requirement
```

