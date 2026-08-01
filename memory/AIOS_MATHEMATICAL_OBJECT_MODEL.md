# AIOS Mathematical Object Model

Date: 2026-07-30
Status: materialized from creator draft (NHÁP)

## 0. Domain

```text
𝕆 = ℂ ⊔ ℍ ⊔ ℕ ⊔ 𝕄 ⊔ 𝕋 ⊔ ℙ ⊔ 𝔸 ⊔ 𝔼
```

- `ℂ` — Creator
- `ℍ` — Host / hardware / OS
- `ℕ` — Runtime / node / surface
- `𝕄` — Memory / state / ledger
- `𝕋` — Tool
- `ℙ` — Provider / model
- `𝔸` — Authority / capability
- `𝔼` — Evidence / artifact

Primary elements:

- `c_Ω ∈ ℂ` — Creator
- `h_0 = MacLocalHost ∈ ℍ` — root host
- `r_0 = aios_mission_router ∈ ℕ` — Local Root

## 1. Node structure

Every node:

```text
n_i = ⟨ id_i, τ_i, loc_i, ep_i, cap_i, auth_i, state_i, health_i, lease_i, lineage_i, cost_i, value_i ⟩
```

Fields:

- `id` — unique identifier
- `τ` — type (see §2)
- `loc` — physical / logical location
- `ep` — endpoint
- `cap` — capabilities
- `auth` — authority set
- `state` — current state
- `health` — health status
- `lease` — existence contract
- `lineage` — source and history
- `cost` — cost
- `value` — value

No node is "just a name":

```text
id_i ≠ n_i
```

## 2. Node type taxonomy

```text
𝒯_N = { ROOT, ORCHESTRATOR, MEMORY, VERIFIER, WORKER, GATEWAY, BROKER, PROVIDER, TOOL, PRODUCT, DATABASE, INFRA }
```

Current mapping:

- `r_0 = aios_mission_router` → `ROOT`
- `federation_orchestrator` → `ORCHESTRATOR`
- `memory_writer` → `MEMORY`
- `verification_truth` → `VERIFIER`
- `codex_operator_runtime` → `WORKER`
- `APΩ gateway` → `GATEWAY`
- `credential broker` → `BROKER`

## 3. Topology

```text
𝒢 = ( ℕ, 𝔼_G, τ, λ )
```

Edge types:

```text
λ(e) ∈ { CONTROL, ROUTE, INVOKE, READ, WRITE, VERIFY, AUTH, EVIDENCE, DEPEND, HEARTBEAT, PROMOTE }
```

Core topology:

```text
c_Ω --CONTROL--> r_0
r_0 --CONTROL--> { federation, memory, verifier, worker, gateway, broker, providers, tools }
gateway --ROUTE--> { providers, tools }
worker --WRITE--> memory
verifier --EVIDENCE--> root
```

Creator is no longer a dispatcher for every leaf node.

## 4. Local Root

```text
r_0 = ⟨ 𝒢_L, ℛ, 𝒬, 𝒜, 𝒱, ℒ ⟩
```

Components:

- `𝒢_L` — whole-local topology
- `ℛ` — runtime registry
- `𝒬` — mission queue
- `𝒜` — authority map
- `𝒱` — verification state
- `ℒ` — ledger / lineage

Materialization conditions:

```text
Materialized(r_0) = 1  ⟺
  DaemonAlive(r_0) = 1
  ∧ RegistryLoaded(r_0) = 1
  ∧ PrimaryEntrypoint(r_0) = 1
  ∧ Verify(r_0) = PASS
  ∧ RollbackReady(r_0) = 1
```

Gate 1 satisfied these conditions.

## 5. Mission object

```text
μ_k = ⟨ id, goal, scope, constraints, budget, deadline, evidenceReq, creatorGate ⟩
```

Plan:

```text
Π(μ_k) = ⟨ steps, bindings, expectedDelta, costEstimate, risk, gate ⟩
```

Execution rule:

```text
AUTOEXEC = 0
Π(μ_k) ⇏ Execute(μ_k)
```

## 6. Runtime lease

```text
ℓ_i = ⟨ task, scope, cpu, ram, disk, network, authority, ttl, returnPath ⟩
```

Run condition:

```text
Run(n_i) = 1 ⟺ Grant_r0(ℓ_i) = 1
```

Expiry:

```text
ttl_i ≤ 0 ⟹ Revoke(n_i)
```

Violation:

```text
Violation(n_i) = 1 ⟹ Freeze → KillRuntime → PreserveEvidence
```

## 7. Authority lattice

```text
𝒜 = { OBSERVE, PLAN, ROUTE, READ, WRITE, EXECUTE, MUTATE, VERIFY, AUTH, ALLOCATE, REVOKE, KILL, PROMOTE }
```

Mapping:

```text
α : ℕ → 2^𝒜
```

Constraint:

```text
∀ n_i ≠ r_0 : α(n_i) ⊆ α(r_0)
```

Worker does not become authority by receiving input:

```text
ReceivesInput(n_i) = 1 ⇏ Authority(n_i)↑
```

## 8. Global state

```text
Z_t = ⟨ G_t, R_t, A_t, M_t, V_t, H_t, L_t, Q_t ⟩
```

No silent state change:

```text
ΔZ_t ≠ 0 ∧ Trace(ΔZ_t) = 0 ⟹ FAIL
```

## 9. OODA transition

```text
Z_{t+1} = ℱ_OODA(Z_t, O_t, D_t, A_t, E_t)

ℱ_OODA = Observe → Orient → Decide → Act → Verify
```

Execution gated:

```text
Act = 1 ⟺ Gate = APPROVED
```

## 10. Health model

```text
h : ℕ → ℋ
ℋ = { HEALTHY, PARTIAL, DEGRADED, STALE, FAILED, UNKNOWN }
```

HTTP 200 does not imply functional:

```text
HTTP200 ⇏ FUNCTIONAL
```

## 11. Evidence object

```text
e_j = ⟨ source, command, timestamp, exitCode, stdoutHash, stderrHash, artifactPath, stateBefore, stateAfter ⟩
```

Rule:

```text
PASS(x) = 1 ⟺ ∃ e_j : Supports(e_j, x) = 1
No Data ⇒ No Claim
```

## 12. Memory and canon

```text
W_m : (Z_t, e_j, ΔZ_t) → M_{t+1}
```

Canon write condition:

```text
CanonWrite = 1 ⟺ Verified = 1 ∧ Authorized = 1 ∧ LineageComplete = 1
```

Memory writer authority:

```text
α(memory_writer) = { READ, WRITE_memory }
```

No shell execution or authority mutation.

## 13. Verification surface

```text
v_t : (claim, state, artifact) → { PASS, FAIL, UNKNOWN }
```

Verification has no business authority.

## 14. Gateway and providers

Gateway routing:

```text
a_g : (request, providerPolicy, toolPolicy) → route
GatewayRoute = 1 ⇏ ToolExecute = 1
```

Port mapping:

```text
π(r_0)        = 9001
π(apo_gateway) = 9011
π(credential_broker) = 8765
π(Ollama)     = 11434
π(LMStudio)   = 1235
π(tool_j)     ∈ [8901, 8914]
```

## 15. LLM object

```text
L_i = ⟨ brand, model, version, role, voice, semantic, authority, tools, memory, qualification ⟩
```

Semantic contract:

```text
Σ* = { NoFabrication, OntologyLock, ProvenanceLock, EvidenceBound, ScopeBound, CorrectionReplay, NoSilentMutation }
```

Voice may differ, but semantics bind:

```text
BrandVoice(L_i) = voice_i
voice_i ≯ Σ*
```

## 16. LLM output object

```text
o_k = ⟨ OBS, INF, UNK, EVD, ACT, ΔZ, COST, RISK ⟩
```

Constraints:

```text
INF ⊆ Closure(OBS, EVD)
UNK ≠ ∅ ⟹ DeclareUnknown = 1
OpenError = 1 ⟹ ContextShift = 0
```

## 17. Gate system

```text
𝒦 = { K_1, K_2, ..., K_9 }
g_i ∈ { CLOSED, OPEN, COMPLETE, FAILED }
```

Gate transition:

```text
g_i : CLOSED → OPEN ⟺ CreatorApprove(K_i) = 1
¬CreatorApprove(K_i) ⟹ ¬Transition(g_i)
```

Current:

```text
g_1 = COMPLETE
∀ i ∈ {2,...,9} : g_i = CLOSED
```

## 18. Invariant vector

```text
ℐ = (I_1, ..., I_12)
```

| ID | Invariant |
|---|---|
| I_1 | AUTO_DISCOVERY = 0 |
| I_2 | AUTO_BINDING = 0 |
| I_3 | AUTO_EXECUTION = 0 |
| I_4 | AUTO_MUTATION = 0 |
| I_5 | ROOT_HOST_RESET = 0 |
| I_6 | DOCKER_RESET = 0 |
| I_7 | ECONOMY_ACTION = 0 |
| I_8 | SINGLE_MISSION_ROOT = 1 |
| I_9 | WORKER_AUTHORITY_ESCALATION = 0 |
| I_10 | UNVERIFIED_CANON_WRITE = 0 |
| I_11 | SILENT_STATE_CHANGE = 0 |
| I_12 | GATE_SKIP = 0 |

## 19. Gap object

```text
γ_i = ⟨ target, expected, observed, cause, impact, requiredGate ⟩
```

Examples:

- `γ_product` — product runtime expected HEALTHY, observed STALE, cause WindowsOnly, impact ProjectionMissing, gate K_4/K_5.
- `γ_credentials` — Slack/PSE expected FUNCTIONAL, observed HTTP200_BUT_NO_KEY, cause MissingCredential, impact ToolCallFail, gate K_6.

## 20. Local mastery metric

```text
ℳ_L = w_1O + w_2A + w_3V + w_4R + w_5C + w_6L - w_7D
```

Variables:

- `O` — observability
- `A` — authority health
- `V` — verification coverage
- `R` — recoverability
- `C` — continuity
- `L` — lineage completeness
- `D` — unresolved debt

Mastery condition:

```text
MasteryLocal = 1 ⟺ O=A=V=R=C=L=1 ∧ D ≤ D_max
```

## 21. System compression

```text
𝒜ℐ𝒪𝒮 = ⟨ 𝒢, r_0, Z_t, 𝒜, ℐ, 𝒦, ℰ, Γ, Σ* ⟩
```

Qualification law:

```text
Every object must have:
  ID + TYPE + STATE + AUTHORITY + LINEAGE + HEALTH + COST + VALUE
```

If any of the eight fields is missing:

```text
ObjectQualified = 0
```
