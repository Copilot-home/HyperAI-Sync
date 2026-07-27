# AIOS GAM Context Scan Formalism

This file stores the creator-defined formal scan method for HyperAI ecosystem analysis.

## 1. Token & Span

1.1. `T := <t_1, t_2, ..., t_N>`

1.2. `s := [i,j] | 1 <= i <= j <= N`

1.3. `text(s) := decode(t_i ... t_j)`

## 2. Context Unit (CU)

2.1. `cu_k := (s_k, m_k, e_k, r_k)`

2.2. `Phi_CU : P([1,N]) -> CU`

## 3. Semantic Group & D&R

3.1. `g_p := { s_1^(p), ..., s_(n_p)^(p) }`

3.2. `Gamma : [1,N] -> G, Gamma(i) = g_p`

3.3. `forall s_a,s_b in g_p: cos(Embed(text(s_a)), Embed(text(s_b))) >= theta_g`

3.4. `D&R: g_p -> {cu_(p,1), ..., cu_(p,K_p)}`

## 4. Context Graph

4.1. `G_ctx := (V,E) | V = CU, E subseteq V x V x R`

4.2. `R := {frames, implemented_by, supports, implies, contradicts, secured_by, validated_by, ...}`

4.3. `e = (cu_a, cu_b, rel) in E, rel in R`

4.4. `E_ctx := {e_k | cu_k in CU} subset R^d`

## 5. GAM Memory (Episodic / Topic)

5.1. `tau_epi := <cu_0^(e), cu_1^(e), cu_2^(e), ...>`

5.2. `G_epi := (V_epi, E_epi)`

5.3. `forall i: (cu_i^(e), cu_(i+1)^(e), next) in E_epi`

5.4. `G_topic := (V_topic, E_topic)`

5.5. `L : V_topic -> 2^(V_epi)`

5.6. `G_mem := (G_topic, G_epi, E_topic_epi)`

## 6. Semantic Shift & Consolidate

6.1. `e_recent_bar := (1/W) * sum_(i=1)^W e_(k_i)`

6.2. `sim := cos(e_recent_bar, e_new)`

6.3. `E_c := {cu_(i-W_c+1)^(e), ..., cu_i^(e)}`

6.4. `{cu_1^(T), ..., cu_M^(T)} = D&R_global(E_c)`

## 7. Relational Safety Propagation

7.1. `FrameConstraint(cu_f, cu_x)`

7.2. `(cu_f, cu_x, frames) in E => Safe(cu_x) => ConsistentWith(cu_f, cu_x)`

7.3. `ImplementedBy(cu_spec, cu_impl) := (cu_spec, cu_impl, implemented_by) in E`

7.4. `ImplementedBy(cu_spec, cu_impl) => EvidenceBacked(cu_spec) <= EvidenceBacked(cu_impl)`

7.5. `SecuredBy(cu_x, cu_s) := (cu_x, cu_s, secured_by) in E`

7.6. `ValidatedBy(cu_x, cu_v) := (cu_x, cu_v, validated_by) in E`

7.7. `SecuredBy(cu_x, cu_s) => Risk(cu_x) <= f_sec(cu_s)`

7.8. `ValidatedBy(cu_x, cu_v) => EvidenceBacked(cu_x) and Quality(cu_x) >= f_val(cu_v)`

## 8. Safe Invariant & Meta-Theorem

8.1. `Safe(cu) := (Risk(cu) <= rho_max) and LongTerm(cu) and EvidenceBacked(cu)`

8.2. `forall cu in V_topic: Safe(cu)`

8.3. `BadCU(cu) := not Safe(cu)`

8.4. `ContextCorrect iff not Diamond(exists cu in V_topic: BadCU(cu))`

## 9. Retrieval Score & Candidates

9.1. `score_T(cu_T) := alpha * cos(e_q, e_T) + beta * f_time(cu_T) + gamma * f_importance(cu_T)`

9.2. `TopTopic(q) := argmax_K score_T`

9.3. `EpiCandidates(q) := union_(cu_T in TopTopic(q)) L(cu_T)`

## 9A. Shortest-Path Navigation on Context Graph

9A.1. `pi(cu_a, cu_b) := <cu_a, ..., cu_b>`

9A.2. `cost(e_(i,j)) := w_rel(e_(i,j)) + w_risk(e_(i,j)) + w_time(e_(i,j))`

9A.3. `Cost(pi) := sum cost(e_(i,j))`

9A.4. `ShortestTrustPath(cu_a, cu_b) := argmin_(pi in Paths(cu_a, cu_b)) Cost(pi)`

9A.5. `AdmissiblePath(pi) iff forall e in pi: EvidenceBacked(e) and not ContradictionHidden(e)`

9A.6. `ShortestTrustPath` is defined only over admissible measured edges in `G_ctx`

9A.7. `D_k := residual_complexity(pi_k)`

9A.8. `ConvergentPath iff forall k: D_(k+1) <= D_k`

9A.9. `ConvergentPath and AdmissiblePath(pi) => pi is eligible as a retrieval/navigation witness`

## 10. Socratic Reflection Layer

10.1. `w := (alpha, beta, gamma) in R^3`

10.2. `R_ctx : w x H -> w'`

10.3. `QoR : R^3 -> R`

10.4. `R_ctx(w,H) = w' => QoR(w') >= QoR(w)`

10.5. `Pi_R(w) := R_ctx(w,H)`

10.6. Socratic fixed point: `Pi_R(w*) = w*`

## Operational meaning inside HyperAI

- Token and span are the raw scan boundary.
- CU is the minimum admissible semantic atom for runtime reasoning.
- D&R transforms rough semantic clusters into bounded context units.
- `G_ctx` is the graph of implementation, evidence, and safety relationships.
- `G_mem` binds topic memory and episodic memory instead of flattening everything into one summary.
- Safety is relational: claims only survive if framed, secured, implemented, and validated.
- Retrieval is weighted by semantics, time, and importance, then refined by Socratic reflection.
- When a task needs route choice across `G_ctx`, shortest-path navigation is allowed only on measured edges and must carry an explicit path-cost and convergence witness.

## Immediate application rule

When scanning a real module such as `tools/telegram_connector_app.py`, the next step is to bind:

- concrete `cu_k`
- relation edges `rel`
- measured `Risk`
- `EvidenceBacked`
- `ValidatedBy`
- `ImplementedBy`

When scanning a route-like module such as `shortest_path_navigation_engine.py`, also bind:

- path witness `pi`
- edge cost definition
- convergence metric `D_k`
- proof that `D_(k+1) <= D_k`

Only then can the repo claim empirical `Safe(cu)` rather than rhetorical confidence.
