# AIOS SyncLane Bootstrap Sequence

## Status

- `orchestration_mode`: `GAM physical-scan + HyperAI local-first reconcile`
- `agent_chain_status`: `not_invoked`
- `scope`: `canonical_source_lane bootstrap`

## Sequence

1. Materialize a clean source lane outside runtime habitats.
2. Install the governed whitelist and narrow `.gitignore`.
3. Initialize a local Git repo in the lane only.
4. Write lane inventory proof.
5. Write dirty ledger proof.
6. Hold at `compare_only` until the peer lane exists.

## Titan

- Lane root: `C:\Users\pc\HyperAI-Sync`
- Source habitat: `C:\Users\pc\HyperAI_Phoenix_Master`
- Runtime habitats excluded by rule:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\dist*`
  - any `node_modules/`
  - caches, logs, DB files, secrets, archives

## MacBook

- Planned lane root: `/Users/andy/HyperAI-Sync`
- Forbidden source: `/Users/andy/Documents/GitHub/hyperAI`
- Required mode: `read_only_inventory` before any transport decision

## Stop Rules

- No `git pull`, `git push`, `git reset`, or `git clean` on runtime/package repos.
- No sync decision without `dirty_ledger`.
- No promotion of runtime artifact repos into source authority.
