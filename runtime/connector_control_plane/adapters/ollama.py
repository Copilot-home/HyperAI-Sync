from typing import Any, Dict, List, Optional

import requests

from ..capability import Capability
from ..state import ConnectorState, ConnectorSubstate
from .base import ConnectorControlAdapter


class OllamaConnectorControlAdapter(ConnectorControlAdapter):
    connector_id = "ollama"
    family = "A"
    schema_version = "2026-07-27"

    def __init__(self, credential_ref: Optional[str] = None, resolver: Any = None, host: str = "http://127.0.0.1:11434"):
        super().__init__(credential_ref, resolver)
        self._host = host
        self._headers = {}
        if credential_ref and resolver:
            key = resolver.resolve_optional(credential_ref)
            if key:
                self._headers["Authorization"] = f"Bearer {key}"

    def _get(self, path: str) -> Any:
        r = requests.get(f"{self._host}/{path}", headers=self._headers, timeout=10)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, body: Dict[str, Any]) -> Any:
        r = requests.post(f"{self._host}/{path}", headers=self._headers, json=body, timeout=30)
        r.raise_for_status()
        return r.json()

    def probe(self) -> Dict[str, Any]:
        try:
            self._get("api/tags")
            return {"ok": True, "state": ConnectorState.ORCHESTRATION_READY.value, "substate": ConnectorSubstate.NONE.value}
        except requests.exceptions.ConnectionError:
            return {"ok": False, "state": ConnectorState.AUTH_FLOW_PRESENT.value, "substate": ConnectorSubstate.ACCOUNT_NOT_CREATED.value, "error": "ollama not reachable"}
        except Exception as e:
            return {"ok": False, "state": ConnectorState.AUTH_FLOW_PRESENT.value, "substate": ConnectorSubstate.REQUIRES_REAUTHORIZATION.value, "error": str(e)}

    def discover_identity(self) -> Dict[str, Any]:
        return {"host": self._host}

    def list_accounts(self) -> List[Dict[str, Any]]:
        return []

    def list_workspaces(self) -> List[Dict[str, Any]]:
        return []

    def list_roles(self) -> List[Dict[str, Any]]:
        return []

    def inspect_permissions(self) -> Dict[str, Any]:
        return {}

    def discover_capabilities(self) -> List[Capability]:
        status = self.probe()
        ready = status["ok"]
        avail = "AVAILABLE" if ready else "ACCOUNT_NOT_CREATED"
        caps = [
            ("model.list", avail),
            ("model.pull", avail),
            ("model.delete", avail),
            ("generate", avail),
            ("embed", avail),
            ("ps", avail),
        ]
        return [Capability(connector_id=self.connector_id, operation=op, availability=avail, schema_version=self.schema_version) for op, avail in caps]

    def get_operation_schema(self, operation: str) -> Dict[str, Any]:
        schemas = {
            "model.list": {"method": "GET", "path": "api/tags"},
            "generate": {"method": "POST", "path": "api/generate", "body": {"model": "string", "prompt": "string"}},
        }
        return schemas.get(operation, {})

    def inspect_plan_constraints(self) -> List[str]:
        return []

    def list_resource_types(self) -> List[str]:
        return ["model"]

    def list_resources(self, resource_type: str, cursor: Optional[str] = None) -> Dict[str, Any]:
        if resource_type == "model":
            return self._get("api/tags")
        return {"object": "list", "data": []}

    def get_resource(self, resource_ref: str) -> Dict[str, Any]:
        return {}

    def get_usage(self) -> Dict[str, Any]:
        return {}

    def get_limits(self) -> Dict[str, Any]:
        return {}

    def get_billing_state(self) -> Dict[str, Any]:
        return {}

    def preflight(self, action: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "risk_class": action.get("risk_class", "R1"), "dry_run": True}

    def dry_run(self, action: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "action": action, "simulated": True}

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("use provider-specific runner or extend adapter")

    def verify(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "receipt": receipt}

    def get_event_cursor(self) -> Optional[str]:
        return None

    def poll_events(self, cursor: Optional[str] = None) -> Dict[str, Any]:
        return {"cursor": cursor, "events": []}

    def subscribe_events(self, callback_ref: str) -> Dict[str, Any]:
        return {"subscribed": False, "reason": "webhooks not configured"}

    def rollback(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": False, "reason": "not_implemented"}

    def compensate(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": False, "reason": "not_implemented"}

    def reconcile(self) -> Dict[str, Any]:
        return self.probe()
