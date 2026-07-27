# AIOS Telegram Native Control Lane

Date: 2026-04-19

## Purpose

This lane exists so HyperAI can control Telegram Desktop directly when browser launch works but Bot API proof is still blocked.

It is a subordinate execution lane under `ooda_control_contract`, not a shell-authority expansion.

## Current Proven Workflow

```text
HyperAI UI / browser lane
-> open Telegram launch page
-> tg:// handoff
-> Telegram Desktop window focus
-> paste command
-> submit command
-> write proof artifact
```

## Current Proven Artifacts

- `runtime/telegram_node/botfather_browser_probe.json`
- `runtime/telegram_node/telegram_client_probe.json`
- `runtime/telegram_node/telegram_desktop_control_probe.json`
- `runtime/telegram_node/telegram_desktop_capture_probe.json`
- `runtime/telegram_node/botfather_client_run.json`
- `runtime/federation_orchestrator/telegram_native_control_contract.json`

## What Is Proven

- Browser-to-native Telegram handoff is proven.
- Telegram Desktop process presence is proven.
- Native desktop command send is proven for BotFather.

## What Is Not Yet Proven

- Reliable text readback from Telegram Desktop.
- OCR or UI Automation parsing of BotFather replies.
- Full `/newbot` or `/token` automation end-to-end.

## Operating Rule

Use this lane for bounded command execution and evidence capture only.

Do not treat it as business-state authority.

Do not promote BotFather-native actions into `target_proof` or `send_proof` unless a repo-governed proof contract explicitly maps those actions into the Telegram mastery equation.

## Next Optimization Order

1. Add visual capture after command send.
2. Add readback/OCR or UIA parsing.
3. Automate bounded BotFather token-retrieval flow.
4. Feed token into HyperAI UI intake path.
5. Return to Bot API target discovery.

## BotFather Client

Repo-governed helper:

- `tools/botfather_client.py`

Supported modes:

- `open`
- `safe-command`
- `plan-create-bot`
- `plan-token`

Use `safe-command` for low-risk command send plus screenshot proof.
Use the planning modes to keep BotFather operations bounded by official Telegram rules before sending a high-impact sequence.
