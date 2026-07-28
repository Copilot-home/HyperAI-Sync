# System Map

Root path: `/Users/cuongnguyen/Workspace/System`

This directory maps development tools without storing deep vendor/runtime payloads inside the workspace.

## Mapped systems

- Docker: `/Users/cuongnguyen/Workspace/System/Docker`
- Codex: `/Users/cuongnguyen/Workspace/System/Codex`
- VS Code: `/Users/cuongnguyen/Workspace/System/VSCode`
- Runtime caches: `/Users/cuongnguyen/Workspace/System/Runtime`
- Shell: `/Users/cuongnguyen/Workspace/System/Shell`

Live config is linked by symlink. Snapshots are copied files for inspection.

Depth discipline:

- `System` must stay shallow: target maximum physical depth is 3.
- Large/deep runtime payloads are externalized under `/Users/cuongnguyen/.finalai_runtime_store`.
- The workspace keeps stable entry points as symlinks so tools can still use familiar paths.
