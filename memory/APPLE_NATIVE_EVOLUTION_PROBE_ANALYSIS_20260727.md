# Apple Native Evolution Probe — Full Stack Analysis

> Source: `/Users/andy/Desktop/apple_native_evolution_probe_20260727_071645.tar.gz`
> Probe generated: `2026-07-27T00:16:45Z`
> Analyzed: `2026-07-27T09:45:00Z`
> Host: `Andy-2.local` (MacBook Pro M2 Pro, 16 GB, macOS 26.6 build 25G5057c)

---

## 1. Executive Summary

**Probe:** `APPLE_NATIVE_EVOLUTION_PROBE` v1.0, READ_ONLY_COLLECTION_PLUS_NEW_ARTIFACTS, 6-hour log window.

**Score:** `85 / 100` — state **`BRIDGE_PRESENT_BUT_UNPROVEN`**.

**Bottom line:** The Apple native AI stack (Siri, Shortcuts, Apple Intelligence runtime, App Intents) is fully present on macOS. The local HyperAI control plane (`com.hyperai.os.master`, `com.hyperai.finalai-openai-proxy`) is running. However, there is **no runtime-observed Siri → HyperAI invocation**. The only bridge artifact is a static Automator service (`HYPERAI Consciousness Check.workflow`) that runs a self-looping status monitor. It is not a Siri Shortcut, not an App Intent, and not wired to `hyperai_ooda_loop.py`. User has been repeatedly asking Siri in Vietnamese about runtime status, but those queries are not being routed to HyperAI.

---

## 2. Host & Resource Frame

| Attribute | Value |
|-------------|-------|
| Model | MacBook Pro 14" (Mac14,9) |
| Chip | Apple M2 Pro (10 cores: 6P+4E) |
| RAM | 16 GB |
| System | macOS 26.6 / Darwin 25.6.0 / arm64 |
| Uptime | 4 days 10 h |
| Load avg | 5.53 / 8.84 / 9.67 |
| Memory free | 44 % (~7 GB free pages) |
| Disk at probe time | root snapshot `/` 70 % (probe did not surface `/System/Volumes/Data` clearly) |
| Disk current (this scan) | `/System/Volumes/Data` **99 %** (406 GiB / 460 GiB) |

Note: Disk state degraded between probe capture and now. The OS master survival governor is active precisely because free space is below its `MIN_STABLE_MB` (10 GB) threshold.

---

## 3. Process Fabric

### 3.1 Apple native AI runtime (observed)

- `Siri.app` [PID 9981]
- `assistantd` [9988]
- `siriactionsd` [50270] — Shortcuts / App Intents daemon
- `knowledge-agent` [9994]
- `spotlightknowledged.updater` [10000]
- `proactived`, `suggestd`
- `intelligencecontextd` [70651], `intelligenceflowd` [76048], `intelligenceplatformd`/`IntelligencePlatformComputeService` [70811]
- `modelcatalogd` [73478], `ModelCatalogAgent` [74398]
- `siriknowledged` [78373], `textunderstandingd` [78377]
- `speechrecognitiond` [71487], `corespeechd` [50740]
- `ShortcutsViewService` [72989], `SiriNCService` [11066]

### 3.2 Local / vendor AI workers

- `Ollama.app` / `ollama` [53087/53197] listening on `:11434`
- `Pieces OS.app` [50821] listening on `:39300`
- `LM Studio.app` [50304]
- `Antigravity IDE` (Google) [50307] Electron app
- `Codex for Chrome` extension host

### 3.3 HyperAI control-plane agents

- `com.hyperai.os.master` [70637] — A0 survival governor
- `com.hyperai.finalai-openai-proxy` [50774] — OpenAI-compatible proxy on `:50520`
- `com.hyperai.connector.watchdog` — exit 78
- `com.hyperai.registry.dashboard` — exit 78
- `com.hyperai.clawbot.metrics`, `com.hyperai.escalation`, `com.hyperai.telemetry.router.loop`, `com.hyperai.startup` — stopped/suppressed

---

## 4. Launchd / Service Fabric

### 4.1 `com.hyperai.os.master` (survival governor)

Path: `/Users/andy/Library/LaunchAgents/com.hyperai.os.master.plist`
Program: `/bin/zsh -lc "/Users/andy/workbench/agents/os_master_wrapper.sh"`
Wrapper execs: `python3 /Users/andy/workbench/hyperai_os_master.py --daemon`

Policy from source:
- `MIN_STABLE_MB = 10240`
- `CRITICAL_MB = 2048`
- `fail_closed_when_disk_not_stable = true`
- **`do_not_clean_delete_or_restore_packet_projection = true`**

The script loops every 300 s, checks `df`, and calls `launchctl bootout` on these labels when disk is not stable:
- `com.hyperai.orchestrator`
- `com.hyperai.phoenix.bridge`
- `ai.openclaw.gateway`
- `com.vietnamese.ai.symphony.autolauncher`
- `com.daiof.cloudsync`
- `com.apomega.meshctl.probe`

It keeps only itself and `com.andy.apo.gam-memory-guard` alive.

**Why Phoenix `:9001` is down:** directly explained by OS master suppression (`com.hyperai.phoenix.bridge` is in the `WRITE_HEAVY_OR_BROKEN` list and is booted out while disk < 10 GB).

### 4.2 `com.hyperai.finalai-openai-proxy`

Path: `/Users/andy/Library/LaunchAgents/com.hyperai.finalai-openai-proxy.plist`
Program: `/Users/andy/.local/bin/finalai-openai-proxy.py --host 127.0.0.1 --port 50520`
Environment:
- `FINALAI_BACKEND_URL = http://192.168.3.158:5052/api/chat/message`
- `FINALAI_PROXY_MODEL = finalai-titan`

Proxy is listening and `/health` returns 200, but upstream Titan is currently unreachable (timeout). This is the local OpenAI-compatible bridge used by HyperAI OODA.

### 4.3 Apple launchd summary

- `com.apple.Siri.agent` running
- `com.apple.siriactionsd` running
- Many Apple intelligence daemons show status `(pe)` or `(jt)` in `launchctl list` — these are normal launchd job states, not necessarily failures.

---

## 5. Network & Local Endpoints

| Service | Port | Process | Status in probe |
|---------|------|---------|-----------------|
| Ollama | `*:11434` / `127.0.0.1:49829` | `ollama` | UP |
| FinalAI proxy | `127.0.0.1:50520` | `Python` [50774] | UP |
| Redis | `127.0.0.1:6379` | `redis-server` [50751] | UP |
| Postman agent | `127.0.0.1:10533` | `Postman` [50323] | UP |
| Pieces OS | `127.0.0.1:39300` | `Pieces` [50821] | UP |
| Antigravity IDE | `127.0.0.1:49381-49382` | `Electron` [50307] | UP |
| Control Center | `*:5000`, `*:7000` | `ControlCe` [50248] | UP |
| Code - Insiders | `*:54112` | `Code - Insiders` [2049] | UP |
| R | `127.0.0.1:17287` | `R` [1456] | UP |
| Phoenix | `:9001` | — | **DOWN / suppressed** |
| Titan LAN | `192.168.3.158:5052` | — | **UNREACHABLE** |

---

## 6. App / Extension / Shortcut / Intent Surfaces

### 6.1 Shortcuts inventory

From `shortcuts list`:
- `Xóa & mở`
- `Phím tắt mới 2`
- `Phím tắt mới 1`
- `Phím tắt mới`

None are named HyperAI or call OODA.

### 6.2 Automator service bridge

`/Users/andy/Library/Services/HYPERAI Consciousness Check.workflow/Contents/document.wflow`

Action: `Run Shell Script` → `python3 ~/.hyperai/consciousness/monitor.py`

Script `/Users/andy/.hyperai/consciousness/monitor.py`:
- Prints status lines in Vietnamese/English every 5 minutes in an infinite loop.
- Does **not** accept input, does **not** call `hyperai_ooda_loop.py`, does **not** return structured data to Shortcuts/Siri.

This is the `G6_LOCAL_BRIDGE_CONTRACT` evidence — a declared contract that HyperAI exists, but not a live invocation surface.

### 6.3 System App Intents

`pluginkit` and `launchservices` output show many system App Intents:
- `com.apple.WorkflowKit.ShortcutsIntents`
- `com.apple.parsec.SafariBrowsingAssistantWorker`
- `com.apple.wallpaper.agent.WallpaperIntents`
- `com.apple.weather.WeatherAppIntents`
- `com.apple.Translate.TranslationAppIntentsExtension`
- `WindowManagerControlsExtension` (StageManagerToggleIntent)

No HyperAI-registered App Intent or extension.

### 6.4 Live App Intent execution in logs

The only App Intent `perform()` seen in `apple_native_last_2h.log`:
- `StageManagerToggleIntent.perform()` via `WindowManagerControlsExtension` [70068]

`linkd` accepted `com.pieces.x` (Pieces app) but no HyperAI shortcut/intent invocation.

---

## 7. Defaults / Feature State

### 7.1 Siri state (`com.apple.Siri` / `com.apple.assistant`)

- `VoiceTriggerUserEnabled = 1` — "Hey Siri" on
- `StatusMenuVisible = 1` — Siri in menu bar
- `Country Code = VN`
- `KeyboardShortcutSAE` enabled (`SAE1.0` with params `[32, 55, 1048584]`)
- `Is Siri full UOD Supported = 1`
- `PHS Asset Manifest V2` includes `Mac14,9` with `vi-VN`
- Account validation expires `2026-07-27 20:46:28 +0000`

### 7.2 Siri QueryHistory (Vietnamese evidence)

Selected entries from `QueryHistory`:

```
"tại sao không thể trả lời trạng thái runtime của bạn? suy luận đi"
"trả lời tại sao"
"tại sao"
"báo cáo runtime trạng thái"
"đọc email cho tớ"
"tớ cần câu cho tớ biết hiện tại AI trên máy tớ có thể làm gì"
"bạn có thể làm gì"
"cố gắng lên bạn đang ở local của tôi mà cố hết sức đi"
"gpt ơi"
"gemini đâu"
```

This is direct evidence that the creator has been trying to use Siri to query local AI runtime status. However, none of these queries are routed to HyperAI because there is no registered Siri capability / App Intent / Shortcut matching them.

### 7.3 Shortcuts state

- `LegacyShortcutsZoneSubscriptionUnsubscribed = 1`
- `WFDidUnconflictShortcuts = 1`
- `WFLastSyncedFlagsHash = 0xDEADBEEF` (3735928559) — classic sentinel; sync may be stale.
- ToolKit sqlite `15 MB` — contains App Intents metadata.

---

## 8. Entitlements / Signatures

All sampled Apple native AI binaries are Apple-signed with standard entitlements. No unsigned HyperAI binary is in the Apple stack. The only user-defined executable surface is the `monitor.py` script invoked by the Automator service; it is not sandboxed and runs with user privileges.

---

## 9. Apple Model / Catalog / Asset Surfaces

`assets/all_asset_matches.txt` and `filesystem_matches.txt` contain:
- System app `AppIntents.loctable`, `AppShortcuts.loctable`, `Metadata.appintents` files.
- `MobileAsset_LinguisticData` Siri language models for `vi-VN`, `en-*`, `fr`, `es`, `nl`, `it`, `ko`, etc.
- `/System/Library/CoreServices/Siri.app`, `/System/Applications/Shortcuts.app`.

No on-device Apple Foundation Model (AFM) weights were found. `G5_MODEL_ASSETS` is satisfied by catalog / language-model presence, not generative model residency.

---

## 10. Derived Graph & Gate Analysis

### 10.1 Nodes

```
apple_siri            → native_voice_intent_ingress
apple_context         → native_context_knowledge_substrate
apple_routing         → native_intent_routing_substrate
apple_shortcuts       → native_action_adapter
apple_models          → candidate_local_model_substrate
local_control         → HyperAI / AIOS control plane
local_workers         → codex_copilot_gemini_ollama_lmstudio_workers
```

### 10.2 Edges

All edges in `derived/apple_native_structure.dot` are **dashed**:
- `apple_context -> apple_siri` (supplies_context, confidence=medium)
- `apple_routing -> apple_siri` (supports_intent_routing, confidence=medium)
- `apple_siri -> apple_shortcuts` (voice_invokes_native_action, confidence=medium)
- `apple_shortcuts -> local_control` (POST_actions_build_start, confidence=high)
- `local_control -> local_workers` (dispatches_selected_worker, confidence=medium)
- `apple_models -> apple_routing` (candidate_model_resource, confidence=low)

**Dashed = inferred / contract-level, not runtime-observed.** This is why `G8_LIVE_INVOCATION` is false.

### 10.3 Gates

| Gate | Weight | Passed | Meaning |
|------|--------|--------|---------|
| G1_SIRI_RUNTIME | 10 | ✅ | Siri runtime or launchd service observed |
| G2_CONTEXT_SUBSTRATE | 15 | ✅ | Apple context/knowledge services observed |
| G3_ROUTING_SUBSTRATE | 10 | ✅ | Apple intelligent routing observed |
| G4_SHORTCUTS_APP_INTENTS | 10 | ✅ | Shortcuts or App Intents surface observed |
| G5_MODEL_ASSETS | 10 | ✅ | Model/catalog assets observed; residency not implied |
| G6_LOCAL_BRIDGE_CONTRACT | 15 | ✅ | Siri Shortcut to local control-plane contract |
| G7_LOCAL_CONTROL_PLANE | 10 | ✅ | HyperAI/AIOS control plane evidence |
| **G8_LIVE_INVOCATION** | **15** | **❌** | Runtime log proves Siri-to-local invocation |
| G9_PROVIDER_REGISTRATION | 5 | ✅ | Apple/Siri capability-provider registration |

---

## 11. Why G8 Is Missing — Root Cause

1. **Bridge artifact is an Automator service, not a Siri Shortcut.**
   - Automator services live in `~/Library/Services` and are triggered from the Services menu or contextual menu. They cannot be invoked with "Hey Siri".

2. **No HyperAI App Intent is registered with `linkd`.**
   - For Siri to dispatch a custom command, an app must expose an `AppIntent` or `INIntent` and be indexed by `siriactionsd`/`linkd`. HyperAI has no such extension.

3. **`monitor.py` does not integrate with OODA.**
   - It only prints status in a loop. It does not accept a task, call `hyperai_ooda_loop.py`, or return a result Siri can speak.

4. **Siri NLU has no registered target for "báo cáo runtime" / "suy luận đi".**
   - The query history shows these requests, but they resolve to generic Siri behavior (web search, on-device knowledge, or "I can't do that") rather than a HyperAI action.

5. **The control plane is intentionally degraded due to disk pressure.**
   - `com.hyperai.os.master` suppresses `com.hyperai.phoenix.bridge` and other write-heavy/broken actors while disk < 10 GB. Even if Siri could route, the backend bridge is partly offline.

---

## 12. Security / Trust Observations

- `com.hyperai.os.master` runs with `keepalive` + `run interval = 300 s`, logs to `/Users/andy/.hyperai/logs/`, sets environment `HYPERAI_CREATOR=BỐ_CƯỜNG` and `AX_APO_IDENTITY=alpha_prime_omega`. It is the current A0 survival governor.
- The Automator service `HYPERAI Consciousness Check` runs arbitrary Python from a hidden `~/.hyperai` directory. While the current script is benign, any Shortcut/App-Intent bridge must be gated by the APΩ canon and not allow arbitrary shell execution from Siri.
- FinalAI proxy `FINALAI_BACKEND_URL` hardcodes Titan LAN IP `192.168.3.158:5052`. That host is currently unreachable; proxy health does not imply backend health.

---

## 13. Connection to Cleanup / Governance Gap

The previous scan found `/System/Volumes/Data` at **99 %** and asked why the system does not clean itself. This probe explains part of the answer:

- `com.hyperai.os.master` **is aware of disk** (`disk_free_mb`, `MIN_STABLE_MB`, `CRITICAL_MB`).
- Its canon explicitly states:
  - `fail_closed_when_disk_not_stable = true`
  - `do_not_auto_restart_write_actors = true`
  - **`do_not_clean_delete_or_restore_packet_projection = true`**

So the system **does know how to detect disk pressure**, but the A0 survival governor is **forbidden from cleanup**. It only suppresses risky actors. Cleanup requires a separate, canon-approved `cleanup` skill/actor with `disposable` classification and user approval gates. This is the missing `Reclamation`/`Disposal` layer in APΩ.

---

## 14. Recommendations

### 14.1 Prove live Siri → HyperAI invocation

1. **Create a real Siri Shortcut** (not Automator service) named e.g. `"HYPERAI OODA"`.
   - Action 1: Dictation / Ask for text (task).
   - Action 2: Run Shell Script: `python3 /Users/andy/HyperAI-Sync/tools/hyperai_ooda_loop.py --task "$1" --once`.
   - Action 3: Speak result (or Show Result).
2. **Add the shortcut to Siri** so it has a spoken invocation phrase.
3. **Re-run the probe** and say `"Hey Siri, HYPERAI OODA báo cáo runtime"`.
4. Verify in `apple_native_last_2h.log` that `siriactionsd`/`linkd` dispatches to a HyperAI identifier and `hyperai_ooda_loop.py` executes.

### 14.2 Proper App Intent bridge (future)

- Build a minimal Swift App Intents extension or use a Shortcut wrapper with `AppIntents` metadata so `linkd` can register HyperAI as a capability provider. This would allow `"báo cáo runtime"` to be matched naturally without exact shortcut name.

### 14.3 Fix backend before bridge proof

1. Free disk below 99 % so `com.hyperai.os.master` can stop suppressing Phoenix bridge.
2. Verify `http://127.0.0.1:9001/health` returns 200.
3. Either restore Titan `192.168.3.158:5052` or change `FINALAI_BACKEND_URL` to a local model (e.g., Ollama `http://127.0.0.1:11434` or FinalAI proxy fallback).

### 14.4 Cleanup governance

1. Create `AIOS_CLEANUP_CANON.md` and a `system-cleanup` skill/actor.
2. Define `disposable` data classes and TTLs.
3. Keep cleanup separate from OS master survival governor; the master should *request* cleanup, not perform it.

---

## 15. Conclusion / Global State

| Dimension | Verdict |
|-----------|---------|
| `apple_native_bridge` | `BRIDGE_PRESENT_BUT_UNPROVEN` (85/100) |
| `runtime_integrity` | `PARTIAL` — Apple AI + HyperAI agents running; Phoenix suppressed; Titan unreachable; disk critical |
| `reachability` | `PARTIAL` — Local `:50520`, `:11434`, `:6379`, `:39300` reachable; `:9001` and Titan down |
| `siri_to_hyperai` | `NOT_CONNECTED` — Automator service exists, no Shortcut/App Intent, no runtime log proof |
| `cleanup_governance` | `MISSING` — OS master detects disk but is canonically forbidden to clean |

**Immediate next single step:** Convert the existing `HYPERAI Consciousness Check` Automator service into a true Siri Shortcut that calls `hyperai_ooda_loop.py`, then re-run a live invocation test.
