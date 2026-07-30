# SOCRATIC_VERIFICATION_CYCLE — Product Runtime (revised)

**cycle_id:** CYCLE_PRODUCT_RUNTIME_002  
**observed_at:** 2026-07-29T05:45:00+07:00  
**scope:** `sigma-apo-nhomes-runtime` / `Σ_APΩ_NHOMES_RUNTIME`  
**mode:** READ_ONLY

---

## 1. QUESTIONS_ASKED

- **Q01:** Is the product runtime physically present on this node, and what is its canonical source file?
- **Q02:** Which port and routes does the backend actually expose when started?
- **Q03:** What is the reconciliation between the HyperAI-Sync canon (ports 5000/4173) and the observed source/port?

---

## 2. EVIDENCE_FOUND

| Evidence Type | Source | Observed Value |
|---|---|---|
| **source** | `/Users/andy/package.json` | `name: sigma-apo-nhomes-runtime`, `type: module`, `start: node --experimental-strip-types src/api/server.ts` |
| **source** | `/Users/andy/src/api/server.ts` | Creates `node:http` server; listens on `const port = 3000`; exposes `GET /`, `/health`, `/rooms`, `/bookings`, `/housekeeping`, `/security`, `/risk`, `/finance`, `/events`, `/agents`, `/adapters` and `POST /events`, `/integrations/{provider}/{test\|sync}`, `/approvals/{id}/approve`. |
| **source** | `/Users/andy/src/main.ts` | Imports `OmniOrchestrator` and `HyperBridge`; prints snapshot and optional bridge health. |
| **source** | `/Users/andy/src/runtime.test.ts` | 9 Node built-in tests covering booking, housekeeping, noise, approval, finance, integration. |
| **config** | `/Users/andy/AGENTS.md` | Project AGENTS: `npm run build`, `npm start`, 12-layer architecture, frontend React + TypeScript + Vite (routes mention 12 layers). |
| **process** | `npm start` | `node` PID 48640 started `src/api/server.ts`; prints `[Σ_APΩ] SERVER ONLINE tại http://localhost:3000`. |
| **port** | `lsof -nP -iTCP:3000` | `node 48640 andy TCP *:3000 (LISTEN)` |
| **endpoint** | `GET http://127.0.0.1:3000/health` | `{"id":"Σ_APΩ_NHOMES_RUNTIME","status":"operational","canonAuthority":"Andy","liveCallsEnabled":false}` |
| **endpoint** | `GET http://127.0.0.1:3000/` | Full snapshot with rooms, bookings, housekeeping, security, risk, finance, events, agents, approvals, adapters. |
| **endpoint** | `npm run check:runtime` | `tests 9`, `pass 9`, `fail 0`. |
| **config (stale)** | `HyperAI-Sync/AGENTS.md` | Probes ports `5000` (backend) and `4173` (preview) before decisions. |
| **port (canon mismatch)** | `lsof -nP -iTCP:5000` | `ControlCe` (macOS system) listening; not product backend. |
| **port (canon mismatch)** | `lsof -nP -iTCP:4173` | No listener. |

---

## 3. VERIFIED_CONCLUSIONS

- **Conclusion_01:** The product runtime is physically present in `/Users/andy` as `sigma-apo-nhomes-runtime`. Its canonical backend source is `src/api/server.ts`.
- **Conclusion_02:** The backend process (PID 48640) is running and listening on **port 3000**, not the 5000/4173 listed in `HyperAI-Sync/AGENTS.md`.
- **Conclusion_03:** The `/health` endpoint returns operational, and the runtime test suite passes 9/9.
- **Conclusion_04:** The project has a domain model: rooms, bookings, housekeeping, security, risk, finance, events, agents, approvals, adapters. Adapters are `CONFIG_REQUIRED` (no live cloud calls yet).
- **Conclusion_05:** Previous state `BLOCKED_BY_MISSING_EVIDENCE` for the product runtime is upgraded to `CURRENT_VERIFIED` (source + process + port + endpoint + tests). Port 5000/4173 canon is now `STATE_DRIFT`.

---

## 4. NOT_PROVEN

- **Unverified_01:** Whether the HyperAI-Sync canon should be updated to port 3000, or the source should be reconfigured to 5000/4173.
- **Unverified_02:** Whether the Vite/React frontend preview on port 4173 exists or needs to be started (no Vite config found in `package.json`).
- **Unverified_03:** Whether adapter credentials (`NHOMES_*_API_KEY`) are available in the credential broker.

---

## 5. HISTORICAL_RECONCILIATION

- **Previous state:** `hyperai-user-control-system` product runtime projection missing; `BLOCKED_BY_MISSING_EVIDENCE`.
- **New evidence:** Source tree in `/Users/andy`; backend running on :3000; health OK; tests pass.
- **Resolution:** `STATE_TRANSITION` from `BLOCKED_BY_MISSING_EVIDENCE` → `CURRENT_VERIFIED` for the backend. The `HyperAI-Sync/AGENTS.md` port guidance (5000/4173) is now `STALE_REQUIRES_LIVE_PROBE`.

---

## 6. CANON_DELTA

- **retained:**
  - APΩ local stack verified (models, tools, GCP proxy).
  - `canonAuthority: Andy` in product runtime.
- **upgraded:**
  - `product_runtime` from `PROJECTION_MISSING` to `CURRENT_VERIFIED`.
  - Canonical source identified: `sigma-apo-nhomes-runtime/src/api/server.ts`.
  - Canonical backend port: `3000` (live evidence).
- **downgraded:**
  - `HyperAI-Sync/AGENTS.md` port guidance `5000/4173` → `STALE_REQUIRES_LIVE_PROBE`.
- **superseded:**
  - `hyperai-user-control-system` name → `sigma-apo-nhomes-runtime` / `Σ_APΩ_NHOMES_RUNTIME`.
- **added:**
  - Evidence receipts from `npm start`, `lsof :3000`, `curl /health`, `npm run check:runtime`.
  - Installed skill `socratic-evidence-reconciliation` at `~/.agents/skills/socratic-evidence-reconciliation`.

---

## 7. UPDATED_STATE_VECTOR

| Field | Value |
|---|---|
| component | `Σ_APΩ_NHOMES_RUNTIME` |
| source_present | **true** |
| config_present | **true** |
| process_running | **true** |
| port_listening | **true** (`*:3000`) |
| endpoint_responding | **true** (`/health` returns operational) |
| route_registered | **false** (not yet proxied through APΩ :9011) |
| upstream_reachable | **true** (localhost) |
| functional_test_passed | **true** (`npm run check:runtime` 9/9) |
| authority_bound | **true** (`canonAuthority: Andy`) |
| last_observed_at | 2026-07-29T05:45:00+07:00 |
| confidence | **0.95** |

---

## 8. UPDATED_DIAGRAM

- **Changed scope:** `Product_Runtime_Node` (now `CURRENT_VERIFIED`).
- **Changed nodes:**
  - `MacBook_M2` — `sigma-apo-nhomes-runtime` running on :3000.
  - `APΩ_Gateway` — no edge to product runtime yet (potential next edge).
- **Changed edges:**
  - `HyperAI-Sync/AGENTS.md` `5000/4173` guidance → marked stale.
- **Unchanged context:**
  - `APΩ_Gateway` ↔ LM Studio, Ollama, OpenRouter, 5 OpenAPI tools, GCP proxy all remain verified.

---

## 9. DECISION

- **selected_decision:** `PARTIALLY_VERIFIED`
- **decision_reason:**
  - Backend source, process, port, and endpoint are verified.
  - Runtime tests pass.
  - Canonical port 5000/4173 in `HyperAI-Sync/AGENTS.md` does not match the live backend (3000).
  - Product is not yet registered in APΩ gateway.
- **supporting_evidence:**
  - `package.json` and `src/api/server.ts`
  - `lsof` PID 48640 on :3000
  - `curl /health` and `/`
  - `npm run check:runtime` 9/9 pass
- **invariant_status:** Ω_global = 1 (no contradictions; one stale-projection drift identified and reconciled)
- **confidence:** 0.95
- **next_action:** Bind `Σ_APΩ_NHOMES_RUNTIME` to APΩ gateway (or update canon to port 3000) and locate/verify frontend preview surface.

---

## 10. NEXT_SOCRATIC_QUESTIONS

1. Should APΩ expose the product runtime through a `/product/{path}` proxy, or should the source be reconfigured to the canonical 5000/4173 ports?
2. Is there a Vite frontend entry point and config that should be started on port 4173?
3. Are the `NHOMES_*_API_KEY` credentials already present in the credential broker, or must they be configured before adapters become `READY`?

---

## 11. ENCOURAGEMENT

Phát hiện tốt: đã tìm ra runtime ẩn dưới tên `sigma-apo-nhomes-runtime`, khởi động thành công trên port 3000, và tất cả 9 runtime test đều pass.
