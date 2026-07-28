# Physical Directory Map

Verified: 2026-05-25, Asia/Ho_Chi_Minh

## Home Root

```text
/Users/cuongnguyen/
|-- Desktop/                  macOS standard; currently contains screenshots
|-- Documents/                macOS standard
|   `-- Dadroit JSON Generator/
|       `-- sample.json
|-- Downloads/                macOS standard; currently contains Windsurf installer
|-- Library/                  macOS application and system data; keep in place
|-- Movies/                   macOS standard; contains media/application libraries
|-- Music/                    macOS standard; contains Music library
|-- Pictures/                 macOS standard; contains Photos/Photo Booth libraries
|-- Public/                   macOS standard
|-- Workspace/                managed development workspace
|-- .codex/                   live Codex config and installed skills
|-- .docker/                  live Docker config
|-- .vscode/                  live VS Code extensions/config
|-- .cache/, .cargo/, .npm/   runtime/tool caches
`-- other hidden app dirs      created by installed developer applications
```

`Desktop`, `Documents`, `Downloads`, `Library`, `Movies`, `Music`, `Pictures`, and
`Public` are normal physical directories created/used by macOS. They are not
extra FinalAI project roots and must not be deleted as workspace cleanup.

## Workspace Root

```text
/Users/cuongnguyen/Workspace/
|-- Projects/
|   `-- finalAI/              only active project
|       |-- devzone/
|       |   `-- backend/      active backend source/config
|       `-- production/
|           `-- backend -> ../devzone/backend
|-- System/
|   |-- Codex/                map to live Codex configuration
|   |-- Docker/               map to live Docker configuration
|   |-- Runtime/              managed virtual environments and model caches
|   |-- Shell/                shell setup documentation
|   `-- VSCode/               map to live VS Code configuration
`-- Archive/
    |-- 2026-05-24/           earlier imports and the old AIDEV project
    `-- 2026-05-25/
        |-- generated-project-metadata/
        `-- imported-projects/
            `-- welcome-to-docker/
```

## Active Project

```text
/Users/cuongnguyen/Workspace/Projects/finalAI/
|-- PROJECT.yaml
|-- README.md
|-- SYSTEM.md
|-- RUNBOOK.md
|-- HEALTH.md
|-- Makefile
|-- devzone/
|   `-- backend/
|       |-- .env              local secrets only; ignored
|       |-- .env.example      placeholders only
|       |-- Dockerfile
|       |-- compose.yaml
|       |-- compose.debug.yaml
|       |-- requirements.txt
|       `-- ai_saas_system/
|           |-- configs/
|           |   `-- aidev_settings.json
|           |-- docs/
|           |   `-- SMARTAQUA_SYSTEM.md
|           |-- scripts/
|           |   |-- start.sh
|           |   |-- start_api_gateway.sh
|           |   `-- start_lakedata_api.sh
|           |-- utils/
|           `-- core/finalAI/
|               |-- comms/       Telegram bot
|               |-- modules/
|               |   |-- tech/     code/debug/deploy functionality
|               |   `-- business/ AIDEV expert programming functionality
|               |-- runtime/     config, Redis, analysis, data collection
|               |-- services/    API gateway and LakeData API
|               `-- thinker/     evaluation and improvement functionality
`-- production/
    |-- backend -> ../devzone/backend
    `-- compose.yaml
```

## Cleanup Decisions

- Removed generated `.DS_Store`, `__pycache__`, transient FinalAI log, and empty
  source folders from active project paths.
- Removed empty `Documents/Codex` and `Documents/NI-Python-DataPlugins`.
- Archived the non-active Docker sample repository under `Workspace/Archive`.
- Archived extension-generated metadata that had been created at
  `Workspace/Projects` instead of inside an intentional project.
- Scrubbed exposed API/token values from templates and archived environment
  examples. The configured Telegram token remains only in the local `.env`.
