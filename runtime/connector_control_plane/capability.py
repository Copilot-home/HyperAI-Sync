from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Capability:
    connector_id: str
    operation: str
    availability: str
    schema_version: str = ""
    last_probe_at: Optional[str] = None
    plan_constraints: List[str] = field(default_factory=list)
    permission_snapshot: Dict[str, Any] = field(default_factory=dict)
