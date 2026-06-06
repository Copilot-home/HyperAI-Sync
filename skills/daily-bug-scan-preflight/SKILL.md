---
name: daily-bug-scan-preflight
description: Preflight and run the daily-bug-scan automation when the task mentions recent commits, WORKSPACE_MISMATCH, NO_NEW_COMMITS, or evidence-backed bug-risk triage across Codex worktrees.
argument-hint: "[cutoff-iso-or-auto]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Daily Bug Scan Preflight

## When to use

Use when the task is the `daily-bug-scan` automation or asks for recent-commit triage in `/Users/andy/.codex/worktrees/*/andy`.

Do not use for general code review, broad bug hunting without a commit window, or repo work outside the `/Users/andy/.git` identity family.

## Inputs / context to gather

1. Read `$CODEX_HOME/automations/daily-bug-scan/memory.md` first.
2. Capture `pwd`, `git rev-parse --show-toplevel`, and `git rev-parse --git-common-dir`.
3. Determine the cutoff:
   - If `$ARGUMENTS` provides an ISO timestamp, use it.
   - Otherwise recover the last-run cutoff from automation memory or the prompt.

## Procedure

1. Verify you are in a git worktree and read the automation memory before any scan.
2. Compare repository identity, not just the literal worktree path:
   - `git rev-parse --show-toplevel`
   - `git rev-parse --git-common-dir`
3. If repo identity differs from the canonical identity in memory, return `WORKSPACE_MISMATCH` and stop.
4. Run the two commit-window probes:
   - `git log --since='<cutoff>' --format='%H %cI %s'`
   - `git log --since='24 hours ago' --format='%H %cI %s'`
5. If both windows are empty, return `NO_NEW_COMMITS` and stop.
6. If commits exist, only continue into diff/test/CI review when you have concrete evidence sources; otherwise report that no evidence-backed bug risks were found.
7. Append a short memory note with anchor verification, commit-window result, and terminal status.

## Efficiency plan

- Stop after memory read plus the two `git rev-parse` probes if repo identity mismatches.
- Stop after the two `git log` probes if both windows are empty.
- Do not inspect diffs, tests, or CI unless commit evidence exists.
- Reuse the current `git-common-dir` result as the decisive anchor throughout the run.

## Pitfalls and fixes

- Symptom: current worktree path differs from the memory path.
  - Likely cause: Codex rotated to a new worktree while the repo identity stayed the same.
  - Fix: use `git-common-dir` as the decisive check; only abort when repository identity differs.
- Symptom: the scan starts inventing bugs despite empty windows.
  - Likely cause: the automation drifted from evidence triage into speculative review.
  - Fix: return `NO_NEW_COMMITS` or no findings and stop.
- Symptom: the run appends normal scan output after a mismatch.
  - Likely cause: abort path was not kept separate.
  - Fix: write a dedicated `WORKSPACE_MISMATCH abort` note instead.

## Verification checklist

- Automation memory was read first.
- `git rev-parse --show-toplevel` and `git rev-parse --git-common-dir` were captured.
- Terminal status is one of `WORKSPACE_MISMATCH`, `NO_NEW_COMMITS`, or evidence-backed findings.
- Any reported bug risk is backed by commit/diff/test/CI/log evidence.
- The automation memory note records anchor verification and the terminal result.

