---
name: slot-local-runtime-template
description: Run the Slot Project local automation template when the task mentions local_runtime, game/admin boundary checks, training dataset counts, bot metrics, or local-only Hugging Face gating.
argument-hint: "[base-url-or-port]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Slot Local Runtime Template

## When to use

Use in `/Users/andy/Slot-project-local-full/Slot-project` for local runtime validation, browser surface checks, and local-only dataset/build verification.

Do not use for deploy/upload/push flows or Hugging Face job submission unless Andy explicitly opens that gate.

## Inputs / context to gather

1. Read `local_runtime/AUTOMATION_TEMPLATE.md` and `local_runtime/TRAINING_PLAN.md`.
2. Default base URL is `http://127.0.0.1:8130` unless `$ARGUMENTS` gives another port or URL.
3. Confirm the evidence payload expected by the user:
   - game/admin boundary
   - browser errors
   - failed requests
   - bot metrics
   - Ollama status
   - training dataset counts
   - artifact paths
   - next single fix if any

## Procedure

1. Read the two local runtime docs first.
2. Check whether the local runtime is serving the expected endpoints.
3. If the port is stale or down, start a fresh runtime:
   - `SLOT_LOCAL_PORT=8130 python3 local_runtime/server.py`
   - `export SLOT_LOCAL_URL=http://127.0.0.1:8130`
4. Run static checks:
   - `python3 -m py_compile local_runtime/server.py`
   - `node --check local_runtime/bot_runner.cjs`
   - `node --check local_runtime/split_surface_test.cjs`
   - `node --check local_runtime/build_training_datasets.cjs`
5. Probe:
   - `/api/health`
   - `/api/hyperai/ollama`
   - `/api/hyperai/training`
6. Execute:
   - `node local_runtime/build_training_datasets.cjs`
   - `node local_runtime/bot_runner.cjs`
   - `node local_runtime/split_surface_test.cjs`
7. Report concise evidence only and append the recurring automation memory note if the workflow expects it.

## Efficiency plan

- Reuse port `8130` unless there is concrete evidence it is stale.
- Fail fast on syntax checks before browser runs.
- Use `/api/health` to confirm whether a fresh server boot is necessary.
- Wait on `split_surface_test.cjs` process output before assuming a browser hang.
- Keep Hugging Face and cloud behavior local-only unless explicitly authorized.

## Pitfalls and fixes

- Symptom: `curl` cannot connect to `127.0.0.1:8130`.
  - Likely cause: no active local runtime or a stale process.
  - Fix: start a fresh local server on `8130` and export `SLOT_LOCAL_URL`.
- Symptom: dataset-building invites cloud or upload behavior.
  - Likely cause: `TRAINING_PLAN.md` was mistaken for authorization.
  - Fix: keep training local-only and preserve `cloud_upload_authorized=false` unless Andy explicitly gates upload/training.
- Symptom: `split_surface_test.cjs` fails even though the page boundaries look clean.
  - Likely cause: the script currently treats the Chrome autoplay warning `The AudioContext was not allowed to start... after a user gesture on the page.` as fatal.
  - Fix: either whitelist that warning in `local_runtime/split_surface_test.cjs` or gate audio startup behind a user gesture.
- Symptom: the report becomes a generic QA narrative.
  - Likely cause: the requested evidence schema was ignored.
  - Fix: return the specific boundary/error/metrics/artifact fields only.

## Verification checklist

- Both local runtime docs were read first.
- Static checks passed or exact failure snippets were captured.
- `/api/health`, `/api/hyperai/ollama`, and `/api/hyperai/training` were probed.
- Browser/game/admin boundary evidence and artifact paths were collected.
- Hugging Face or deploy-style actions were not taken without an explicit gate.
