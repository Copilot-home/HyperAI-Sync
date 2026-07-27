# AIOS AIServer Runtime Trace

Date: 2026-04-16

## Scope

Read-only trace of the local `AI Server` application currently active on the root host.

## Runtime Identity

Observed app package:

```text
Name = LocalAIs.com.AIServer
DisplayName = AI Server
PackageFullName = LocalAIs.com.AIServer_2.0.1.0_x64__q6fhkaxfet316
Version = 2.0.1.0
PublisherDisplayName = Software Tailor (HK) Limited
InstallLocation = C:\Program Files\WindowsApps\LocalAIs.com.AIServer_2.0.1.0_x64__q6fhkaxfet316
```

The app is a Windows full-trust packaged app using Windows App Runtime and WinUI/.NET runtime components.

## Active Processes

Observed live lanes:

```text
AIServer.exe serve
path = C:\Users\pc\AppData\Local\Packages\LocalAIs.com.AIServer_q6fhkaxfet316\LocalState\AIServer\2.0.1.0\AIServer.exe
port = 11434
role = Ollama-compatible local AI server
```

```text
AIServer.exe runner (transient / model-load scoped)
model = C:\Users\pc\.ollama\models\blobs\sha256-29d8c98fa6b098e200069bfb88b9508dc3e85586d20cba59f8dda9a808165104
ctx-size = 4096
batch-size = 512
n-gpu-layers = 29
threads = 8
flash-attn = enabled
parallel = 1
observed port = 51852
role = internal llama runner
```

Ollama desktop also has an `ollama.exe serve` process on `11434`. Both are part of the local model substrate and must be treated as overlapping provider infrastructure, not as separate shell authority.

## Installed Runtime Structure

AIServer has two relevant physical strata:

```text
package app root:
C:\Program Files\WindowsApps\LocalAIs.com.AIServer_2.0.1.0_x64__q6fhkaxfet316

mutable runtime state:
C:\Users\pc\AppData\Local\Packages\LocalAIs.com.AIServer_q6fhkaxfet316\LocalState
```

The packaged app root contains:

- `AIServer.dll`
- `AIServer.exe`
- `AIServer.deps.json`
- `AIServer.runtimeconfig.json`
- `Server\AIServer.exe`
- `Server\lib\ollama\*.dll`

The local server bundle includes CUDA/llama.cpp/Ollama runtime libraries such as:

- `cublas64_12.dll`
- `cublasLt64_12.dll`
- `ggml-cuda.dll`
- `ggml-cpu-*.dll`

## Dependency Signal

`AIServer.deps.json` shows:

- `.NETCoreApp,Version=v8.0/win-x64`
- `OllamaSharp/5.2.3`
- `Microsoft.Extensions.AI.Abstractions/9.5.0`
- `Microsoft.EntityFrameworkCore/9.0.6`
- `Microsoft.EntityFrameworkCore.Sqlite/9.0.6`
- `Microsoft.Data.Sqlite.Core/9.0.6`
- WinUI and CommunityToolkit dependencies

Interpretation: AIServer is not just a UI wrapper. It is a local model server/control app with .NET AI abstractions, Ollama client integration, SQLite-backed state, and bundled Ollama-compatible runner infrastructure.

## API Proof

Observed API endpoints:

```text
GET http://127.0.0.1:11434/
-> 200 "Ollama is running"

GET http://127.0.0.1:11434/api/tags
-> 200 model list

GET http://127.0.0.1:11434/v1/models
-> 200 OpenAI-compatible model list

GET http://127.0.0.1:51852/health
-> 200 {"status":0,"progress":1}
```

`51852` is not a durable listener. It was observed during active runner execution and later closed. Treat it as transient runner proof, not a stable API endpoint.

Chat probes:

```text
POST http://127.0.0.1:11434/api/chat
model = deepseek-r1:1.5b
result = done=true
```

```text
POST http://127.0.0.1:11434/v1/chat/completions
model = qwen2.5-coder:1.5b
result = object=chat.completion
```

Model behavior should not be treated as deterministic authority. The API route is proven; exact-output compliance is model-dependent.

## Runtime Logs

Recent AIServer log evidence shows:

- model family: `DeepSeek R1 Distill Qwen 1.5B`
- file format: `GGUF V3`
- quantization: `Q4_K - Medium`
- architecture: `qwen2`
- runtime context: `n_ctx = 4096`
- GPU offload: `29/29 layers`
- CUDA model buffer around `934.70 MiB`
- warning: prompt truncation occurred when prompt length was around `7000` and runtime limit was `4096`

Operational implication: AIServer is GPU-backed and live-capable, but large prompt workflows need context budgeting or upstream summarization.

## Relationship To HyperAI

Current binding:

```text
AIServer/Ollama 11434
-> local model substrate
-> QuantumReason llm_orchestrator.py local provider
-> QuantumReason fakeOpenAPI 8000
-> app/runtime OpenAI-compatible clients
```

Relevant source-controlled bridge:

```text
C:\Users\pc\aidev\quantumreason_v3\llm_orchestrator.py
LOCAL_LLM_URL default = http://localhost:11434/api/generate
local model preference = qwen2.5-coder:1.5b, codellama:latest, mistral-core:latest, mistral:latest
```

The AIServer app itself is packaged binary/runtime substrate. The controllable source-level integration is currently the QuantumReason provider fabric in `aidev`.

## Classification

```text
runtime_class = local_model_substrate
lane_class = provider_fabric
status = live_capable + partially_proven
authority = 0 by itself
promotion_requirement = proof + phi_i(M) mapping + open gate
```

Allowed roles:

- local model serving
- OpenAI-compatible model listing
- Ollama-compatible generation/chat
- provider substrate behind QuantumReason fakeOpenAPI
- runtime evidence source

Forbidden roles:

- shell authority
- app backend authority
- memory authority
- cloud authority
- automatic quota fallback authority
- deterministic business/proof authority by model output alone

## Risks

- Port ownership overlap on `11434` between Ollama desktop and AIServer can confuse attribution unless process ownership is checked.
- Runner ports such as `51852` are transient and should not be treated as stable integration endpoints.
- Runner context is `4096`, while some prompts are larger and get truncated.
- Model output can drift from exact instruction even when the API route is healthy.
- AIServer source is packaged binary, so durable integration should happen through local API contract and QuantumReason source, not by mutating packaged app files.

## Next Safe Action

Add AIServer explicitly to the model/provider registry as a local substrate behind the QuantumReason fakeOpenAPI route. Avoid restarting or reconfiguring the packaged app unless a separate mission and rollback plan exists.
