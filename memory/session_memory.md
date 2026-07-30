# Session Memory

- Last updated: 2026-07-29T13:00:20Z
- Current focus: Ollama lineage live verification
- Latest summary: Probed Ollama lineage across native Mac, Docker, and APΩ routing. Only native Ollama.app (PID 13894, port 11434) and remote Titan (192.168.3.84:11434) are live. Docker descendants (ollama-brain, FinalAI, prod) and HyperAI network/volumes are absent from current Docker state. Port 11435 is not in use. APΩ routes macbook_ollama to 127.0.0.1:11434, titan_ollama to 192.168.3.84:11434, macmini_ollama to 192.168.3.28:11434 (unreachable Ollama), and lmstudio/Bionic to 127.0.0.1:1234.
- Next action: Verify 192.168.3.28:11434 Ollama if macmini is expected live; otherwise update canon to mark macmini_ollama CURRENTLY_UNREACHABLE.
