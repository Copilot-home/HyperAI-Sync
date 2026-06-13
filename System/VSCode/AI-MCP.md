# VS Code AI and MCP

Normalized on: 2026-05-24

## Fixed Issue

Original error:

```text
Server process error: spawn npx ENOENT
```

Cause:

- VS Code extension `MCP ACS Debugger` spawned `npx`.
- Homebrew Node/npm/npx was not installed or not visible to the VS Code GUI environment.

## Node Runtime

Active Node paths:

- Node: `/opt/homebrew/bin/node`
- npm: `/opt/homebrew/bin/npm`
- npx: `/opt/homebrew/bin/npx`

Installed Node:

- Homebrew formula: `node`

## GUI PATH

The macOS GUI session PATH was set with:

```sh
launchctl setenv PATH /opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Restart VS Code after changing this.

## VS Code Settings

User settings:

- Live: `/Users/cuongnguyen/Library/Application Support/Code/User/settings.json`
- Snapshot: `/Users/cuongnguyen/Workspace/System/VSCode/settings.json`

MCP config:

- Live: `/Users/cuongnguyen/Library/Application Support/Code/User/mcp.json`
- Snapshot: `/Users/cuongnguyen/Workspace/System/VSCode/mcp.json`

Key overrides:

```json
{
  "chat.disableAIFeatures": false,
  "mcp-debugger.autoStart": true,
  "mcp.servers.ts-mcp-debugger": {
    "command": "/opt/homebrew/bin/npx",
    "args": ["-y", "@ai-capabilities-suite/mcp-debugger-server"]
  }
}
```

## Verification

```sh
/opt/homebrew/bin/npx -y @ai-capabilities-suite/mcp-debugger-server --help
```

Expected result:

- Prints `MCP ACS Debugger Server`
- No `ENOENT`

