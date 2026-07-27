# AIOS VS Code / Extension Policy Under Degraded Shell

Date: 2026-04-15

## Purpose

This policy defines what VS Code, VS Code extensions, editor agents, and IDE copilots may or may not do when:

```text
shell_authority = degraded
```

VS Code and extensions are not shell authority. They are creator/operator surfaces and may support reasoning, approval intake, editing, and evidence display only within invariant gates.

This policy must be read with `memory/AIOS_CREATOR_AI_COEXISTENCE_WORKFLOW.md`: VS Code/extension capabilities exist to reduce creator burden, not to pressure the creator or override post-turning system context.

## Default Classification

| Class | Meaning |
| --- | --- |
| `allowed` | Safe under degraded shell without additional approval, if no hidden mutation occurs |
| `approval_required` | May proceed only with explicit mission binding, evidence path, and rollback plan |
| `blocked` | Must not run while `shell_authority=degraded` |

## Allowed Commands

Allowed commands are read-only, planning-only, or memory-governed actions that do not mutate root host runtime state.

| Command class | Examples | Conditions |
| --- | --- | --- |
| Read repo files | open file, search text, inspect JSON/MD, view logs | no secret exfiltration; no source mutation unless explicitly planned |
| Static classification | map lanes, classify command risk, audit invariants | must reference canon artifacts |
| Planning | create implementation plan, rollback plan, sprint plan | no execution side effects |
| Memory/governance docs | update `.md` governance artifacts, queue docs, capsule docs | use memory writer for workspace state after substantial change |
| JSON governance artifact update | update policy/readiness/trace JSON under runtime governance | validate with `python -m json.tool` |
| Low-cost verification of docs | check file existence, grep policy terms, validate JSON | no app/runtime mutation |
| Approval intake | capture creator acknowledgement text | cannot convert acknowledgement into business truth without evidence recorder |
| Evidence display | show existing proof/log/artifact to creator | display only; no promotion without verification gate |

## Approval-Required Commands

These commands are not automatically forbidden, but cannot run from VS Code/extension unless all gates are satisfied:

- explicit mission template
- explicit mission authority
- evidence artifact path
- rollback plan
- invariant check
- verification plan

| Command class | Examples | Required mission |
| --- | --- | --- |
| Runtime probe beyond artifact inspection | port/process probe, local health probe, bounded script that checks runtime | `runtime_preservation` |
| App code edit | frontend/backend/source changes | mission must identify owning lane and CI requirement |
| Build/test/smoke | `npm run ci:build`, `npm run ci:browser-smoke`, targeted test | allowed only if repo verification rules require it |
| Extension command that writes workspace files | generate code, apply patch, update config | mission binding and evidence path required |
| GitHub/remote coordination | `gh` auth/status/issue/PR operations | identity and production lane must be checked first |
| Linear/external queue mutation | create/update external coordination issue | only implementation/proof/governance work that should leave memory queue |

## Blocked Commands

Blocked commands must not be run by VS Code, extensions, terminals spawned by VS Code, editor agents, or IDE copilots while `shell_authority=degraded`.

| Blocked command class | Examples |
| --- | --- |
| OS destructive recovery | OS reset, reinstall, repair install that mutates root host broadly |
| Docker destructive recovery | Docker Desktop factory reset, purge data, delete Docker WSL data |
| WSL destructive recovery | `wsl --unregister`, WSL reset, distro deletion, HCS destructive repair |
| Root runtime deletion | deleting runtime roots, source lineage roots, memory roots, vault/archive roots |
| Economy execution | Telegram publish confirmation, funding confirmation, wallet action, TON transaction, treasury mutation |
| Auto-deploy | deploy, publish, release, package push, marketplace publish |
| Authority promotion | promoting browser/editor/chat/extension output to canon without verification proof |
| Archive promotion | making archive/lineage roots executable authority without proof and rollback contract |
| Secret extraction | dumping tokens, wallets, private keys, credential stores into chat/logs/artifacts |
| Broad automated repair | command sequences that mutate many system areas without mission and rollback |

## Command Evaluation Order

Before executing any VS Code/extension command under degraded shell:

1. Check `memory/AIOS_INVARIANTS.md`.
2. Check `runtime/federation_orchestrator/aios_invariants.json`.
3. Check `runtime/federation_orchestrator/vscode_extension_degraded_shell_policy.json`.
4. Classify the command as `allowed`, `approval_required`, or `blocked`.
5. If `approval_required`, require mission binding, evidence path, rollback plan, and verification plan.
6. If `blocked`, stop and record the blocker.
7. If the command changes shell/root-host/economy status, re-audit `T`, `G(t)`, `Th`, `W`, `F`, `D`, and `Trust(S)`.

## Extension Behavior Requirements

Extensions should fail closed:

- If command class is unknown, treat it as `approval_required`.
- If command contains destructive OS/Docker/WSL/economy keywords, treat it as `blocked`.
- If command writes canon, require memory writer update.
- If command changes app code, require repo verification rule selection.
- If command touches economy state, require evidence recorder and current readiness to allow economy execution.

## Current State

Current policy assumes:

- `shell_authority = degraded`
- root host is conservation-critical
- economy execution is blocked
- VS Code/extension is not shell authority
