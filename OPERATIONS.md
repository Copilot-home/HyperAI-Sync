# Workspace Operations

Root: `/Users/cuongnguyen/Workspace`

## Read Order

1. `/Users/cuongnguyen/Workspace/STACK.yaml`
2. `/Users/cuongnguyen/Workspace/PROJECTS.md`
3. `/Users/cuongnguyen/Workspace/System/README.md`
4. Project-specific `SYSTEM.md` and `RUNBOOK.md`

## Start finalAI

Set token first:

```sh
cd /Users/cuongnguyen/Workspace/Projects/finalAI/devzone/backend
cp .env.example .env
```

Then edit `.env`, and run:

```sh
cd /Users/cuongnguyen/Workspace/Projects/finalAI
make up
```

Local services:

```sh
cd /Users/cuongnguyen/Workspace/Projects/finalAI
make runtime
make api
make lakedata
```

Production wrapper:

```sh
cd /Users/cuongnguyen/Workspace/Projects/finalAI
make prod-up
```

## System Config

- Docker map: `/Users/cuongnguyen/Workspace/System/Docker`
- Codex map: `/Users/cuongnguyen/Workspace/System/Codex`
- VS Code map: `/Users/cuongnguyen/Workspace/System/VSCode`
- Runtime map: `/Users/cuongnguyen/Workspace/System/Runtime`

## Cleanup Rules

- Keep Desktop, Documents, and Downloads empty for active development.
- Move old or unclear files to `/Users/cuongnguyen/Workspace/Archive/<date>`.
- Keep only `/Users/cuongnguyen/Workspace/Projects/finalAI` as the active project unless a new project is intentionally created.
- Do not store secrets in source files.
- Do not commit `.env`, `venv`, `__pycache__`, logs, or `.DS_Store`.
