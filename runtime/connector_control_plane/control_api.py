import json
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException

from .adapters.notion import NotionConnectorControlAdapter
from .adapters.ollama import OllamaConnectorControlAdapter
from .adapters.openai import OpenAIConnectorControlAdapter
from .adapters.openrouter import OpenRouterConnectorControlAdapter
from .adapters.vercel import VercelConnectorControlAdapter
from .credential_resolver import CredentialResolver
from .policy import KeyHygienePolicy
from .receipt import EvidenceReceipt
from .registry import CapabilityRegistry

app = FastAPI(title="APΩ Connector Control Plane")

registry = CapabilityRegistry()


def register_default_adapters():
    resolver = CredentialResolver()
    defaults = [
        ("openai", lambda: OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", resolver)),
        ("ollama", lambda: OllamaConnectorControlAdapter()),
        ("openrouter", lambda: OpenRouterConnectorControlAdapter("env:OPENROUTER_API_KEY", resolver)),
        ("notion", lambda: NotionConnectorControlAdapter("env:NOTION_API_KEY", resolver)),
        ("vercel", lambda: VercelConnectorControlAdapter("env:VERCEL_TOKEN", resolver)),
    ]
    for connector_id, factory in defaults:
        try:
            adapter = factory()
            registry.register(adapter)
        except Exception as e:
            app.state.connection_errors = getattr(app.state, "connection_errors", {})
            app.state.connection_errors[connector_id] = str(e)


@app.on_event("startup")
def load_default_adapters():
    register_default_adapters()


@app.get("/control/connectors")
def list_connectors(family: str = None):
    return {"connectors": registry.list_connectors(family)}


@app.get("/control/families")
def list_families():
    return {"families": registry.list_families()}


@app.get("/control/capabilities")
def list_capabilities(connector_id: str = None, family: str = None):
    if connector_id:
        adapter = registry.get_adapter(connector_id)
        if not adapter:
            return {"error": "not_found"}
        return {"connector_id": connector_id, "capabilities": [c.__dict__ for c in adapter.discover_capabilities()]}
    if family:
        return {"family": family, "capabilities": [c.__dict__ for c in registry.resolve_capability("", family=family)]}
    return {"capabilities": []}


@app.get("/control/usage")
def usage(connector_id: str):
    adapter = registry.get_adapter(connector_id)
    if not adapter:
        return {"error": "not_found"}
    return adapter.get_usage()


@app.get("/control/billing")
def billing(connector_id: str):
    adapter = registry.get_adapter(connector_id)
    if not adapter:
        return {"error": "not_found"}
    return adapter.get_billing_state()


RECEIPT_DIR = Path(__file__).resolve().parent / "receipts"


def _record_receipt(
    connector_id: str,
    action: dict,
    policy_result: dict,
    risk_class: str = "R1",
    credential_ref: str = "",
) -> str:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_id = f"receipt-{uuid.uuid4().hex[:16]}"
    mission_id = action.get("mission_id") or receipt_id
    requested = action.get("operation", "unknown")
    effective = f"{connector_id}.{requested}"
    status = "POLICY_DECISION_REQUIRED" if not policy_result["ok"] else "POLICY_ADMISSIBLE"
    receipt = EvidenceReceipt.start(
        mission_id=mission_id,
        connector_id=connector_id,
        requested_action=requested,
        effective_action=effective,
        risk_class=risk_class,
        credential_ref=credential_ref or "env:UNKNOWN",
    )
    receipt.finish(status)
    receipt.approval_id = action.get("approval_id")
    receipt.resource_refs = action.get("resource_refs", [])
    payload = receipt.as_dict()
    payload["policy_result"] = policy_result
    (RECEIPT_DIR / f"{receipt_id}.json").write_text(
        json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8"
    )
    return receipt_id


@app.post("/runtime/actions/{connector_id}")
def execute_action(connector_id: str, action: dict):
    adapter = registry.get_adapter(connector_id)
    if not adapter:
        return {"error": "not_found"}

    policy_result = KeyHygienePolicy.check(action).to_dict()
    risk_class = "R5" if not policy_result["ok"] else action.get("risk_class", "R1")
    credential_ref = getattr(adapter, "credential_ref", "")
    receipt_id = _record_receipt(connector_id, action, policy_result, risk_class, credential_ref)

    if not policy_result["ok"]:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "policy_decision_required",
                "receipt_id": receipt_id,
                "policy_result": policy_result,
            },
        )

    result = adapter.preflight(action)
    return {
        "ok": result.get("ok", True),
        "receipt_id": receipt_id,
        "policy_result": policy_result,
        "adapter_result": result,
    }


@app.get("/events/subscriptions")
def list_subscriptions():
    return {"subscriptions": []}


@app.get("/evidence/receipts/{receipt_id}")
def get_receipt(receipt_id: str):
    path = RECEIPT_DIR / f"{receipt_id}.json"
    if not path.exists():
        return {"receipt_id": receipt_id, "status": "not_found"}
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("connector_control_plane.control_api:app", host="127.0.0.1", port=9012, reload=False)
