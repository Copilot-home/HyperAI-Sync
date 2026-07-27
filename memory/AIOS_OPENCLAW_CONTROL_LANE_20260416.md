# AIOS OpenClaw Control Lane

## Classification

- Surface: OpenClaw 2026.4.14, build 323493f.
- Runtime class: observed operator/control lane.
- Graph placement: `G_env` and `G_rt_env`.
- Authority state: not promoted.
- HyperAI app authority remains unchanged:
  - backend: `hyperai-user-control-system/backend/server.js` on port `5000`
  - frontend: static `dist-isolated` preview on port `4173`

## Observed Runtime

- Gateway: `ws://127.0.0.1:18789`
- Bind mode: loopback.
- Auth mode: token.
- Gateway process observed: PID `24712`, `node ...\openclaw\dist\index.js gateway --port 18789`.
- Canvas host: `http://127.0.0.1:18789/__openclaw__/canvas/`.
- Browser sidecar: `http://127.0.0.1:18791/`, token auth.
- Default agent: `main`.
- OpenClaw workspace: `C:\Users\pc\.openclaw\workspace`.
- Heartbeat: enabled every 30 minutes.
- Plugins observed: `acpx`, `browser`, `device-pair`, `phone-control`, `talk-voice`.
- Model observed: `ollama/all-minilm:22m`.

## Control Contract

Allowed through `tools/openclaw_control.py`:

- health probe
- status probe
- gateway status probe
- task inspection
- log tail
- browser-control readiness probe
- agent turn only after explicit user approval

Blocked by default:

- device pairing mutation
- phone control
- channel message sending
- cron job creation or mutation
- external delivery
- destructive config reset
- broad OpenClaw workspace mutation
- secret printing
- authority promotion by installation or reachability alone

Promotion rule:

- OpenClaw cannot become a HyperAI authority lane until fresh health proof exists, `phi_i(M)` is mapped, and a repo-governed execution contract defines proof, rollback, and stop rules.

## Current Blockers And Risks

- `main` agent bootstrap is pending.
- OpenClaw node service is missing.
- Bonjour gateway advertisement had probing/announcing warnings.
- One loopback gateway timeout was observed before later reachable status.
- Later wrapper verification saw intermittent gateway reachability: PID `24712` still listened on port `18789`, but `openclaw status` reported `gateway.reachable=false` with timeout.
- Native Windows mode is accepted for this first integration, but the WSL2 guidance remains recorded risk.

## Execution Rule

Use `tools/openclaw_control.py` for OpenClaw probes and bounded approved actions. The wrapper must redact secrets, write proof artifacts, and fail closed when the gateway is unreachable or auth warnings are present.
