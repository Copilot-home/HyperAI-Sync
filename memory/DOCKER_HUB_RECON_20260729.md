# Docker Hub / Docker Enterprise Recon — 2026-07-29

## Goal
Prepare for Docker Hub organization / image publishing actions by confirming what already exists.

## Findings

### 1. Docker Desktop is logged in
- `~/.docker/config.json` contains `https://index.docker.io/v1/` auth with `credsStore: "desktop"`.
- Docker Desktop is active (`desktop-linux` context).

### 2. Docker Hub account
- Username: `sowhat1989` (from Docker Desktop keychain credentials, used for `index.docker.io/v1/`).
- Public profile exists on Docker Hub.

### 3. Existing public repositories under `sowhat1989`
```
sowhat1989/ai_coding
sowhat1989/default
sowhat1989/dev_workflow
sowhat1989/terminal_control
```
- All 4 are published **MCP profiles** (`media_types: application/vnd.docker.mcp.profile.v1+json`).
- These match the local `docker mcp profile list` output: `ai_coding`, `dev_workflow`, `terminal_control`.
- `sowhat1989/default` likely corresponds to the local `profile` profile.

### 4. Existing Docker organization
```
GET https://hub.docker.com/v2/orgs/nguyencuong1989
{
  "id": "5a8eb098ba404909b4ddc55a41f5a5a9",
  "orgname": "nguyencuong1989",
  "full_name": "nguyen duc cuong",
  "company": "Lineage_AI",
  "type": "Organization",
  "date_joined": "2025-11-30T16:53:20.835857Z",
  "is_active": true
}
```
- Organization `nguyencuong1989` already exists and is active.
- It currently has **0 public repositories**.

### 5. Available on Docker Hub
- Official `ollama/ollama` image exists on Docker Hub, multi-arch.
- It is **not present locally** (no cached image, no container).

### 6. Enterprise category reference
Docker Hub image categories for enterprise include:
- API management
- Content management system
- Data science
- Developer tools
- Databases & storage
- Languages & frameworks
- Integration & delivery
- Internet of things
- Machine learning & AI
- Message queues
- Monitoring & Observability
- Networking
- Operating systems
- Security

## Open decisions
1. Should a new image be published under the existing org `nguyencuong1989` or the personal namespace `sowhat1989`?
2. What is the desired repository name? (e.g., `hyperai-ollama`, `apo-ollama`, `ollama-brain`)
3. Which Docker Hub category should the image be tagged with? (`Machine learning & AI` is the most natural for Ollama.)
4. Should the existing MCP profile repos remain under `sowhat1989` or be moved to the org?
5. A Docker Hub PAT is present in the macOS keychain; it can be used for publishing if needed.

## No suitable skill found
- Searched local skills and `npx skills find docker`. Found build/compose skills (`multi-stage-dockerfile`, `docker-patterns`, `docker-compose-orchestration`) but no Docker Hub organization/repository management skill.
