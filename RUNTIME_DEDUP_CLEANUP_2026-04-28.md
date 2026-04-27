# Runtime Dedup Cleanup — 2026-04-28

## Objective
Safely reduce duplicated runtime app artifacts accumulated during incremental system growth, without touching canon/source-critical assets.

## Scope
- `/Users/andy/.vscode/extensions`
- `/Users/andy/Downloads/.vsix-temp`

## Scan-first findings (before cleanup)
- Extension directories: `158`
- Duplicate extension IDs: `6`
- Orphan hidden extension dirs (missing package.json): `7`
- Data volume: `400Gi used, 29Gi free, 94%`

### Duplicate extension IDs detected
- `ms-python.debugpy`
- `ms-python.vscode-python-envs`
- `ms-azuretools.vscode-azure-mcp-server`
- `dart-code.dart-code`
- `vscjava.vscode-maven`
- `ms-python.vscode-pylance`

## Actions executed
1. Removed orphan hidden extension directories without `package.json` (7 dirs).
2. Kept newest version per duplicate extension ID and removed older versions (6 dirs).
3. Removed temporary converted VSIX cache folder `/Users/andy/Downloads/.vsix-temp`.

## Removed artifacts summary
- Total removed entries: `14`
  - Orphan hidden dirs: `7`
  - Old duplicate versions: `6`
  - Temp cache folders: `1`

## Post-cleanup verification
- Extension directories: `145`
- Duplicate extension IDs: `0`
- Orphan hidden extension dirs: `0`
- Data volume: `400Gi used, 29Gi free, 94%`

## Safety notes
- No canon/policy/source repo paths were modified.
- Only disposable runtime artifacts and superseded extension versions were removed.
- Active latest extension versions were explicitly preserved.

## Outcome
Runtime extension layer is now normalized (no duplicate IDs, no orphan extension dirs), reducing extension-state conflicts and stale-path bug probability.
