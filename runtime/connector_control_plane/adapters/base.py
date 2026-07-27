from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ConnectorControlAdapter(ABC):
    connector_id: str = ""
    family: str = ""
    schema_version: str = ""

    def __init__(self, credential_ref: Optional[str] = None, resolver: Optional[Any] = None):
        self.credential_ref = credential_ref or ""
        self.resolver = resolver

    @abstractmethod
    def discover_identity(self) -> Dict[str, Any]: ...

    @abstractmethod
    def list_accounts(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def list_workspaces(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def list_roles(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def inspect_permissions(self) -> Dict[str, Any]: ...

    @abstractmethod
    def discover_capabilities(self) -> List[Any]: ...

    @abstractmethod
    def get_operation_schema(self, operation: str) -> Dict[str, Any]: ...

    @abstractmethod
    def inspect_plan_constraints(self) -> List[str]: ...

    @abstractmethod
    def list_resource_types(self) -> List[str]: ...

    @abstractmethod
    def list_resources(self, resource_type: str, cursor: Optional[str] = None) -> Dict[str, Any]: ...

    @abstractmethod
    def get_resource(self, resource_ref: str) -> Dict[str, Any]: ...

    @abstractmethod
    def get_usage(self) -> Dict[str, Any]: ...

    @abstractmethod
    def get_limits(self) -> Dict[str, Any]: ...

    @abstractmethod
    def get_billing_state(self) -> Dict[str, Any]: ...

    @abstractmethod
    def preflight(self, action: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def dry_run(self, action: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def verify(self, receipt: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def get_event_cursor(self) -> Optional[str]: ...

    @abstractmethod
    def poll_events(self, cursor: Optional[str] = None) -> Dict[str, Any]: ...

    @abstractmethod
    def subscribe_events(self, callback_ref: str) -> Dict[str, Any]: ...

    @abstractmethod
    def rollback(self, receipt: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def compensate(self, receipt: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def probe(self) -> Dict[str, Any]: ...

    @abstractmethod
    def reconcile(self) -> Dict[str, Any]: ...
