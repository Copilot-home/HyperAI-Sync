# Workspace Runtime Topology

Invariant:

```text
Runtime concept <-> canonical physical location
Operational artifact <-> canonical physical file
One concept <-> one owner <-> one lifecycle
```

## Control Plane

Canonical location: `/Users/cuongnguyen/Workspace`

Purpose:

- Intent, config, manifests, entrypoints, and stable symlinks.
- No deep vendor/runtime payloads.
- Maximum workspace entry depth: 3.

## Payload Plane

Canonical entrypoint: `/Users/cuongnguyen/Workspace/payload`

Physical store: `/Users/cuongnguyen/.workspace_payload_store/payload`

Layout:

- `payload/projects`: active project payloads.
- `payload/worktrees`: alternate worktrees and agent branches.
- `payload/archives`: historical imports and backups.
- `payload/generated`: generated modules and generated outputs.
- `payload/datasets`: static or imported datasets.
- `payload/vendor`: vendored dependencies and node_modules-style payloads.
- `payload/forks`: forked upstream source trees.
- `payload/deployments`: deployment payloads.
- `payload/exports`: exported reports or bundles.
- `payload/manifests`: payload-plane manifests.

## Runtime Plane

Canonical entrypoint: `/Users/cuongnguyen/Workspace/runtime`

Physical store: `/Users/cuongnguyen/.finalai_runtime_store/runtime`

Layout:

- `runtime/state`: mutable runtime state.
- `runtime/memory`: memory stores and durable recall surfaces.
- `runtime/telemetry`: mission telemetry and event logs.
- `runtime/traces`: execution traces.
- `runtime/evidence`: evidence artifacts and filesystem maps.
- `runtime/cache`: runtime caches.
- `runtime/venvs`: Python virtual environments.
- `runtime/logs`: runtime logs.
- `runtime/generated`: runtime-generated modules.
- `runtime/manifests`: runtime-plane manifests.

## Locate Rules

- EvidenceGate or semantic-closure issue: open `runtime/evidence`.
- Trace issue: open `runtime/traces`.
- Mission/event telemetry issue: open `runtime/telemetry`.
- Memory/state issue: open `runtime/memory` or `runtime/state`.
- Generated module mismatch: open `payload/generated` first, then `runtime/generated`.
- Vendor/fork issue: open `payload/vendor` or `payload/forks`.
- Historical/backup issue: open `payload/archives`.

Do not use broad search as the first move when the runtime concept is known.
