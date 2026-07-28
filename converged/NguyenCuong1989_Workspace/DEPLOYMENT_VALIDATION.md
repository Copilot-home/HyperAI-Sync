# Deployment Validation

Status: **NOT VALIDATED / MUTATION BLOCKED** as of 2026-05-25.

This file records observed evidence only. A deployment has not been performed.

## Validation Matrix

| Check | Result | Evidence |
| --- | --- | --- |
| Active Python syntax parse | Pass | 30 `.py` files parsed without bytecode writes |
| API gateway in-process health | Partial pass | `/api/status` returned HTTP `200` |
| Telegram credential reachability | Partial pass | Telegram `getMe` returned the configured bot identity |
| Redis connectivity | Fail | No listener at `127.0.0.1:6379` |
| PostgreSQL connectivity | Fail | No response at `127.0.0.1:5432` |
| LakeData API health | Fail | HTTP `503` due to PostgreSQL absence |
| LakeData schema | Not found | No table-init or migration source found for `lakedata` |
| Compose parse | Pass | Dev compose resolves five declared services |
| Compose runtime | Not run | No FinalAI compose containers exist |
| FinalAI image build | Not run | `finalai:latest` absent |
| FinalAI SBOM | Not available | Image absent |
| FinalAI CVE gate | Not available | Image absent |
| Torch/StarCoder compatibility | Fail pending remediation | `torch==2.2.0` emits NumPy ABI warning with `numpy==2.0.2` |

## Security Blockers Before Enabling Telegram Runtime

- The bot command handler has no verified sender allowlist before accepting
  Python to execute.
- Module deployment derives a write path from user-supplied module names
  without a verified path boundary.

## Required Approval Checkpoint

No source or compose change, Docker build, service startup, volume inspection
requiring mutation, cleanup or dependency adjustment should proceed until the
user reviews this baseline and authorizes a specific remediation scope.
