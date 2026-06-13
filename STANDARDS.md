# Workspace Standards

## Project Shape

Every active project uses:

```text
PROJECT/
  PROJECT.yaml
  README.md
  SYSTEM.md
  RUNBOOK.md
  Makefile
  devzone/
    README.md
    backend/
  production/
    README.md
    backend -> ../devzone/backend
    compose.yaml
```

## Zone Meaning

- `devzone/backend`: source, Dockerfile, compose for local backend development, VS Code project config.
- `production`: production orchestration, deployment notes, and symlinked backend reference.

## System Mapping

App-owned live config stays where the app expects it:

- Docker: `/Users/cuongnguyen/.docker`
- Codex: `/Users/cuongnguyen/.codex`
- VS Code: `/Users/cuongnguyen/Library/Application Support/Code/User`

`/Users/cuongnguyen/Workspace/System` maps those paths with symlinks and snapshots.

