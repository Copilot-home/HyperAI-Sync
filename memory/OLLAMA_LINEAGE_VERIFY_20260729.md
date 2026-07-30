# Ollama Lineage Live Verification — 2026-07-29

## Executive
- Native Ollama.app on MacBook is the **only local Ollama authority** live on this machine.
- Docker-based Ollama descendants (`ollama-brain`, `FinalAI`, `prod`, generic `ollama` volume) are **NOT currently present** in Docker Desktop on this Mac.
- `ollama/ollama` image exists on Docker Hub but has **not been pulled/cached** locally.
- Remote Titan Ollama (`192.168.3.84:11434`) is live. macmini Ollama (`192.168.3.28:11434`) is unreachable.
- Docker MCP Gateway profiles (`terminal_control`, `lineageai`) are configured but do **not** reference Ollama. `claude-memory` volume is present and bound to the `lineageai` memory server.

## Evidence

### 1. Native Ollama (MacBook)
```
PID 13894: ollama serve
Port 11434: LISTEN *:11434
~/.ollama: exists with config.json, models
Ollama.app: /Applications/Ollama.app (Contents/ installed)
Version: 0.30.10
Models: smollm2, siri, chatgpt, qwen2.5:1.5b, deepseek-v4-flash:cloud, etc.
```

### 2. Docker Ollama descendants — NOT PRESENT
```
docker ps -a           : no ollama-brain, backend-ollama-1, ollama-brain-prod
docker images -a       : no ollama/ollama, no *ollama* image
docker volume ls       : no andy_ollama_models, ollama_models, ollama_models_prod,
                         backend_finalai_ollama_data, ollama, crow_ollama_data
docker network ls      : no andy_hyperai-network
docker builder du      : no ollama build-cache entries
Port 11435             : not listening
```

### 3. Docker Hub / manifest
```
docker search ollama           : ollama/ollama exists (1596 stars)
docker manifest inspect        : ollama/ollama:latest exists, multi-arch (amd64, arm64)
Verdict: image is available on Docker Hub, but not in local store.
```

### 4. APΩ routing (from /Users/andy/.apo/gateway/apo_config.yaml)
```
macbook_ollama  -> 127.0.0.1:11434/v1   (native Ollama.app)  LIVE
titan_ollama    -> 192.168.3.84:11434/v1                    LIVE (version 0.32.4)
macmini_ollama  -> 192.168.3.28:11434/v1                    UNREACHABLE (ping OK, port 11434 refused)
lmstudio/Bionic -> 127.0.0.1:1234/v1                        LIVE (token required)
```

### 5. Bionic / LM Studio
```
/Applications/Bionic.app running, PID 41654
Port 1234 LISTEN
Separate model store: ~/.lmstudio
Runtime: LLMWorker / MLX / llama.cpp / Metal backend (lmlink-connector)
Not an Ollama runtime.
```

### 6. Docker MCP Gateway profiles
```
$ docker mcp profile list
- ai_coding
- terminal_control
- dev_workflow
- super
- profile
- codex_unified
- lineageai

terminal_control: mcp/desktop-commander, mcp/filesystem, mcp/sequentialthinking
lineageai:        mcp/memory (claude-memory:/app/dist), mcp/sonarqube, mcp/playwright, mcp/fetch

No profile contains ollama, 11434, or 11435.
Volume claude-memory exists (16.67kB) and is bound to the memory server in lineageai.
```

## Reconciliation with user canon

| Canon item | Verdict |
|------------|---------|
| Official primitive `ollama/ollama` | ✅ Confirmed on Docker Hub, not locally cached |
| Mac native descendant | ✅ LIVE (port 11434, `~/.ollama`, Metal) |
| HyperAI Docker `ollama-brain` / `andy_ollama_models` / `andy_hyperai-network` | ❌ NOT_CURRENTLY_PRESENT |
| `11435` host projection | ❌ Not in use |
| FinalAI `backend-ollama-1` / `backend_finalai_ollama_data` | ❌ NOT_CURRENTLY_PRESENT |
| Prod `ollama-brain-prod` / `ollama_models_prod` | ❌ NOT_CURRENTLY_PRESENT |
| Titan Nvidia path | ✅ LIVE as remote Ollama endpoint (version 0.32.4) |
| macmini Ollama | ⚠️ PING OK, port 11434 unreachable |
| Bionic / LM Studio separate runtime | ✅ Confirmed (port 1234) |

## Open questions
1. Should the Docker Ollama descendants be restored, or are they intentionally retired?
2. Is `192.168.3.28` expected to run Ollama, or should `macmini_ollama` upstream be removed from `apo_config.yaml`?
3. Does Titan use Docker Ollama or native Ollama? API does not expose this; would require SSH/Docker access to Titan.
