from typing import Any, Dict, List, Optional

from .adapters.base import ConnectorControlAdapter
from .capability import Capability


class CapabilityRegistry:
    def __init__(self):
        self._adapters: Dict[str, ConnectorControlAdapter] = {}
        self._families: Dict[str, List[str]] = {}

    def register(self, adapter: ConnectorControlAdapter) -> None:
        self._adapters[adapter.connector_id] = adapter
        self._families.setdefault(adapter.family, []).append(adapter.connector_id)

    def get_adapter(self, connector_id: str) -> Optional[ConnectorControlAdapter]:
        return self._adapters.get(connector_id)

    def list_families(self) -> List[str]:
        return list(self._families.keys())

    def list_connectors(self, family: Optional[str] = None) -> List[str]:
        if family:
            return list(self._families.get(family, []))
        return list(self._adapters.keys())

    def resolve_capability(self, requested_action: str, family: Optional[str] = None) -> List[Capability]:
        candidates = []
        for cid in self.list_connectors(family):
            adapter = self._adapters[cid]
            for cap in adapter.discover_capabilities():
                if cap.operation == requested_action:
                    candidates.append(cap)
        return candidates
