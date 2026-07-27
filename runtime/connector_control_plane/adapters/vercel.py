from typing import Any, Dict, List, Optional

import requests

from ..capability import Capability
from ..state import ConnectorState, ConnectorSubstate
from .base import ConnectorControlAdapter


class VercelConnectorControlAdapter(ConnectorControlAdapter):
    connector_id = "vercel"
    family = "C"
    schema_version = "2026-07-27"
    _base_url = "https://api.vercel.com"

    def __init__(self, credential_ref: str, resolver: Any):
        super().__init__(credential_ref, resolver)
        self._token = resolver.resolve(credential_ref)
        self._headers = {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}

    def _get(self, path: str) -> Any:
        r = requests.get(f"{self._base_url}/{path}", headers=self._headers, timeout=30)
        r.raise_for_status()
        return r.json()

    def probe(self) -> Dict[str, Any]:
        try:
            self._get("v2/user")
            return {"ok": True, "state": ConnectorState.ORCHESTRATION_READY.value, "substate": ConnectorSubstate.NONE.value}
        except Exception as e:
            return {"ok": False, "state": ConnectorState.AUTH_FLOW_PRESENT.value, "substate": ConnectorSubstate.REQUIRES_REAUTHORIZATION.value, "error": str(e)}

    def discover_identity(self) -> Dict[str, Any]:
        try:
            return self._get("v2/user")
        except Exception as e:
            return {"error": str(e)}

    def list_accounts(self) -> List[Dict[str, Any]]:
        return []

    def list_workspaces(self) -> List[Dict[str, Any]]:
        try:
            return self._get("v1/teams").get("teams", [])
        except Exception:
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
            ("user.read", avail),
            ("team.list", avail),
            ("project.list", avail),
            ("project.read", avail),
            ("deployment.list", avail),
            ("domain.list", avail),
        ]
        return [Capability(connector_id=self.connector_id, operation=op, availability=avail, schema_version=self.schema_version) for op, avail in caps]

    def get_operation_schema(self, operation: str) -> Dict[str, Any]:
        schemas = {
            "user.read": {"method": "GET", "path": "v2/user"},
            "team.list": {"method": "GET", "path": "v1/teams"},
            "project.list": {"method": "GET", "path": "v9/projects"},
            "project.read": {"method": "GET", "path": "v9/projects/{projectId}"},
            "deployment.list": {"method": "GET", "path": "v6/deployments"},
            "domain.list": {"method": "GET", "path": "v5/domains"},
        }
        return schemas.get(operation, {})

    def inspect_plan_constraints(self) -> List[str]:
        return []

    def list_resource_types(self) -> List[str]:
        return ["team", "project", "deployment", "domain"]

    def list_resources(self, resource_type: str, cursor: Optional[str] = None) -> Dict[str, Any]:
        endpoints = {
            "team": "v1/teams",
            "project": "v9/projects",
            "deployment": "v6/deployments",
            "domain": "v5/domains",
        }
        path = endpoints.get(resource_type, "")
        if not path:
            return {"object": "list", "data": []}
        return self._get(path)

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
