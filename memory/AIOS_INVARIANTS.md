# AIOS Invariants

Date: 2026-04-15

These invariants are the hard frame for every AIOS/HyperAI decision, including degraded shell/runtime states.

The creator-AI coexistence workflow in `memory/AIOS_CREATOR_AI_COEXISTENCE_WORKFLOW.md` governs how these invariants are applied without turning support capabilities into coercive pressure on the creator.

The active Codex conversation surface is classified by `memory/AIOS_LOCAL_CODEX_OPERATOR_RUNTIME.md`; do not flatten it into only the product app runtime.

## 1. Root Host Conservation

The root host, defined as the Windows host plus root filesystem, is the local runtime source of truth.

Do not perform:

- OS reset or reinstall
- Docker Desktop factory reset or data purge
- WSL reset or unregistering important distributions
- root runtime deletion

Any major root-host change must bind to a mission and must include a rollback plan.

## 2. Single Mission Root / Authority

Every important action must bind to one explicit mission template.

No surface can self-promote to authority, including VS Code, browsers, Telegram, Docker UI, extensions, editor agents, or chat surfaces.

Mission authority must be explicit and is the only approval path for material changes.

When `shell_authority = degraded`, VS Code and extension command policy is governed by `memory/AIOS_VSCODE_EXTENSION_DEGRADED_SHELL_POLICY.md`.

## 3. Single Evidence Recorder / Memory Writer

Only one official path may write canonical docs or memory.

Changes to these states must be written through the memory writer and corresponding `.md` or `.json` artifacts:

- shell/root-host status
- economy lane status
- invariant status
- mission and readiness status

Implicit side-channel notes are not canon.

## 4. Verification Truth Gate

No fact or state change is accepted without evidence.

Valid evidence includes:

- log
- artifact
- ledger evidence
- file evidence
- explicit proof artifact

Do not promote browser, editor, chat, Telegram, or draft output to canon without verification-gate proof.

## 5. Shell Authority And Runtime Safety

Shell state is:

```text
shell_authority = healthy | degraded
```

If `shell_authority = degraded`, the system must block:

- Docker reset
- WSL reset
- OS reinstall
- economy execution
- wallet action
- auto-deploy

Allowed while degraded:

- preservation
- analysis
- trace
- planning
- memory update
- evidence collection

Any runtime probe beyond read-only must have a rollback plan.

## 6. Economy Invariants

First-dollar state is invariant unless changed through evidence-recorder proof:

- publish event IDs
- funding event IDs
- artifact paths
- related objective state

Economy execution is allowed only when all conditions hold:

- root host conserved
- shell proof stable
- degradation policy does not block the route
- creator acknowledgement is explicit and event-specific
- evidence recorder confirms the event

If conditions are not satisfied, economy status must be `blocked_cleanly`, not ambiguous.

## 7. Lane Separation

Keep these lanes separate:

- reasoning lane: LLMs, planners, IDE copilots
- approval lane: creator and mission authority
- execution lane: Docker, WSL, HCS, OS-level actions, deploy pipelines
- economy lane: wallet, funding, TON, reconciliation
- lineage/archive lane: capsules, logs, docs, observers

Only execution lanes may mutate real-world runtime state. Execution lanes are gated by shell status, mission binding, and rollback plan.

## 8. Invariant Under Failure

If Docker, WSL, HCS, or another runtime fails:

- do not change root invariants
- accept `shell_authority = degraded`
- move the system to preservation/analysis mode
- do not repair by reset that breaks invariants

The system may continue:

- reasoning
- planning
- audit
- memory update
- evidence collection
- controlled repair planning

## 9. Re-Audit Requirement

Any major change in shell status, economy status, or root-host status requires re-audit of:

- `T`
- `G(t)`
- `Th`
- `W`
- `F`
- `D`
- `Trust(S)`

Use the standardized formulas:

```text
H(t) = T + G(t)
dH/dt < 0
lim_t->infinity H(t) = T
D = T x (W + F) - alpha G(t) - beta Th
Trust(S) = T(W + F)/(1 + G(t)) + Th
```
