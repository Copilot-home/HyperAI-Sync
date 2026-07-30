> Source: live probe, 2026-07-28.
> Preserved as-is; do not normalize against external schemas.
> Author: Alpha_Prime_Omega

# NotebookLM Enterprise API Probe

## Endpoint

```
https://us-discoveryengine.googleapis.com/v1alpha/projects/171781820082/locations/us/notebooks
```

## Project

- `antigravity-apo-4287`
- project number: `171781820082`
- `discoveryengine.googleapis.com`: enabled

## Auth

- `gcloud auth print-access-token` with Drive scope.
- Token accepted by API.

## Result

```json
{
  "error": {
    "code": 400,
    "message": "User must be assigned a license in order to be granted access, the license must have a subscription tier that is not unspecified. Required license for this request is SUBSCRIPTION_TIER_NOTEBOOK_LM_INTERACT.",
    "status": "FAILED_PRECONDITION"
  }
}
```

## Meaning

- The API is reachable and auth works.
- The project does **not** currently have a Gemini Notebook Enterprise license.
- A paid subscription / license assignment is required before `notebooks.create`, `sources.create`, or mind-map generation can be called programmatically.

## Scaffold

- `~/HyperAI-Sync/tools/hyperai_notebooklm_enterprise.py` created.
- It can check license, create notebook, and add the six Drive sources once a license is assigned.
- Activation gate: `AX_NOTEBOOKLM_ENTERPRISE_ENABLED=1`.
