# APΩ Skill → Task Compass for `sigma-apo-nhomes-runtime`

This map matches the project's missing/needed surfaces to the available skills. It is derived from the source and `AGENTS.md` drift analysis.

## Skill usage rule

- `skill invoke <skill-name>` works for skills already in the session's available list.
- `skill list <path>` searches a registry and may miss local skills; for local skill creation/install use `npx skills`.
- When the user provides a skill name/path, execute that skill first (Mandatory Skill-First Rule).

---

## Missing surface → Recommended skill

| Missing surface | Evidence | Recommended skill(s) | Why |
|---|---|---|---|
| **Docker / containerization** | No `Dockerfile`, `compose.yaml`, `.dockerignore` | `azure-prepare` | Generates `Dockerfile`, `azure.yaml`, and Bicep/Terraform for azd deployment. Use only if azd/Azure is the target. |
| **Azure deployment (azd)** | No `azure.yaml`, infra/ | `azure-prepare` → `azure-validate` → `azure-deploy` | Standard azd pipeline: prepare, validate, deploy. |
| **Azure AKS / enterprise infra** | No AKS/cluster config | `azure-kubernetes`, `azure-enterprise-infra-planner` | If the runtime should run on AKS with GPU/service mesh. |
| **Azure VM / compute sizing** | No compute target | `azure-compute`, `azure-quotas` | For raw VM/Container Apps sizing and quota checks. |
| **Frontend (React + Vite)** | `src/ui/` empty; no `vite.config` | `frontend-design`, `vercel-react-best-practices`, `vercel-react-view-transitions`, `vercel-composition-patterns` | Build React/Vite UI, apply design quality, view transitions, composition patterns. |
| **Vercel deploy** | No Vercel config | `deploy-to-vercel`, `vercel-cli-with-tokens`, `vercel-optimize` | If the frontend is targeted at Vercel. |
| **Figma → code** | `AGENTS.md` mentions Figma | `frontend-design` (Figma domain), `mermaid-diagrams` for wireframes | There is no `figma` skill in the current registry; use `frontend-design` for design-to-code and `mcp` Figma server if configured. |
| **Adapter credentials** | Adapters require `NHOMES_*_API_KEY` | `hyperai-credential-broker`, `secrets-management` | Load/rotate credentials through broker; manage env secrets. |
| **Connector control plane** | 12 providers (`pms`, `airbnb`, etc.) need registry | `hyperai-connector-control-plane` | Capability negotiation, connector registry, state machine, evidence receipts for each adapter. |
| **Database / persistence** | In-memory only | `azure-storage` (Blob/Table/Queue), `surrealdb-python`, `surrealql` | Choose based on canon: cloud (Azure) vs local (SurrealDB). |
| **API docs / README** | `README.md` is generic GKE template | `docx`, `doc-coauthoring`, `mermaid-diagrams` | Produce project README, API guide, architecture diagrams. |
| **Testing / UI validation** | `runtime.test.ts` covers backend | `webapp-testing`, `debug-live` | Playwright UI tests and live debugging when frontend exists. |
| **Architecture diagrams** | 12-layer AGENTS, 4 empty dirs | `mermaid-diagrams` | C4/flow/ER diagrams for the NHomes system. |
| **Cost/perf optimization** | No telemetry | `vercel-optimize` (Vercel), `azure-cost` (Azure) | Post-deployment cost and performance analysis. |
| **Socratic verification** | Need evidence-first cycles for new surfaces | `socratic-evidence-reconciliation` (built) | For every new build phase, produce `SOCRATIC_VERIFICATION_CYCLE`. |
| **Repo / issue governance** | Many repos, open issues | `hyperai-repo-governance` | Keep project/related repos clean. |
| **PR / merge hygiene** | Open PRs in ecosystem | `hyperai-pr-triage` | Triage `NguyenCuong1989` / `Copilot-home` PRs. |
| **System scan / cleanup** | Local disk/model caches | `system-scan-ctx-gam`, `system-cleanup-executor` | Periodic disk/runtime hygiene. |

---

## Immediate next actions with skills

1. **If target is Azure + azd:** `azure-prepare` → `azure-validate` → `azure-deploy`.
2. **If target is Vercel frontend:** `frontend-design` → `deploy-to-vercel`.
3. **If target is AKS:** `azure-kubernetes` + `azure-quotas`.
4. **Before any live integration:** `hyperai-credential-broker` + `secrets-management`.
5. **Before declaring 12-layer architecture complete:** `mermaid-diagrams` + `socratic-evidence-reconciliation` cycle per layer.

---

## Skills to avoid for this project

- `lark-*` skills — useful only if the team workflow is on Lark/Feishu, not for runtime build.
- `runcomfy-*` / `ai-image-generation` / `video-*` — creative media, not infrastructure.
- `azure-ai` — only if adding Azure OpenAI/Speech/OCR, not core runtime.
- `mcp-builder` — only if building a new MCP server; current runtime is a REST API.

---

## Correct `skill` tool usage

- `skill invoke <skill-name>` — run a skill by name from the session list.
- `skill list <path>` — requires `path`, but it searches skill registries; it does **not** list local files.
- `npx skills find <query>` — search public skills ecosystem.
- `npx skills add <owner/repo>` or `npx skills add <local-dir>` — install a skill.
- `npx skills init <name>` — scaffold a new skill.
