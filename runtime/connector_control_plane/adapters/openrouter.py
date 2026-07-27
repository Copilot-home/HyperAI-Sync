from typing import Any, Dict, List, Optional

import requests

from ..capability import Capability
from ..state import ConnectorState, ConnectorSubstate
from .base import ConnectorControlAdapter


class OpenRouterConnectorControlAdapter(ConnectorControlAdapter):
    connector_id = "openrouter"
    family = "A"
    schema_version = "2026-07-27"
    _base_url = "https://openrouter.ai/api/v1"

    def __init__(self, credential_ref: str, resolver: Any):
        super().__init__(credential_ref, resolver)
        self._api_key = resolver.resolve(credential_ref)
        self._headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}

    def _get(self, path: str) -> Any:
        r = requests.get(f"{self._base_url}/{path}", headers=self._headers, timeout=30)
        r.raise_for_status()
        return r.json()

    def probe(self) -> Dict[str, Any]:
        try:
            self._get("models")
            return {"ok": True, "state": ConnectorState.ORCHESTRATION_READY.value, "substate": ConnectorSubstate.NONE.value}
        except Exception as e:
            return {"ok": False, "state": ConnectorState.AUTH_FLOW_PRESENT.value, "substate": ConnectorSubstate.REQUIRES_REAUTHORIZATION.value, "error": str(e)}

    def discover_identity(self) -> Dict[str, Any]:
        try:
            credits = self._get("credits")
            return {"credits": credits}
        except Exception as e:
            return {"error": str(e)}

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
        avail = "AVAILABLE" if ready else "REQUIRES_REAUTHORIZATION"
        caps = [
            ("model.list", avail),
            ("model.chat", avail),
            ("credit.read", avail),
            ("usage.read", avail),
        ]
        return [Capability(connector_id=self.connector_id, operation=op, availability=avail, schema_version=self.schema_version) for op, avail in caps]

    def get_operation_schema(self, operation: str) -> Dict[str, Any]:
        schemas = {
            "model.list": {"method": "GET", "path": "models"},
            "model.chat": {"method": "POST", "path": "chat/completions", "body": {"model": "string", "messages": "array"}},
            "credit.read": {"method": "GET", "path": "credits"},
            "usage.read": {"method": "GET", "path": "usage"},
        }
        return schemas.get(operation, {})

    def inspect_plan_constraints(self) -> List[str]:
        return []

    def list_resource_types(self) -> List[str]:
        return ["model"]

    def list_resources(self, resource_type: str, cursor: Optional[str] = None) -> Dict[str, Any]:
        if resource_type == "model":
            return self._get("models")
        return {"object": "list", "data": []}

    def get_resource(self, resource_ref: str) -> Dict[str, Any]:
        return {}

    def get_usage(self) -> Dict[str, Any]:
        try:
            return self._get("usage")
        except Exception as e:
            return {"error": str(e)}

    def get_limits(self) -> Dict[str, Any]:
        try:
            return self._get("credits")
        except Exception as e:
            return {"error": str(e)}

    def get_billing_state(self) -> Dict[str, Any]:
        return {"credits": self.get_limits(), "usage": self.get_usage()}

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
