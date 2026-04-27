# APO Industrial Autonomous Master Plan

## Canon anchor
- Canon file: `/Users/andy/axcontrol/CANONICAL_CODEGEN_LAW.md`
- SHA-256: `5a4f750b598dcac220025a70839b123f6a1dcf1ee17099ca1cc25dd13eedcba7`
- Canon status: locked as deterministic policy source for this rollout.

## GAM baseline (live evidence)
- Data volume: `94%` (`/System/Volumes/Data`)
- Active ecosystem:
  - `/Users/andy/Projects/AI`: ~`7.8G`
  - `/Users/andy/Archive/HyperAI-Ecosystem`: ~`5.3G`
- Observed high-pressure runtime zones:
  - Heavy IDE/runtime multiprocess activity (VS Code + helper processes)
  - Docker-backed MCP entries still present in `mcp.json`

## Industrial zoning model (L0-L4)

### L0 — Canon & Control Plane (immutable intent)
- `/Users/andy/axcontrol` (policy/canon origin)
- Canon inputs must be hash-anchored and tracked before structural actions.

### L1 — Active Source Plane (production-editable)
- `/Users/andy/Projects/AI/HyperAI`
- `/Users/andy/Projects/AI/DAIOF-Framework`
- Rule: only source + deterministic configs, no uncontrolled binary dump.

### L2 — Runtime Plane (ephemeral execution)
- Local process/runtime state, temp execution artifacts, active MCP runtimes.
- Rule: recoverable artifacts; keep retention windows tight.

### L3 — Dependency Plane (rebuildable)
- `node_modules`, `.venv`, package caches, generated build assets.
- Rule: pin versions, enforce reproducibility, allow purge/regenerate.

### L4 — Archive Plane (cold storage)
- `/Users/andy/Archive/HyperAI-Ecosystem`
- Rule: immutable snapshots, rollback-only, no active runtime dependencies.

## Autonomous execution board (detailed)
1. Canon hash lock and policy source mapping.
2. Disk/process/runtime GAM baseline capture.
3. Physical tree + size heatmap export.
4. Source-of-truth repo registry (owner + purpose + criticality).
5. Runtime service registry (process, port, lifecycle owner).
6. Dependency registry (npm/pip/system) with pin strategy.
7. Artifact taxonomy (cache/build/log/model/backup).
8. Retention policy by class (7d/30d/90d/cold).
9. Critical-path protection rules (never-delete set).
10. Drift detection policy (path + hash + process anomalies).
11. MCP topology policy (HTTP vs stdio vs docker tiers).
12. Docker MCP control gates (allowed image list + health checks).
13. Memory anti-drift protocol (snapshot -> queue -> import).
14. Launch schedule + backoff policy.
15. Failure-mode playbook (warn/degrade/abort).
16. Rollback map for every mutating operation.
17. Verification suite (disk/process/path/hash).
18. Audit logging and changelog commit policy.
19. Human override and emergency stop controls.
20. Weekly reconciliation + monthly hardening cycle.

## Deployment decisions for this run
- Implement `scan-gam.sh` as baseline collector.
- Implement `drift-memory-guard.sh` as autonomous watcher.
- Install `launchd` job to execute periodic guard + memory snapshots.
- Persist anti-drift preference in Copilot memory for future sessions.

## Output contract
- Snapshot folder: `/Users/andy/Projects/AI/Tools/ops/memory-snapshots`
- Logs folder: `/Users/andy/Projects/AI/Tools/ops/logs`
- Alert folder: `/Users/andy/Projects/AI/Tools/ops/alerts`
- Queue file for memory import: `latest-memory-queue.md`
