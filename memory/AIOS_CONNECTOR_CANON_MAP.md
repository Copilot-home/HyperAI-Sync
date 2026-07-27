# AIOS Connector Canon Map

Date: 2026-04-18

## Purpose

This artifact normalizes the CLI-native and runtime-native ecosystem into connector roles instead of treating the environment as a tool list or process list.

## Canonical Connector Reading

The ecosystem should be read through connector roles such as:

- `conductor`
- `mcp_hub`
- `github`
- `llm_engine`
- `runtime_observer`
- `tech_debt_auditor`
- `telegram`
- `web_agent`

## Current Artifacts

Machine-readable connector map:

- `runtime/federation_orchestrator/connector_canon_map.json`

Machine-readable CLI registry:

- `runtime/federation_orchestrator/cli_capability_registry.json`

## Dashboard Rule

System inventory should summarize meaningful groups and connector roles.

Do not use raw subprocess counts as the main system truth.
