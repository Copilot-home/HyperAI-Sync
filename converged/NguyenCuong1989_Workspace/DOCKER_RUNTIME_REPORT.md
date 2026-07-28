# Docker Runtime Report

Status: read-only audit, 2026-05-25.

## Actual Docker State

| Artifact | Observed State | Provenance/Relation To FinalAI |
| --- | --- | --- |
| `welcome-to-docker:latest` | Image present; container `zealous_agnesi` running; no mounts; no published host port | Source retained in Archive; upstream remote is `docker/welcome-to-docker`; not FinalAI |
| `langchain/langchain:latest` | Image present; container `friendly_galois` exited; no mounts | Docker Scout provenance is upstream LangChain; not referenced by FinalAI source or compose |
| `finalai:latest` | Not present | Declared by FinalAI compose, never verified as built |
| `redis:7-alpine` | Not present | Declared FinalAI runtime dependency |
| `postgres:14` | Not present | Declared FinalAI runtime dependency |

## CVE Evidence

`docker scout cves --only-severity critical langchain/langchain:latest`
confirmed `12 Critical` vulnerabilities across 10 packages. The affected image
is an upstream LangChain artifact and is not evidence about the unbuilt
FinalAI image.

No FinalAI SBOM or FinalAI CVE result exists because no FinalAI image currently
exists in the Docker engine.

## Compose Reconciliation

The active compose file resolves to:

- `finalai_runtime` built from the FinalAI Dockerfile
- `api_gateway` built from the same Dockerfile, port `5050`
- `lakedata_api` built from the same Dockerfile, port `5051`
- `redis:7-alpine`, port `6379`
- `postgres:14`, port `5432`

Observed gaps:

- No compose container is running.
- No Redis/PostgreSQL listeners are available.
- No named volumes are declared for Redis or PostgreSQL persistence.
- `.env` is imported into all three app services; compose rendering shows the
  Telegram credential would be exposed to API/LakeData containers as well as
  the Telegram runtime.

## Cleanup Gate

Six anonymous Docker volumes exist and are not mounted by the two current
containers. Their originating workload and stored contents have not been
identified. No volume or container cleanup is authorized without inspection
and human approval.
