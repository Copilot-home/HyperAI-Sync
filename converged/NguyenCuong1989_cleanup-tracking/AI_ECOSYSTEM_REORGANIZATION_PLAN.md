# [B4] TOPIC & PLAN - AI Ecosystem Consolidation to ~/Andy

**Topic:** Scattered AI ecosystem (ai-system, tr-gi-p, backups, alternatives) needs consolidation into proper macOS-compliant directories under /Users/andy with clear separation of active/backup/data layers.

## Proposed macOS-Compliant Structure

```
~/Projects/AI/                          # Active AI Development
├── HyperAI/                           # Primary HyperAI system (from ai-system/)
│   ├── core/                          # Core DAIOF + HyperAI systems
│   ├── engines/                       # AI engines (phoenix, brain)
│   ├── agents/                        # Agent implementations
│   └── api/                           # REST/HTTP APIs
├── DAIOF-Framework/                   # Protocol framework
├── MCP-Ecosystem/                     # MCP server implementations
│   ├── instances/                     # Running MCP servers
│   └── extensions/                    # VS Code integration
└── Tools/                             # Supporting tools
    ├── CLI/
    ├── Tracing/                       # copilot_trace_scan
    └── Training-Data/                 # chain-data

~/Library/Developer/HyperAI/           # Development/Build artifacts
├── build/
├── cache/
└── logs/

~/Archive/HyperAI-Ecosystem/           # Consolidated backups & alternatives
├── 2025-10-12_tr-gi-p_backup/        # Archived tr-gi-p snapshots
├── hyperAI-1_alternative/            # Alternative implementations
├── legacy-systems/                    # Old versions
└── workspace-snapshots/               # Historical workspace states
```

## [B4-PLAN] Reorganization Steps

### PHASE 1: Analysis & Mapping (READ-ONLY)
1. Identify active system in tr-gi-p vs ai-system (which one is being used?)
2. Check Git history to understand project evolution
3. Verify MCP servers dependencies
4. List all active configuration files

### PHASE 2: Consolidation (WITH GIT TRACKING)

**Step 1: Create new structure**
   - mkdir -p ~/Projects/AI/{HyperAI/core,HyperAI/engines,HyperAI/agents,MCP-Ecosystem/instances,Tools}
   - mkdir -p ~/Library/Developer/HyperAI/{build,cache,logs}
   - mkdir -p ~/Archive/HyperAI-Ecosystem/{backups,alternatives,legacy,snapshots}

**Step 2: Move primary active system**
   - Move ~/ai-system/* → ~/Projects/AI/HyperAI/core/ (if active)
   - Move ~/tr-gi-p/ACTIVE_SYSTEMS/* → ~/Projects/AI/HyperAI/engines/
   - Move ~/tr-gi-p/hyperai_phoenix* → ~/Projects/AI/HyperAI/engines/

**Step 3: Consolidate supporting systems**
   - Move ~/daiof-vscode-extension-ecosystem → ~/Projects/AI/MCP-Ecosystem/
   - Move ~/mcpServers → ~/Projects/AI/MCP-Ecosystem/instances/
   - Move ~/copilot_trace_scan → ~/Projects/AI/Tools/Tracing/
   - Move ~/chain-data → ~/Projects/AI/Tools/Training-Data/
   - Move ~/cli → ~/Projects/AI/Tools/CLI/

**Step 4: Archive old/backup systems**
   - Move ~/tr-gi-p_BACKUP_* → ~/Archive/HyperAI-Ecosystem/backups/
   - Move ~/tr-gi-p/legacy/ → ~/Archive/HyperAI-Ecosystem/legacy/
   - Move ~/tr-gi-p/temp_backup/ → ~/Archive/HyperAI-Ecosystem/snapshots/
   - Move ~/Documents/GitHub/hyperAI → ~/Archive/HyperAI-Ecosystem/alternatives/hyperAI-github/
   - Move ~/hyperAI-1 → ~/Archive/HyperAI-Ecosystem/alternatives/hyperAI-1/

**Step 5: Clean home directory**
   - Delete ~/ai-system (consolidated to Projects/AI)
   - Delete ~/tr-gi-p (contents moved to Projects/AI + Archive)
   - Remove scattered directories from root

**Step 6: Update references**
   - Update VS Code workspace settings to point to new paths
   - Update MCP server paths in mcp.json
   - Update environment variables (if any reference old paths)
   - Update Git remotes for active projects

**Step 7: Create symbolic links (optional)**
   - ln -s ~/Projects/AI/HyperAI ~/hyperai (backward compatibility)
   - ln -s ~/Archive ~/archive (for convenience)

### PHASE 3: Verification
1. Test MCP servers launch from new locations
2. Verify all Git repositories still functional
3. Check no broken symlinks or missing dependencies
4. Validate disk usage after consolidation

## Safety Measures
- All operations tracked in cleanup-tracking Git repo
- Each move operation logged with timestamp
- Original backups preserved in ~/Archive/ until confirmed working
- Symbolic links for backward compatibility if needed
- Git history preserved on all projects

## Expected Benefits
✓ Clean home directory (removes 7+ scattered directories)
✓ Proper organization following macOS conventions
✓ Clear separation: active (Projects/) vs archive (Archive/)
✓ Easy to backup entire ecosystem (single Projects/AI folder)
✓ Better IDE integration and discovery
✓ Easier onboarding for future systems

## Questions for User (BEFORE EXECUTION)

1. **Which is the ACTIVE system?** ai-system or tr-gi-p?
2. **Keep symbolic links?** For backward compatibility?
3. **Archive strategy:** How long to keep backups before deleting?
4. **MCP server state:** Are servers configured to auto-start? Need to reconfigure paths?
5. **Git remotes:** Which repos are under version control? Need path updates?

