from fastapi import FastAPI

from .adapters.notion import NotionConnectorControlAdapter
from .adapters.ollama import OllamaConnectorControlAdapter
from .adapters.openai import OpenAIConnectorControlAdapter
from .adapters.openrouter import OpenRouterConnectorControlAdapter
from .adapters.vercel import VercelConnectorControlAdapter
from .credential_resolver import CredentialResolver
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


@app.post("/runtime/actions/{connector_id}")
def execute_action(connector_id: str, action: dict):
    adapter = registry.get_adapter(connector_id)
    if not adapter:
        return {"error": "not_found"}
    return adapter.preflight(action)


@app.get("/events/subscriptions")
def list_subscriptions():
    return {"subscriptions": []}


@app.get("/evidence/receipts/{receipt_id}")
def get_receipt(receipt_id: str):
    return {"receipt_id": receipt_id, "status": "not_implemented"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("connector_control_plane.control_api:app", host="127.0.0.1", port=9012, reload=False)
