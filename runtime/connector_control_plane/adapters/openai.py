import os
from typing import Any, Dict, List, Optional

import requests

from ..capability import Capability
from ..policy import KeyHygienePolicy
from ..state import ConnectorState, ConnectorSubstate
from .base import ConnectorControlAdapter


class OpenAIConnectorControlAdapter(ConnectorControlAdapter):
    connector_id = "openai"
    family = "A"
    schema_version = "2026-07-27"
    _base_admin_url = "https://api.openai.com/v1"

    def __init__(self, credential_ref: str, resolver: Any):
        super().__init__(credential_ref, resolver)
        self._admin_key = resolver.resolve(credential_ref)
        self._headers = {"Authorization": f"Bearer {self._admin_key}", "Content-Type": "application/json"}
        self._identity: Optional[Dict[str, Any]] = None

    def _get(self, path: str) -> Any:
        r = requests.get(f"{self._base_admin_url}/{path}", headers=self._headers, timeout=30)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, body: Dict[str, Any]) -> Any:
        r = requests.post(f"{self._base_admin_url}/{path}", headers=self._headers, json=body, timeout=30)
        r.raise_for_status()
        return r.json()

    def _delete(self, path: str) -> Any:
        r = requests.delete(f"{self._base_admin_url}/{path}", headers=self._headers, timeout=30)
        r.raise_for_status()
        return r.json() if r.text else {}

    def discover_identity(self) -> Dict[str, Any]:
        if self._identity is None:
            self._identity = self._get("organization/users")
        return self._identity

    def list_accounts(self) -> List[Dict[str, Any]]:
        return self._get("organization/projects").get("data", [])

    def list_workspaces(self) -> List[Dict[str, Any]]:
        return self.list_accounts()

    def list_roles(self) -> List[Dict[str, Any]]:
        return self._get("organization/roles").get("data", [])

    def inspect_permissions(self) -> Dict[str, Any]:
        return {"admin_keys": self._get("organization/admin_api_keys").get("data", [])}

    def discover_capabilities(self) -> List[Capability]:
        caps = [
            ("identity.list", "AVAILABLE"),
            ("project.list", "AVAILABLE"),
            ("key.list", "AVAILABLE"),
            ("key.delete.project", "AVAILABLE"),
            ("service_account.create", "AVAILABLE"),
            ("spend_limit.org.set", "AVAILABLE"),
            ("spend_alert.org.set", "AVAILABLE"),
            ("spend_limit.project.set", "AVAILABLE"),
            ("spend_alert.project.set", "AVAILABLE"),
            ("domain.list", "MANUAL_VERIFICATION_REQUIRED"),
            ("sso.configure", "MANUAL_VERIFICATION_REQUIRED"),
            ("agent.list", "MANUAL_VERIFICATION_REQUIRED"),
        ]
        return [Capability(connector_id=self.connector_id, operation=op, availability=avail, schema_version=self.schema_version) for op, avail in caps]

    def get_operation_schema(self, operation: str) -> Dict[str, Any]:
        schemas = {
            "service_account.create": {
                "method": "POST",
                "path": "organization/projects/{project_id}/service_accounts",
                "body": {"name": "string"},
            },
            "spend_limit.org.set": {
                "method": "POST",
                "path": "organization/spend_limit",
                "body": {"currency": "USD", "interval": "month", "threshold_amount": "integer (cents)"},
            },
            "spend_alert.org.set": {
                "method": "POST",
                "path": "organization/spend_alerts/{alert_id}",
                "body": {
                    "currency": "USD",
                    "interval": "month",
                    "threshold_amount": "integer (cents)",
                    "notification_channel": {"type": "email", "recipients": ["string"], "subject_prefix": "string"},
                },
            },
            "spend_limit.project.set": {
                "method": "POST",
                "path": "organization/projects/{project_id}/spend_limit",
                "body": {"currency": "USD", "interval": "month", "threshold_amount": "integer (cents)"},
            },
            "spend_alert.project.set": {
                "method": "POST",
                "path": "organization/projects/{project_id}/spend_alerts",
                "body": {
                    "currency": "USD",
                    "interval": "month",
                    "threshold_amount": "integer (cents)",
                    "notification_channel": {"type": "email", "recipients": ["string"], "subject_prefix": "string"},
                },
            },
            "key.delete.project": {
                "method": "DELETE",
                "path": "organization/projects/{project_id}/api_keys/{key_id}",
            },
        }
        return schemas.get(operation, {})

    def inspect_plan_constraints(self) -> List[str]:
        return []

    def list_resource_types(self) -> List[str]:
        return ["project", "user", "api_key", "service_account", "spend_limit", "spend_alert", "audit_log"]

    def list_resources(self, resource_type: str, cursor: Optional[str] = None) -> Dict[str, Any]:
        endpoints = {
            "project": "organization/projects",
            "user": "organization/users",
            "api_key": "organization/admin_api_keys",
            "spend_limit": "organization/spend_limit",
            "spend_alert": "organization/spend_alerts",
            "audit_log": "organization/audit_logs",
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
        try:
            return self._get("organization/spend_limit")
        except Exception:
            return {}

    def get_billing_state(self) -> Dict[str, Any]:
        return {
            "spend_limit": self.get_limits(),
            "spend_alerts": self._get("organization/spend_alerts"),
        }

    def preflight(self, action: Dict[str, Any]) -> Dict[str, Any]:
        policy_result = KeyHygienePolicy.check(action)
        if not policy_result.ok:
            return {
                "ok": False,
                "risk_class": "R5",
                "dry_run": True,
                "policy_result": policy_result.to_dict(),
            }
        return {
            "ok": True,
            "risk_class": action.get("risk_class", "R1"),
            "dry_run": True,
            "policy_result": policy_result.to_dict(),
        }

    def dry_run(self, action: Dict[str, Any]) -> Dict[str, Any]:
        preflight = self.preflight(action)
        if not preflight["ok"]:
            return preflight
        return {
            "ok": True,
            "action": action,
            "simulated": True,
            "policy_result": preflight.get("policy_result"),
        }

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

    def probe(self) -> Dict[str, Any]:
        try:
            self._get("organization/admin_api_keys")
            return {"ok": True, "state": ConnectorState.ORCHESTRATION_READY.value, "substate": ConnectorSubstate.NONE.value}
        except Exception as e:
            return {"ok": False, "state": ConnectorState.AUTH_FLOW_PRESENT.value, "substate": ConnectorSubstate.REQUIRES_REAUTHORIZATION.value, "error": str(e)}

    def reconcile(self) -> Dict[str, Any]:
        return self.probe()
