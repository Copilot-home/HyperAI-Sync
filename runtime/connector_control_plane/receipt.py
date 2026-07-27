import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class EvidenceReceipt:
    mission_id: str
    connector_id: str
    requested_action: str
    effective_action: str
    risk_class: str
    status: str
    account_id: Optional[str] = None
    workspace_id: Optional[str] = None
    resource_refs: List[str] = field(default_factory=list)
    policy_generation: int = 0
    approval_id: Optional[str] = None
    credential_ref_hash: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    external_operation_id: Optional[str] = None
    rollback: Dict[str, Any] = field(default_factory=dict)
    cost: Optional[Dict[str, Any]] = None
    evidence_hash: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "connector_id": self.connector_id,
            "account_id": self.account_id,
            "workspace_id": self.workspace_id,
            "requested_action": self.requested_action,
            "effective_action": self.effective_action,
            "resource_refs": self.resource_refs,
            "risk_class": self.risk_class,
            "policy_generation": self.policy_generation,
            "approval_id": self.approval_id,
            "credential_ref_hash": self.credential_ref_hash,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "external_operation_id": self.external_operation_id,
            "status": self.status,
            "rollback": self.rollback,
            "cost": self.cost,
            "evidence_hash": self.evidence_hash,
        }

    def finish(self, status: str, external_operation_id: Optional[str] = None):
        self.finished_at = datetime.now(timezone.utc).isoformat()
        self.status = status
        self.external_operation_id = external_operation_id or self.external_operation_id
        payload = json.dumps(self.as_dict(), sort_keys=True, default=str).encode()
        self.evidence_hash = hashlib.sha256(payload).hexdigest()

    @classmethod
    def start(cls, mission_id: str, connector_id: str, requested_action: str, effective_action: str, risk_class: str, credential_ref: str) -> "EvidenceReceipt":
        started = datetime.now(timezone.utc).isoformat()
        ref_hash = hashlib.sha256(credential_ref.encode()).hexdigest()
        return cls(
            mission_id=mission_id,
            connector_id=connector_id,
            requested_action=requested_action,
            effective_action=effective_action,
            risk_class=risk_class,
            status="PENDING",
            started_at=started,
            credential_ref_hash=ref_hash,
        )
