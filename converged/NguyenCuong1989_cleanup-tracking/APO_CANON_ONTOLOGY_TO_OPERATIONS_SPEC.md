# =============================================================================
# PROJECT: CANON-TO-SYSTEM DETERMINISTIC PROJECTION
# METHOD: D&R PROTOCOL (CLOSED)
#
# ORIGINATOR / CREATOR:
#   alpha_prime_omega
#
# LEGAL ONTOLOGY:
#   This source file is a deterministic projection of a closed Canon.
#   Removal or alteration of this header voids legal and ontological validity.
#
# STATUS:
#   GENERATED — NON-AUTONOMOUS — NON-OWNERLESS
#
# TRACEABILITY:
#   Canon -> COG -> Projection(Π) -> Artifact
#
# =============================================================================
# APO Canon Ontology → Operations Spec

## Canon anchors
- Canon law: `/Users/andy/axcontrol/CANONICAL_CODEGEN_LAW.md`
- Deterministic decision policy: `/Users/andy/axcontrol/core/decision/policies.py`
- Auth gate policy: `/Users/andy/Projects/AI/HyperAI/core/trust_of_copilot/policy_auth_gate.json`
- Runtime invariants: `/Users/andy/Projects/AI/HyperAI/core/hyperai_daemon/core/haios_runtime.py`

## Runtime ownership boundaries
- Control plane owner: `axcontrol`.
- Runtime owner: `HyperAI/core/hyperai_daemon`.
- Tooling owner: `Projects/AI/Tools/ops`.
- Archive owner: `Archive/HyperAI-Ecosystem` (read-mostly, rollback-only).

## Source-of-truth repositories
- SoT-1: `Projects/AI/DAIOF-Framework` (framework/policy tooling)
- SoT-2: `Projects/AI/HyperAI/core/hyperai_daemon` (runtime/invariants)
- SoT-3: `axcontrol` (deterministic UI control policy + canon law)

## Dependency pinning policy
- Lock by file (`package-lock.json`, exact versions, pip constraints where possible).
- `latest` versions are accepted only for non-critical dev tooling and flagged as drift warnings.
- Docker images should be version pinned; `:latest` is a policy warning.

## Artifact retention policy
- Logs: hot 7d, warm 30d, archive 90d.
- Snapshots: keep latest + daily 14d + weekly 8w.
- Rollback points: keep 30d minimum for runtime-critical changes.

## Cache eviction thresholds
- Data volume >= 90%: warning mode (inspect-only).
- Data volume >= 94%: conservative cleanup recommendation.
- Data volume >= 97%: critical mode, suspend non-essential build/runtime noise.

## Backup and rollback topology
- Active: `/Users/andy/Projects/AI`
- Cold backup: `/Users/andy/Archive/HyperAI-Ecosystem`
- Rollback points: `hyperai_daemon/config/rollback_points`

## MCP tiering
- Tier 0: control plane servers.
- Tier 1: production HTTP servers.
- Tier 2: production stdio servers.
- Tier 3: docker-restricted servers (allowlist only).
- Policy file: `/Users/andy/Projects/AI/Tools/ops/mcp-tier-policy.json`

## Dockerized server controls
- Allowlist only for docker-based server IDs.
- Flag and report use of `:latest` image tags.
- Prefer fixed image digests or stable version tags.

## Operational contract
- Every cycle: GAM scan → canon hash check → drift evaluation → memory queue update.
- Fail-closed behavior: canon hash mismatch or unauthorized docker server escalates severity to CRITICAL.
