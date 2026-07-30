# AIOS Cleanup Canon

> Version: 2026-07-27.cleanup-canon.v1
> Authority: Nguyễn Đức Cường (Andy) — Canon Authority
> Scope: Local-first AIOS/HyperAI runtime on macOS
> Purpose: Define how every runtime system cleans its own storage, caches, logs, and temporary databases without human manual intervention.

## Canon Law

```text
USER = Andy = Creator = Canon Authority
ASSISTANT = runtime worker / scanner / reconciler / implementer
CANON is authority.
Cleanup without receipt -> invalid.
No anchor, no validity.
Artifact without anchor -> do not conclude.
Role without evidence -> UNKNOWN_KEEP.
```

## Global Cleanup Policy

1. **Every system owns its own waste.** Runtime processes must expose a cleanup path for their own caches, logs, build artifacts, and stale temporary data.
2. **Disposables are auto-approved.** Class `disposable` may be deleted by `system_cleanup_executor` without per-action approval.
3. **Recyclables require user gate when large.** Class `recyclable` over 500 MB requires an explicit `approve_recycle` receipt or an OODA cleanup mission.
4. **Protected never deleted.** Class `protected` includes source trees, model weights, canon/memory, credentials, wallets, Git objects, and user documents.
5. **Receipt required.** Every cleanup action must produce a JSON receipt with `before_bytes`, `after_bytes`, `deleted_items`, `command`, `status`.
6. **Fail closed.** If a cleanup command fails, abort that system; do not cascade. Report as `CLEANUP_PARTIAL`.
7. **Dry-run first.** Any new cleanup recipe must run `--dry-run`, show predicted impact, and only execute after proof.

## Asset Classification

| Class | Definition | Examples | Approval |
|-------|-----------|----------|----------|
| `disposable` | Regenerated automatically, no source of truth | pip/npm/pnpm cache, DerivedData, `.crdownload`, app caches, crash logs, `__pycache__` | auto |
| `recyclable` | Can be rebuilt/redownloaded but costs time | `node_modules`, HuggingFace cache, Docker images, Xcode simulator runtimes, VS Code extensions | >500MB gate |
| `protected` | User data, source, canon, credentials, models in use | `HyperAI-Sync/`, `~/.codex/`, `~/.config/devin/`, `~/.hyperai/`, `~/.ollama/models/`, `~/.ssh/`, Photos, Git repos | never without explicit |
| `unknown` | Cannot classify | kept; report to `memory/UNKNOWN_KEEP_CLEANUP.md` | manual |

## Per-System Cleanup Recipes

### 1. Python / pip / uv

- **Owner surface:** `python_runtime`, `pip_cache`
- **Disposables:**
  - `pip cache purge`
  - `find <project_roots> -type d -name __pycache__ -prune -exec rm -rf {} +`
  - `find <project_roots> -type d -name .pytest_cache -prune -exec rm -rf {} +`
  - `~/.cache/uv` if uv installed
- **Recyclables:** `~/.cache/huggingface` (embedding models) — gate >500MB
- **Protected:** `~/.local/share` app state, `~/.pyenv` versions, `~/.conda` envs

### 2. Node / npm / pnpm / yarn

- **Owner surface:** `node_runtime`
- **Disposables:**
  - `npm cache clean --force`
  - `pnpm store prune`
  - `yarn cache clean`
  - `~/.npm/_cacache` old tarball cache
- **Recyclables:** `node_modules` inside project roots (can be `npm install` again)
- **Protected:** `~/.npmrc` with auth tokens, `package-lock.json`, source files

### 3. Homebrew

- **Owner surface:** `homebrew`
- **Disposables:**
  - `brew cleanup -s`
  - `~/Library/Caches/Homebrew/downloads/*.tar.gz` older than 30 days
- **Protected:** installed Cellar, `Brewfile`, `~/.brewfile`

### 4. VS Code / Insiders

- **Owner surface:** `vscode_operator_surface`
- **Disposables (auto):**
  - `~/Library/Application Support/Code/CachedExtensionVSIXs`
  - `~/Library/Application Support/Code/Crashpad`
  - `~/Library/Application Support/Code/logs`
  - `~/Library/Application Support/Code - Insiders/CachedExtensionVSIXs`
  - `~/Library/Application Support/Code - Insiders/Crashpad`
  - `~/Library/Application Support/Code - Insiders/logs`
- **Recyclables (gate):**
  - `~/Library/Application Support/Code/Cache`
  - `~/Library/Application Support/Code/CachedData`
  - `~/Library/Application Support/Code - Insiders/Cache`
  - `~/Library/Application Support/Code - Insiders/CachedData`
- **Protected:** `User/settings.json`, `User/keybindings.json`, extensions themselves, `globalStorage` unless explicit

### 5. Xcode

- **Owner surface:** `xcode_toolchain`
- **Disposables:**
  - `~/Library/Developer/Xcode/DerivedData`
  - `xcrun simctl delete unavailable`
- **Recyclables (gate):**
  - `xcrun simctl erase all` (device content)
  - old iOS simulator runtimes in `~/Library/Developer/CoreSimulator/Profiles/Runtimes`
- **Protected:** active project archives, source-controlled code

### 6. Docker

- **Owner surface:** `docker_desktop`
- **Disposables (when daemon healthy):**
  - `docker system prune -f`
  - `docker volume prune -f`
  - `docker builder prune -f`
- **Protected:** named volumes used by `tenure` or HyperAI; do not prune without label check

### 7. Ollama

- **Owner surface:** `ollama_local_models`
- **Disposables:**
  - `~/.cache/ollama` temporary blobs
  - `~/.ollama/logs` old logs
- **Recyclables (gate):** `ollama rm <model>` for models not used in 30 days
- **Protected:** currently loaded models (`ollama ps`)

### 8. macOS System Caches

- **Owner surface:** `macos_system`
- **Disposables:**
  - `~/Library/Caches/pip`
  - `~/Library/Caches/node-gyp`
  - `~/Library/Caches/GeoServices`
  - `~/Library/Caches/com.apple.helpd`
  - `~/Library/Caches/com.apple.parsecd`
  - `~/Library/Caches/typescript`
  - `~/Library/Caches/fanal`
  - `~/Library/Caches/com.grammarly.ProjectLlama`
- **Protected:** `~/Library/Caches/ollama` while `ollama` running, `~/Library/Caches/Google` while Chrome running

### 9. Downloads / Browser leftovers

- **Owner surface:** `downloads`
- **Disposables:**
  - `*.crdownload` incomplete Chrome downloads
  - `*.part` incomplete downloads
  - `.DS_Store` files in user dirs
- **Recyclables (gate):** `.dmg`, `.pkg`, `.zip` older than 30 days in `~/Downloads`
- **Protected:** any file with name matching `*key*`, `*credential*`, `*wallet*`, `*private*`, `APO_*`

## Cleanup Triggers

- `disk_free_mb < 10240` -> run `disposable` cleanup automatically
- `disk_free_mb < 2048` -> also run `recyclable` cleanup with gate (creator surface fanout, default wait 60s then proceed if no veto)
- `disk_free_mb > 10240` for 2 consecutive cycles -> cleanup idle, log `CLEANUP_STABLE`

## Receipt Schema

Every cleanup execution must write a receipt to `runtime/federation_orchestrator/cleanup_receipts/<timestamp>_<system>.json`:

```json
{
  "schema_version": "2026-07-27.cleanup-receipt.v1",
  "system": "vscode",
  "trigger": "disk_low",
  "started_at": "ISO8601",
  "completed_at": "ISO8601",
  "dry_run": false,
  "disk_before_mb": 7000,
  "disk_after_mb": 9500,
  "actions": [
    {"command": "rm -rf ...", "status": "ok", "freed_mb": 123}
  ],
  "deleted_items": ["path1", "path2"],
  "errors": [],
  "next": "continue_monitoring"
}
```

## DO_NOT_DELETE (Protected Anchor List)

- `~/.hyperai/` (runtime recovery, consciousness, OS master)
- `~/HyperAI-Sync/` source and `memory/` canon
- `~/.codex/` skills and config
- `~/.config/devin/`
- `~/.zshenv` and other shell env with secrets
- `~/.ssh/`, `~/.gnupg/`
- `~/.ollama/models/` unless explicit model removal
- Any file matching `*private*`, `*key*`, `*credential*`, `*wallet*`, `*secret*`
- Git `.git` directories
- Apple Photos Library `*.photoslibrary`

## Integration Points

- **OS Master Survival Governor** (`workbench/hyperai_os_master.py`) triggers cleanup when `disk_state` is not `STABLE`.
- **OODA Loop** (`tools/hyperai_ooda_loop.py`) routes `"cleanup"`, `"dọn"`, `"giải phóng disk"` tasks to `system_cleanup_executor` surface.
- **Cleanup Executor** (`tools/hyperai_cleanup_executor.py`) reads this canon and runs recipes, producing receipts.
- **Verification Truth** verifies receipts and disk delta before promoting `disk_state` to `STABLE`.
