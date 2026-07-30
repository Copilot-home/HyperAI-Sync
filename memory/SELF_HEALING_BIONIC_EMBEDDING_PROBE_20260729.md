# SELF-HEALING CYCLE — Bionic Embedding Probe

**Protocol:** AGENT_SELF_HEALING_PROTOCOL v1.0
**CycleID:** SELF-HEAL-BIONIC-EMBED-001
**Timestamp:** 2026-07-29T12:15:00Z
**Mode:** execution_first / evidence_first

---

## EXECUTED STEPS

| Step | Action | Result |
|---|---|---|
| recover_metadata | Reload `project_state.json`, `runtime_execution_todo.md`, `AGENTS.md` (3 locations) | Done |
| recover_workflow | Read current todo list, re-establish mission | Done |
| recover_registry | List skills (`~/.agents/skills`, `~/.config/devin/skills`), MCP servers | Done |
| recover_topology | Probe APΩ `/health` (ok), Bionic `/v1/models` (ok), Docker tool servers (missing) | Recovered by `docker compose up -d --wait` |
| scan_workspace | `ls` `/Users/andy` and `/Users/andy/HyperAI-Sync` | Done |
| discover_skills | `skill search` + directory listing | Done |
| execute_first | `POST 127.0.0.1:1234/v1/embeddings` with `text-embedding-nomic-embed-text-v1.5` | Done |
| collect_evidence | Saved output, exit code, error body | Done |
| update_baseline | Update `project_state.json` and memory | Done |
| respond_last | This report | Done |

---

## EVIDENCE

**Request:**
```bash
curl -sS -w "\nHTTP %{http_code}\n" http://127.0.0.1:1234/v1/embeddings \
  -H "Authorization: Bearer $LMSTUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-nomic-embed-text-v1.5","input":"hello world"}'
```

**Response (HTTP 400):**
```json
{
  "error": "Failed to load model \"text-embedding-nomic-embed-text-v1.5\". Error: Fork path '/Applications/Bionic.app/Contents/Resources/app/.webpack-bionic/lib/embeddingworker.js' does not exist."
}
```

---

## CONCLUSION

- Bionic's `/v1/embeddings` endpoint is **reachable** (HTTP 400, not 404).
- The model `text-embedding-nomic-embed-text-v1.5` is **listed** in `/v1/models`.
- However, Bionic **cannot load** the embedding model because `embeddingworker.js` is missing from the bundle.
- Therefore, **Bionic cannot currently serve embeddings**.
- APΩ cannot use Bionic as an embedding upstream until the missing worker is present.

---

## CANON_DELTA

- **Corrected:** Bionic listing `text-embedding-nomic-embed-text-v1.5` does **not** imply a functional embedding API.
- **Added:** Missing `embeddingworker.js` is a known runtime boundary for this Bionic build.

---

## TOPOLOGY RECOVERY NOTE

During topology recovery, Docker OpenAPI tool servers were found not running. They were restarted with:

```bash
cd /Users/andy/openapi-servers && docker compose up -d --wait
```

All five containers reached Healthy status. APΩ `/health` and `/v1/models` remain functional; tool `/openapi.json` endpoints verified.
