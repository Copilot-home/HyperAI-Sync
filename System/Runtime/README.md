# Runtime Substrate

Live runtime/cache paths:

- Codex runtimes: `/Users/cuongnguyen/.cache/codex-runtimes`
- Hugging Face cache: `/Users/cuongnguyen/.cache/huggingface`
- Cargo cache/tooling: `/Users/cuongnguyen/.cargo`
- Externalized FinalAI runtime store: `/Users/cuongnguyen/.finalai_runtime_store`
- Homebrew prefix on Apple Silicon: `/opt/homebrew`
- Node/npm/npx: `/opt/homebrew/bin/{node,npm,npx}`

Workspace links:

- `/Users/cuongnguyen/Workspace/System/Runtime/live-codex-runtimes`
- `/Users/cuongnguyen/Workspace/System/Runtime/live-huggingface-cache`
- `/Users/cuongnguyen/Workspace/System/Runtime/live-cargo`
- `/Users/cuongnguyen/Workspace/System/Runtime/finalAI-venv`
- `/Users/cuongnguyen/Workspace/System/Runtime/finalAI-data`

Depth discipline:

- `System` is a body-schema map, not a vendor payload store.
- Deep runtime payloads live outside the workspace in `/Users/cuongnguyen/.finalai_runtime_store`.
- Workspace entries under `System/Runtime` must remain depth-3 symlinks or small docs/config files.

These are maps to live paths, not copies.
