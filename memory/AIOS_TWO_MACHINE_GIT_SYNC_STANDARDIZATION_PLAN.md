# AIOS Two-Machine Git Sync Standardization Plan

Date: 2026-04-15

## Purpose

Creator works across at least two physical machines:

- Titan GT77 Windows root host, current active local operator surface.
- MacBook, observed through creator-copied terminal evidence and cloud inventory.

The goal is to keep the ecosystem synchronized through Git and evidence artifacts without flattening sediment, deleting archives, or promoting stale copies as authority.

## Current Titan Evidence

Read-only scan artifacts:

- `runtime/lineage/local_physical_git_inventory_20260415.json`
- `runtime/lineage/local_git_repo_inventory_20260415.json`

Current measured facts:

- Titan user profile contains many Git repositories and nested repository strata.
- `C:\Users\pc\aidev` is the preferred live lineage root for `https://github.com/sowhat1989/aidev.git`.
- `https://github.com/sowhat1989/aidev.git` appears in many duplicate/archive/backup paths, including `CascadeProjects`, `Documents`, `AI_EMERGENCY_VAULT`, `_CONSOLIDATED`, `VSCode-Extensions-Backup`, and `C:\Users\pc\aidev`.
- `C:\Users\pc\aidev` is dirty and must not be overwritten, reset, staged, committed, or pushed without a dirty-state ledger.
- `C:\Users\pc\HyperAI_Phoenix_Master` remains the current control habitat.
- `hyperai-user-control-system` remains the current product shell authority.

## Sync Invariant

Git is the synchronization transport, not automatic authority.

```text
physical path -> repo role -> git remote/branch -> dirty ledger -> sync decision -> patch/push/pull
```

No machine should pull, push, reset, checkout, merge, or clean a repo until the local dirty state is recorded.

## Repository Role Classes

Use these classes before any synchronization:

- `authority-live`: active source or runtime substrate used by the current system.
- `preferred-lineage`: canonical historical/source lineage that should be protected and reconciled first.
- `working-copy`: usable development copy with possible local changes.
- `archive-sediment`: preserved backup or historical stratum, not a direct sync target.
- `tool-extension`: plugin/extension repo used by a local AI/editor surface.
- `generated-checkpoint`: repo-like checkpoint created by an editor/agent backup system.
- `external-reference`: third-party source checked out for reading or comparison.
- `unknown`: must remain read-only until classified.

## Current Classification Seed

| Path | Remote | Role | Sync status |
| --- | --- | --- | --- |
| `C:\Users\pc\HyperAI_Phoenix_Master` | none observed by git probe | `authority-live` / control habitat | memory-first, do not force Git authority |
| `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system` | none observed by git probe | `authority-live` / product shell | CI/runtime truth local |
| `C:\Users\pc\aidev` | `https://github.com/sowhat1989/aidev.git` | `preferred-lineage` / backend-source substrate | dirty, requires ledger before sync |
| `C:\Users\pc\CascadeProjects\aidev_project*` | `https://github.com/sowhat1989/aidev.git` | `archive-sediment` or `working-copy` pending proof | no direct sync |
| `C:\Users\pc\HyperAI_Phoenix_Master\AI_EMERGENCY_VAULT\*` | mixed | `archive-sediment` | preserve, do not delete |
| `C:\Users\pc\HyperAI_Phoenix_Master\_CONSOLIDATED\*` | mixed | `archive-sediment` | preserve, do not delete |
| `C:\Users\pc\.gemini\extensions\*` | third-party extension remotes | `tool-extension` | preserve, do not uninstall |
| `C:\Users\pc\.codex\vendor_imports\skills` | OpenAI skills remote | `tool-extension` | preserve |

## Two-Machine Sync Protocol

### Phase 1: Titan Read-Only Ledger

- Record all Git roots, remotes, branches, heads, dirty status.
- Record physical top-level inventory with common generated directories excluded.
- Mark duplicate remotes and nested repository strata.
- Do not stage, commit, pull, push, reset, checkout, clean, move, or delete.

### Phase 2: MacBook Read-Only Ledger

Run equivalent read-only inventory on MacBook and commit or copy only the resulting inventory artifact into a designated sync evidence path.

Required MacBook evidence fields:

- host identity
- root scanned
- repo path
- remote URL
- branch
- HEAD
- dirty status
- role guess
- timestamp

### Phase 3: Cross-Machine Reconciliation

Compare Titan vs MacBook by:

- remote URL
- branch
- HEAD
- dirty state
- path role
- artifact timestamp

Classification outcomes:

- `same-head-clean`: safe candidate for normal Git pull/push.
- `same-head-dirty`: requires local diff review before sync.
- `diverged-clean`: requires branch/rebase/merge decision.
- `diverged-dirty`: high-risk; freeze until patch ledger exists.
- `remote-duplicate-archive`: keep as sediment, not direct sync target.
- `missing-on-peer`: decide whether clone is needed or the path is local-only.

### Phase 4: Structure Standardization

Standardization must be a metadata map before physical movement.

Target logical structure:

```text
root-host/
  control-habitat/        -> HyperAI_Phoenix_Master
  product-shell/          -> hyperai-user-control-system
  preferred-lineage/      -> aidev
  provider-fabric/        -> quantumreason/local fakeAPI substrate
  tool-extensions/        -> Codex/Gemini/VS Code extension repos
  cloud-substrate/        -> GCP/Azure/other cloud observation ledgers
  archive-sediment/       -> emergency vaults, consolidated backups, checkpoint strata
  evidence-ledgers/       -> machine inventories, sync decisions, drift reports
```

This logical structure should be written as registry metadata first. Physical moves require a separate mission, backup proof, and rollback plan.

## Stop Rules

Do not:

- delete duplicate folders
- run `git reset --hard`
- run `git clean`
- auto-pull across dirty repos
- auto-push creator changes
- rewrite nested backup histories
- uninstall or normalize MCP/extension repos
- treat app label or remote name as capability proof
- promote MacBook-copied evidence to Titan live truth without a matching read-only ledger

## Next Safe Step

Create a machine-readable sync registry that records:

```text
repo_path -> role_class -> remote -> branch -> head -> dirty_status -> machine -> sync_recommendation
```

Then produce a MacBook-compatible read-only inventory command so both machines emit the same schema.
