# AIOS Drift Verification Protocol

Date: 2026-04-18

## Purpose

This protocol binds drift verification into the HyperAI post-turning execution flow.

The system must not rely on doctrine-only confidence when runtime proof is available. Drift verification exists to compare live runtime truth, source truth, registry truth, and proof/artifact truth before authority or execution claims are made.

## Required Truth Layers

Every drift verification pass should compare at least:

1. live runtime truth
2. source truth
3. registry truth
4. proof or artifact truth

## Canonical Drift Classes

### 1. Surface != Mapping

The surface is being interpreted with the wrong role, authority class, or execution placement.

### 2. Artifact != Runtime

Persisted graph, proof, or registry artifacts lag behind live runtime state.

### 3. Route != Policy

The active or reported route does not follow the policy chain or mission contract.

## Output Contract

The generated artifact must:

- record generated timestamp
- record the 4 truth layers
- classify each drift item into one canonical drift class
- include severity
- include node_id or scope when possible
- include runtime value and artifact value when applicable

## Current Artifact

Machine-readable drift report:

- `runtime/federation_orchestrator/drift_verification_report.json`

## Reporting Rule

Reports should clearly separate:

- live runtime truth
- source truth
- registry truth
- artifact truth

Do not collapse them into a single narrative state.
