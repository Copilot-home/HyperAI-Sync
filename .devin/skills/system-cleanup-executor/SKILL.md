# system-cleanup-executor

Use this skill when the HyperAI local runtime needs to free disk space, prune stale caches, logs, build artifacts, or temporary databases across the AI ecosystem on macOS.

## When to use

- `df` shows `/System/Volumes/Data` capacity over 90%.
- `hyperai_os_master.py` reports `disk_state` as `MINIMUM_RECOVERED` or `CRITICAL`.
- A user task contains keywords: `cleanup`, `clean`, `dọn`, `giải phóng disk`, `free space`, `prune`, `prune cache`, `truncate logs`.
- An OODA mission is routed to the `system_cleanup_executor` surface.

## Authority and gates

- **Canon source of truth:** `HyperAI-Sync/memory/AIOS_CLEANUP_CANON.md`
- **Executor entrypoint:** `HyperAI-Sync/tools/hyperai_cleanup_executor.py`
- **Approval rule:**
  - Class `disposable` -> auto-execute.
  - Class `recyclable` over 500 MB -> require explicit creator approval or an open `approve_recycle` gate in the mission contract.
  - Class `protected` -> never delete without creator explicit instruction.
- **Receipt rule:** every execution must produce a JSON receipt. Cleanup without receipt is invalid.

## Quick usage

### Dry run all disposable systems

```bash
python3 HyperAI-Sync/tools/hyperai_cleanup_executor.py --systems all --dry-run
```

### Execute cleanup for one system

```bash
python3 HyperAI-Sync/tools/hyperai_cleanup_executor.py --systems vscode
```

### Execute cleanup for multiple systems

```bash
python3 HyperAI-Sync/tools/hyperai_cleanup_executor.py --systems pip,npm,vscode,xcode
```

### Auto mode (OS master calls this)

```bash
python3 HyperAI-Sync/tools/hyperai_cleanup_executor.py --auto
```

`--auto` runs only `disposable` recipes when `disk_free_mb < 10240` and adds `recyclable` recipes when `disk_free_mb < 2048` after gate.

## System recipes

| System | Disposable actions | Recyclable actions | Protected (never) |
|--------|--------------------|--------------------|-------------------|
| `pip` | `pip cache purge`, `__pycache__`, `.pytest_cache` | `~/.cache/huggingface` | `~/.local/share`, `~/.pyenv`, `~/.conda` |
| `npm` | `npm cache clean --force`, `~/.npm/_cacache` | `pnpm store prune`, `node_modules` | `~/.npmrc` with tokens, `package-lock.json` |
| `homebrew` | `brew cleanup -s` | old downloads >30 days | Cellar, `Brewfile` |
| `vscode` | `CachedExtensionVSIXs`, `Crashpad`, `logs` | `Cache`, `CachedData` | `User/settings.json`, extensions, `globalStorage` |
| `xcode` | `DerivedData`, `simctl delete unavailable` | `simctl erase all`, old runtimes | archives, source |
| `docker` | `system prune`, `volume prune`, `builder prune` | none (daemon must be healthy) | named volumes for `tenure` / HyperAI |
| `ollama` | `~/.cache/ollama`, old logs | `ollama rm` for stale models | currently loaded models |
| `macos` | `~/Library/Caches/pip`, `node-gyp`, `GeoServices`, `helpd`, `parsed`, `typescript`, `fanal`, `Grammarly` | `Google` cache (stop Chrome first) | running app caches |
| `downloads` | `*.crdownload`, `*.part`, `.DS_Store` | `.dmg`/`.zip` >30 days | `*key*`, `*private*`, `*credential*`, `*wallet*`, `APO_*` |

## Receipt location

```
HyperAI-Sync/runtime/federation_orchestrator/cleanup_receipts/<timestamp>_<system>.json
```

Agents must read the latest receipt and verify `disk_after_mb` before reporting cleanup success.

## Integration with OODA

When a cleanup task enters `tools/hyperai_ooda_loop.py`, the loop:

1. Classifies task as `runtime_cleanup`.
2. Selects `system_cleanup_executor` surface.
3. Dispatches mission with `--systems` derived from the task (default `auto`).
4. Verifies receipt and disk delta.
5. Updates `memory/` with closure.

## Fail closed

- If any recipe command fails, stop that system only; do not cascade.
- If `disk_after_mb` is not better than `disk_before_mb`, mark `CLEANUP_PARTIAL` and escalate.
- Never delete a path matching `DO_NOT_DELETE` in the canon.

## No-Hack Zone

- Do not use `rm -rf /` or broad wildcard deletions.
- Do not delete `~/.hyperai/`, `~/HyperAI-Sync/`, `~/.codex/`, `~/.config/devin/`, `~/.zshenv`, `~/.ssh/`, `~/.gnupg/`, `~/.ollama/models/`, Git repos, Photos libraries, or any `*key*`/`*private*`/`*credential*`/`*wallet*`/`*secret*` file without explicit creator instruction.
