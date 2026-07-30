# Skill Tool `path` Validation Fix

**Issue:** `Tool 'skill' validation failed: The 'path' parameter is required for the 'list' command.`

**Root cause:** The in-session `skill` tool's `list` and `search` commands require a `path` parameter. The default is `null`, and the tool fails fast when `path` is missing.

**Fix applied:**
1. Added `## Tool Guardrails` to three AGENTS.md files so the assistant always passes `path`:
   - `/Users/andy/AGENTS.md`
   - `/Users/andy/.codex/AGENTS.md`
   - `/Users/andy/HyperAI-Sync/AGENTS.md`
2. Verified the corrected call patterns:
   - `skill list path=/Users/andy/HyperAI-Sync`
   - `skill search path=/Users/andy/HyperAI-Sync keywords=...`
3. Documented the fallback CLI for listing all installed skills:
   - `devin skills list`

**Verification:**
- `skill list path=/Users/andy/HyperAI-Sync` → returns `No skills found in ...` (no validation error).
- `skill search path=/Users/andy/HyperAI-Sync keywords=orchestrator` → returns `No skills found ... matching ...` (no validation error).
- `devin skills list` → returns full skill catalog (global + user skills) successfully.

**Notes:**
- The binary/schema of the `skill` tool cannot be patched from user space.
- The AGENTS.md guardrails are the operational fix to prevent future missing-path calls.
- Project-level `.devin/skills/` directories can be added later if the project needs in-session discoverable skills.
