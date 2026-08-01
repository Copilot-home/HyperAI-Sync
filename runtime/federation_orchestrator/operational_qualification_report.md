# Operational Qualification Report

audited_at: 2026-07-31T10:41:01.870901+00:00

## 1. Runtime discovery

Observed AIOS-relevant processes: **98**
Total network connections observed: **235**

### Observed by command (selected)

| pid | command | listening_ports | role |
|-----|---------|-----------------|------|
| 323 |  |  | UNKNOWN |
| 526 | /System/Library/CoreServices/ControlCenter.app/Contents/MacO | 7000,7000,5000,5000 | UNKNOWN |
| 787 | /opt/homebrew/opt/redis/bin/redis-server 127.0.0.1:6379  | 6379,6379 | MEMORY |
| 796 | Contents/Frameworks/Squirrel.framework/Versions/A/Squirrel b |  | PROVIDER |
| 809 | /Applications/Xcode.app/Contents/Developer/Library/Framework | 50520 | PROVIDER |
| 831 | /Applications/Ollama.app/Contents/MacOS/Ollama hidden | 49196 | PROVIDER |
| 864 | /Applications/Ollama.app/Contents/Resources/ollama serve | 11434 | PROVIDER |
| 2540 | zsh (kiro-cli-term) |  | MEMORY |
| 2617 | /bin/zsh |  | UNKNOWN |
| 2700 | node /Users/andy/.antigravity-ide/extensions/googlecloudtool |  | UNKNOWN |
| 2707 | node /Users/andy/.antigravity-ide/extensions/googlecloudtool |  | UNKNOWN |
| 2708 | node /Users/andy/.antigravity-ide/extensions/googlecloudtool |  | UNKNOWN |
| 2779 | /Applications/Antigravity IDE.app/Contents/Frameworks/Antigr |  | UNKNOWN |
| 3557 | /Applications/Antigravity IDE.app/Contents/Frameworks/Antigr |  | UNKNOWN |
| 3612 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 51499 | UNKNOWN |
| 3852 | /Users/andy/.lmstudio/.internal/utils/node -e 
function conn |  | PROVIDER |
| 4812 | /Applications/Xcode.app/Contents/Developer/Library/Framework |  | UNKNOWN |
| 4813 | /Applications/Xcode.app/Contents/Developer/Library/Framework |  | UNKNOWN |
| 8954 | /Users/andy/.lmstudio/extensions/frameworks/lmlink-connector | 50588 | PROVIDER |
| 9100 | /System/Library/PrivateFrameworks/IntelligenceFlowContextRun |  | UNKNOWN |
| 9153 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr |  | UNKNOWN |
| 10069 | npm exec @playwright/mcp@latest    |  | UNKNOWN |
| 10079 | npm exec @upstash/context7-mcp@1.0.31    |  | UNKNOWN |
| 10177 | node /Users/andy/.npm/_npx/9833c18b2d85bc59/node_modules/.bi |  | UNKNOWN |
| 10195 | node /Users/andy/.npm/_npx/15b07286cbcc3329/node_modules/.bi |  | UNKNOWN |
| 10207 | node /Users/andy/.npm/_npx/295df104acba4005/node_modules/.bi |  | UNKNOWN |
| 10344 | bash -c kill 74521; sleep 2; cd /Users/andy/HyperAI-Sync &&  |  | BROKER |
| 10357 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 8765 | BROKER |
| 10407 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr |  | UNKNOWN |
| 11490 | bash -c cd /Users/andy/openapi-servers/servers/quotes-ui &&  |  | TOOL |
| 11491 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 8906 | TOOL |
| 11511 | bash -c cd /Users/andy/openapi-servers/servers/flashcards && |  | TOOL |
| 11512 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 8907 | TOOL |
| 11536 | bash -c cd /Users/andy/openapi-servers/servers/time-ui && no |  | TOOL |
| 11537 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 8908 | TOOL |
| 11978 | bash -c cd /Users/andy/openapi-servers && MODEL_URL=http://1 |  | TOOL |
| 11979 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 8909 | TOOL |
| 12223 | bash -c cd /Users/andy/openapi-servers/servers/bitcoin-price |  | TOOL |
| 12224 | /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.fr | 8910 | TOOL |
| 15562 | bash -c pkill -f "uvicorn main:app --host 127.0.0.1 --port 8 |  | TOOL |

## 2. Role registry

Total surfaces: **75**
Observed runtime: **69**
Role resolved: **29**

## 3. Authority matrix

Authority resolved: **29 / 75**

## 4. Auth topology

- PRESENT: 8
- MISSING: 6
- PRESENT_UNKNOWN: 1

## 5. Dependency graph

Nodes: **75**, Edges: **202**

## 6. Binding plan

Operationally qualified: **27 / 35**

### Not qualified (selected)

| id | role | missing | compute_claim |
|-----|------|---------|---------------|
| apo_upstream_titan_ollama | PROVIDER | observed_runtime, role_resolved, authority_resolved, depende | manual_or_recycle |
| apo_upstream_macmini_ollama | PROVIDER | observed_runtime, role_resolved, authority_resolved, depende | manual_or_recycle |
| openapi_tool_slack | TOOL | auth:SLACK_BOT_TOKEN, auth:SLACK_TEAM_ID | process_group |
| openapi_tool_google_pse | TOOL | auth:GOOGLE_PSE_CX | process_group |
| mcp_docker_mcp | MCP | observed_runtime, role_resolved, authority_resolved, depende | manual_or_recycle |
| hyperai_product_runtime | PRODUCT | observed_runtime, role_resolved, authority_resolved, depende | manual_or_recycle |
| federation_orchestrator | ORCHESTRATOR | observed_runtime, role_resolved, authority_resolved, depende | manual_or_recycle |
| memory_writer | MEMORY | observed_runtime, role_resolved, authority_resolved, depende | manual_or_recycle |

## 7. Invariants preserved

- READONLY_DISCOVERY = 1
- UNBOUNDED_DISCOVERY = 0
- AUTO_BINDING = 0
- AUTO_EXECUTION = 0
- AUTO_MUTATION = 0
- No plaintext secrets logged
- mcp_docker_mcp:8811 not started
- Gate 2 not opened

## 8. Gaps requiring explicit gate

- **apo_upstream_titan_ollama**: ['observed_runtime', 'role_resolved', 'authority_resolved', 'dependencies_resolved', 'health_probed']
- **apo_upstream_macmini_ollama**: ['observed_runtime', 'role_resolved', 'authority_resolved', 'dependencies_resolved', 'health_probed']
- **openapi_tool_slack**: ['auth:SLACK_BOT_TOKEN', 'auth:SLACK_TEAM_ID']
- **openapi_tool_google_pse**: ['auth:GOOGLE_PSE_CX']
- **mcp_docker_mcp**: ['observed_runtime', 'role_resolved', 'authority_resolved', 'dependencies_resolved', 'health_probed']
- **hyperai_product_runtime**: ['observed_runtime', 'role_resolved', 'authority_resolved', 'dependencies_resolved', 'health_probed']
- **federation_orchestrator**: ['observed_runtime', 'role_resolved', 'authority_resolved', 'dependencies_resolved', 'health_probed']
- **memory_writer**: ['observed_runtime', 'role_resolved', 'authority_resolved', 'dependencies_resolved', 'health_probed']