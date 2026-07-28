v1

## User Profile

Andy treats Codex as runtime labor operating under his Canon/provenance rules, not as an author or owner. His recurring work in this memory set centers on HyperAI/AIOS runtime supervision in `/Users/andy`, Slot Project local-runtime validation in `/Users/andy/Slot-project-local-full/Slot-project`, and Codex automation upkeep across rotating worktrees. He expects workflow contracts, named skill order, and repo/runtime boundaries to be preserved exactly once given.

He prefers execution over plan restatement on operational tasks, but with hard gates: no invented verification, no ungated uploads/deploys/cloud calls, no ownership transfer language, and no broad scans when a contract defines an early-stop state. Good output is compact, evidence-backed, and usually packetized, with one next safe step instead of a long narrative. When a run is read-only, he expects the agent to keep probes narrow and to treat live state as run-specific rather than reusing stale assumptions.

## User preferences

- When the user gives an operational workflow, execute it and validate it instead of restating the plan.
- For automation runs, read the automation memory first and keep results anchored to exact files, commands, and terminal states.
- For HyperAI read-only heartbeats, stay non-invasive and report only deltas, broken anchors, and the next single safe step.
- For `hyperai-skill-orchestrator`, preserve `hyperai-runtime-orchestrator` first, then `find-skills`, keep packetized output, and stop at `HEARTBEAT_NO_EVENT` when the queue lacks `event_id`, `status=pending`, `priority`, and `intent`.
- For `daily-bug-scan`, use concrete repo evidence only; empty commit windows or weak evidence should end as `NO_NEW_COMMITS` / no findings.
- Treat stale worktree paths and repo identity as different things; prefer `git rev-parse --git-common-dir` and `/Users/andy/.git` over literal historical worktree equality.
- For Slot Project local automation, keep Hugging Face/training/upload behavior capture-only unless Andy explicitly opens that gate.
- When the user names a workflow frame such as `game-studio:*`, `vercel:investigation-mode`, or a provider boundary such as `skills.sh`, stay inside that frame rather than drifting to adjacent tooling.
- In ownership/provenance threads, do not imply appropriation, assistant authorship, or ownership transfer over Andy’s content or system identity.

## General Tips

- Start consolidation from [`/Users/andy/.codex/memories/phase2_workspace_diff.md`](/Users/andy/.codex/memories/phase2_workspace_diff.md), then use [`/Users/andy/.codex/memories/raw_memories.md`](/Users/andy/.codex/memories/raw_memories.md) as the routing layer and open matching rollout summaries only when they sharpen wording, validation, or conflicts.
- Check extension instructions before consolidating; current guidance is in [`/Users/andy/.codex/memories/extensions/ad_hoc/instructions.md`](/Users/andy/.codex/memories/extensions/ad_hoc/instructions.md). [ad-hoc note]
- Repeated workflow shortcuts live in [`/Users/andy/.codex/memories/skills/hyperai-readonly-heartbeat/SKILL.md`](/Users/andy/.codex/memories/skills/hyperai-readonly-heartbeat/SKILL.md), [`/Users/andy/.codex/memories/skills/hyperai-skill-orchestrator-heartbeat/SKILL.md`](/Users/andy/.codex/memories/skills/hyperai-skill-orchestrator-heartbeat/SKILL.md), [`/Users/andy/.codex/memories/skills/slot-local-runtime-template/SKILL.md`](/Users/andy/.codex/memories/skills/slot-local-runtime-template/SKILL.md), and [`/Users/andy/.codex/memories/skills/daily-bug-scan-preflight/SKILL.md`](/Users/andy/.codex/memories/skills/daily-bug-scan-preflight/SKILL.md).
- Treat instruction-only rollouts as contracts/preferences, not proof of successful execution.
- For HyperAI heartbeats, re-probe `11435` and `9999` each run; prior failures were not stable and later recovered.
- For Slot local runs, `split_surface_test.cjs` can fail on the Chrome autoplay warning even when all boundary checks pass; treat that as a specific known failure mode, not a generic browser break.
- When a memory depends only on deleted rollout evidence, remove it rather than preserving stale convenience.

## What's in Memory

### /Users/andy

#### 2026-06-05

- HyperAI read-only heartbeat recovered anchors: hyperai-autonomous-runtime-heartbeat, AIOS_MISSION_ROUTER, aios_verify_run, 11435, 9999/health, runtime_execution_todo.md
  - desc: Search this first for `cwd=/Users/andy` read-only heartbeat runs that need current router verification, queue inspection, or delta-only reporting.
  - learnings: The 2026-06-05 run confirmed `11435` and `9999` recovered, so endpoint health must be treated as run-specific even when earlier notes marked them broken.

#### 2026-06-02

- HyperAI skill-orchestrator queue gating: hyperai-skill-orchestrator, hyperai-runtime-orchestrator, find-skills, HEARTBEAT_NO_EVENT, event_id, status=pending, npx skills --help
  - desc: Use this for event-bus-first heartbeat/queue validation, stop-code routing, and the exact packetized report shape under `cwd=/Users/andy`.
  - learnings: The durable path is memory first, required skill anchors next, `verify.run` plus `npx skills --help`, then stop immediately when the queue lacks explicit pending-event schema.

### /Users/andy/Slot-project-local-full/Slot-project

#### 2026-06-05

- Slot local runtime automation template: local_runtime, AUTOMATION_TEMPLATE.md, TRAINING_PLAN.md, 8130, cloud_upload_authorized=false, SieuNoMax
  - desc: Search this first for `cwd=/Users/andy/Slot-project-local-full/Slot-project` when a run needs local template execution, fresh-boot vs reuse decisions, or evidence-only reporting on game/admin boundaries.
  - learnings: Probe `8130` first, reuse the listener when healthy, boot `SLOT_LOCAL_PORT=8130 python3 local_runtime/server.py` when down, and keep HF/training behavior local-only.

#### 2026-06-02

- Slot autoplay-warning failure shield: split_surface_test.cjs, AudioContext was not allowed to start, user gesture, console warning fatal
  - desc: Use this when Slot browser checks fail despite otherwise clean boundary results; it routes to the known Chrome autoplay warning case.
  - learnings: `split_surface_test.cjs` currently treats the autoplay warning as fatal, so the likely fixes are warning allowlisting or gating audio startup behind a user gesture.

### /Users/andy/.codex/worktrees/*/andy

#### 2026-06-02

- daily-bug-scan repo-identity preflight: daily-bug-scan, git rev-parse, --git-common-dir, /Users/andy/.git, NO_NEW_COMMITS, WORKSPACE_MISMATCH
  - desc: Use this for recurring `daily-bug-scan` automation runs across rotating Codex worktrees; details live in the `automation/daily-bug-scan across Codex worktrees` block in [`/Users/andy/.codex/memories/MEMORY.md`](/Users/andy/.codex/memories/MEMORY.md).
  - learnings: Read automation memory first, treat `/Users/andy/.git` as the durable repo-identity anchor, record stale historical worktree paths as drift, and stop cleanly when both commit windows are empty.

### Older Memory Topics

#### /Users/andy/.codex/worktrees/4294/andy

- Contributor credit, ownership docs, and skills.sh scope correction: all-contributors, CONTRIBUTOR_PROFILE.md, OPEN_SOURCE_CREDIT.md, skills.sh, DockerHub, JSON Schema
  - desc: Search this first for repo credit wiring, public ownership-boundary docs, or correcting a `skills.sh` versus DockerHub scope drift in `cwd=/Users/andy/.codex/worktrees/4294/andy`.

#### /Users/andy

- HyperAI closed-loop recovery and lightweight LLM binding: Phoenix bridge, qwen2.5:0.5b, /trigger, AUDIT_ORCHESTRATOR, RUN_COMPLEX_WORKFLOW, 9001
  - desc: Use this for HyperAI runtime repair/binding work in `cwd=/Users/andy` where the loop method, bridge paths, or deterministic audit logic matter.

- Σ_APΩ/N-Homes runtime-app implementation: AgentOS + Electron, xcodebuildmcp, hyperai-core, docker scout, agent_os.py
  - desc: Use when the task re-enters the `/Users/andy` runtime-app plan and needs the locked roots, iOS spec-only rule, HyperAI Docker cleanup steps, or the `except Exception: pass` backend failure fix.
