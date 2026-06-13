# Ecosystem Evidence Map

Generated: 2026-06-09

This report is an evidence-first map of the current local GPT/Codex/finalAI/software-factory ecosystem. It separates verified facts from inferred architecture and open checks.

## Verified Roots

### Workspace and relocation

- Workspace root: `/Users/cuongnguyen/Workspace`
- Active project symlink: `/Users/cuongnguyen/Workspace/Projects/finalAI`
- Symlink target: `/Users/cuongnguyen/.workspace_payload_store/Projects/finalAI`
- Relocation manifest: `/Users/cuongnguyen/Workspace/WORKSPACE_RELOCATION_MANIFEST.tsv`

Verified relocation entries:

- `/Users/cuongnguyen/Workspace/Projects/finalAI` -> `/Users/cuongnguyen/.workspace_payload_store/Projects/finalAI`
- `/Users/cuongnguyen/Workspace/Projects/dev_zone` -> `/Users/cuongnguyen/.workspace_payload_store/Projects/dev_zone`
- `/Users/cuongnguyen/Workspace/Projects/chatgpt-apps` -> `/Users/cuongnguyen/.workspace_payload_store/Projects/chatgpt-apps`
- `/Users/cuongnguyen/Workspace/Projects/finalAI.worktrees` -> `/Users/cuongnguyen/.workspace_payload_store/Projects/finalAI.worktrees`
- `/Users/cuongnguyen/Workspace/System/Runtime/finalAI-venv` -> `/Users/cuongnguyen/.finalai_runtime_store/venvs/finalAI`
- `/Users/cuongnguyen/Workspace/System/Runtime/finalAI-data` -> `/Users/cuongnguyen/.finalai_runtime_store/data/finalAI`

### Factory/runtime stores

- Factory state: `/Users/cuongnguyen/.factory`
- Zed factory state: `/Users/cuongnguyen/zed/.factory`
- finalAI runtime data: `/Users/cuongnguyen/.finalai_runtime_store/data/finalAI`
- finalAI runtime venv: `/Users/cuongnguyen/.finalai_runtime_store/venvs/finalAI`
- finalAI payload store: `/Users/cuongnguyen/.workspace_payload_store/Projects/finalAI`

Observed runtime-store files:

- `/Users/cuongnguyen/.finalai_runtime_store/data/finalAI/vscode_master_loop.log`
- `/Users/cuongnguyen/.finalai_runtime_store/data/finalAI/vscode_file_tracker_latest.json`
- `/Users/cuongnguyen/.finalai_runtime_store/data/finalAI/vscode_file_tracker.log`
- `/Users/cuongnguyen/.finalai_runtime_store/data/finalAI/vscode_telemetry_bridge.log`

## finalAI Project Evidence

### Git state

- Git repository root: `/Users/cuongnguyen/.workspace_payload_store/Projects/finalAI`
- Current branch: `main`
- Latest observed commits:
  - `de61618 DOC: Add orchestration system completion summary`
  - `dcb188c FEATURE: Complete cross-service orchestration system`
  - `f866579 Update customization: fix.agent.md`
  - `2f9ac21 FEATURE: Add filesystem analyzer for system self-discovery and physical architecture mapping`
  - `2805285 DEPLOYED: Full system activation with HTTP fallback - all components operational`
- Untracked nested directories observed:
  - `docker-desktop-fork`
  - `docker-local`

### Project descriptor

Source: `/Users/cuongnguyen/Workspace/Projects/finalAI/PROJECT.yaml`

Declared type:

- `closed-loop-unified-ai-runtime`

Declared zones:

- Backend: `/Users/cuongnguyen/Workspace/Projects/finalAI/backend`
- Production: `/Users/cuongnguyen/Workspace/Projects/finalAI/production`
- Data: `/Users/cuongnguyen/Workspace/Projects/finalAI/data`
- Docs: `/Users/cuongnguyen/Workspace/Projects/finalAI/docs`

Declared runtime:

- Language: Python
- Entrypoint: `backend/app/runtime/main.py`
- Module: `runtime.main`
- Python path: `backend/app`
- Long-lived runtime: `true`

Declared workers:

- `runtime.redis_client`
- `runtime.data_fetcher`
- `comms.telegram_bot`

Declared services:

- `redis` on `6379`
- `postgres` on `5432`
- `lakedata_api` on `5051`
- `api_gateway` on `5050`
- `finalai_runtime`
- `ollama` on `11434`
- `langchain_api` on `5053`
- `chat_api` on `5052`
- `frontend` on `8080`
- `finalai_unified` profile on `6050`, `6051`, `6052`, `6053`, `6080`

### Runtime source layout

Observed directories under `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/app`:

- `comms`
- `engine`
- `runtime`
- `services`
- `thinker`
- `utils`

Observed backend Python file count:

- `46` Python files under `backend/app`

Declared module groups in `PROJECT.yaml`:

- `comms`: `ai_assistance`, `telegram_bot`
- `engine`: `deployer`, `executor`, `generator`, `langchain_client`, `ollama_client`, `reviewer`
- `runtime`: `data_fetcher`, `deep_observability`, `deployment_tracker`, `dev_trigger`, `main`, `mission_telemetry`, `orchestrator`, `redis_client`, `semantic_telemetry`, `system_analyzer`, `unified_runtime`
- `services`: `api_gateway`, `chat_api`, `langchain_api`, `lakedata_api`
- `thinker`: `evaluator`, `self_assessment`, `self_improver`

### Project skills

Skill root:

- `/Users/cuongnguyen/Workspace/Projects/finalAI/.github/skills`

Observed project skills:

- `/Users/cuongnguyen/Workspace/Projects/finalAI/.github/skills/finalai-module-apis/SKILL.md`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/.github/skills/finalai-orchestration-governance/SKILL.md`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/.github/skills/finalai-pipeline-checklist/SKILL.md`

### Runtime artifacts and telemetry

Observed processed data:

- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/execution_traces.jsonl`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/mission_telemetry.jsonl`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/event_log.jsonl`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/deployment_log.jsonl`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/workspace_physical_map.json`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/workspace_physical_classification.json`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/workspace_physical_tree_full.txt`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/workspace_physical_paths_full.txt`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/data/processed_data/python_data`

Approximate observed sizes from `ls -la`:

- `execution_traces.jsonl`: about 4.7 MB
- `mission_telemetry.jsonl`: about 268 KB
- `event_log.jsonl`: about 98 KB
- `deployment_log.jsonl`: about 75 KB

### Compose/runtime profiles

Observed compose files include:

- `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/compose.yaml`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/compose.single-container.yaml`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/compose.prod.yaml`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/compose.prod.optimized.yaml`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/compose.prod.secrets.yaml`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/backend/compose.prod.unlimited.yaml`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/production/compose.yaml`

Additional Docker-related source trees:

- `/Users/cuongnguyen/Workspace/Projects/finalAI/docker-local`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/docker-desktop-fork`
- `/Users/cuongnguyen/Workspace/Projects/finalAI/gordon-ui-unlimited`

## Codex / Plugin Store Evidence

### Codex marketplace source

- Marketplace clone: `/Users/cuongnguyen/.codex/.tmp/plugins`
- Remote: `https://github.com/openai/plugins.git`
- Current local plugin patch commit: `d24c889 Add Binance public market data MCP tools`
- Marketplace manifest: `/Users/cuongnguyen/.codex/.tmp/plugins/.agents/plugins/marketplace.json`

Observed marketplace scale:

- `172` plugins in `.codex/.tmp/plugins/plugins`
- `147` plugins with `.app.json`
- `64` plugins with skills
- `550` `SKILL.md` files in marketplace source
- `4` plugins with local `.mcp.json` before/including Binance patch

Category distribution:

- Productivity: `42`
- Developer Tools: `40`
- Finance: `26`
- Business & Operations: `15`
- Data & Analytics: `13`
- Communication: `12`
- Education & Research: `10`
- Creativity: `9`
- Other / Travel / Security: remaining categories

### Codex local skills

- `/Users/cuongnguyen/.codex/skills`: `44` standalone skills
- `/Users/cuongnguyen/.codex/vendor_imports/skills`: `39` vendor/imported skills

### App directory and tool cache

Observed in Codex cache:

- App directory cache connectors: `1473`
- Enabled connectors in cache: `1473`
- Accessible connectors in that cache snapshot: `0`
- Codex app tools cache: `360` callable tools

### Binance plugin patch

Source plugin:

- `/Users/cuongnguyen/.codex/.tmp/plugins/plugins/binance`

Materialized cache plugin:

- `/Users/cuongnguyen/.codex/plugins/cache/openai-curated/binance/cd0fccd4`

Added local MCP tools:

- `get_ticker_price`
- `get_24hr_ticker`
- `get_order_book`
- `get_klines`
- `get_exchange_info`

Validation performed:

- `validate_plugin.py` passed on source plugin.
- `validate_plugin.py` passed on materialized cache plugin.
- Direct MCP JSON-RPC `initialize` passed.
- Direct MCP JSON-RPC `tools/list` passed.
- Direct MCP calls to Binance public API for ticker/order book/klines/exchange info passed.

Known ingestion caveat:

- Current `tool_search` session did not discover the new Binance MCP tools after patching, likely because tool registry was loaded before plugin modification. The plugin files and direct MCP behavior are valid, but Codex may need a reload/restart to ingest the new server into the active session.

## Cross-Agent Skill Surface

Observed skill/plugin roots beyond Codex:

- `/Users/cuongnguyen/.agents/plugins`
- `/Users/cuongnguyen/.agents/skills`
- `/Users/cuongnguyen/.claude/plugins`
- `/Users/cuongnguyen/.claude/skills`
- `/Users/cuongnguyen/.copilot/skills`
- `/Users/cuongnguyen/.gemini/antigravity/skills`
- `/Users/cuongnguyen/.github/skills`
- `/Users/cuongnguyen/zed/.agents/skills`
- `/Users/cuongnguyen/Desktop/.sixth/skills`

Interpretation from evidence:

- The ecosystem is not Codex-only.
- The skill/plugin substrate appears designed to span multiple agent hosts and IDE/runtime contexts.

## Evidence-Based Architecture Reading

The current system is best described as a multi-layer software factory ecosystem:

1. **Runtime Layer**
   - finalAI runtime with Python services, workers, orchestration, telemetry, and Docker compose profiles.

2. **Factory / Development Layer**
   - `.factory`, Zed factory state, project skills, GitHub instructions, pipeline checklist, module APIs, and runtime governance skills.

3. **Data / Telemetry Layer**
   - execution traces, mission telemetry, event logs, deployment logs, workspace physical maps, and runtime store logs.

4. **Distribution Layer**
   - Codex plugin marketplace source, plugin cache, app connector directory, local MCP servers, skills, and app manifests.

5. **Cross-Agent Layer**
   - Codex, GitHub/Copilot, Claude, Gemini/Antigravity, Zed, and other skill/plugin directories.

6. **Commercialization / Store Layer**
   - Marketplace-ready plugin structure exists, but maturity varies by plugin. Many are connector shells; fewer have callable MCP/local tools.

## Corrected Earlier Mistakes

Earlier statement to correct:

- `FILESYSTEM_GRAPH.json` said active finalAI tree had no Git baseline.

Current direct check:

- `/Users/cuongnguyen/Workspace/Projects/finalAI` is a symlink to `/Users/cuongnguyen/.workspace_payload_store/Projects/finalAI`.
- That target has a Git repository.
- Therefore the older graph has at least one stale fact and must be treated as a historical snapshot, not current truth.

Earlier behavior to correct:

- I treated plugin work as a standalone local project before fully checking `.codex`.
- Correct rule going forward: plugin/store work should begin from `/Users/cuongnguyen/.codex/.tmp/plugins` and the materialized cache under `/Users/cuongnguyen/.codex/plugins/cache`.

## Open Checks Not Yet Performed

These require a deliberate runtime audit pass:

- Docker live state: `docker ps`, compose services, health endpoints, container logs.
- Redis/Postgres actual availability and data continuity.
- Current finalAI runtime logs versus declared runtime topology.
- Whether `execution_traces.jsonl` contains recent divergent execution graphs.
- Whether plugin cache regeneration overwrites manual cache edits.
- Whether Codex reload ingests the newly added Binance MCP tools.
- Whether `.secrets` files are tracked, ignored, or leaked. I verified existence only and did not read secret contents.

## Next Concrete Step

Recommended next audit artifact:

- `FINALAI_RUNTIME_LIVE_AUDIT_2026-06-09.md`

Scope:

- Docker service state
- health endpoints
- Redis/Postgres reachability
- latest logs
- latest execution trace shape
- mapping from declared `PROJECT.yaml` services to running reality

