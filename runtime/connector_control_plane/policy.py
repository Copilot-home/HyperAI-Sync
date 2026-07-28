from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class PolicyDecision:
    """Canonical policy decisions that can be attached to an action."""

    SET_EXPIRY_OR_ROTATION_SCHEDULE = "set_expiry_or_rotation_schedule"


@dataclass
class PolicyResult:
    """Result of a policy guardrail check."""

    ok: bool
    reason: str = ""
    required_decision: Optional[str] = None
    status: str = "POLICY_ADMISSIBLE"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "reason": self.reason,
            "required_decision": self.required_decision,
            "status": self.status,
            "metadata": self.metadata,
        }


class KeyHygienePolicy:
    """
    Guardrail: API keys without an expiry date cannot be approved for active use
    unless the caller explicitly attaches a policy decision to set an expiry or
    rotation schedule.

    This implements the APΩ control-plane rule:

        if key.expires_at is None and action == "approve_state":
            require policy_decision == "set_expiry_or_rotation_schedule"
    """

    @classmethod
    def check(cls, action: Dict[str, Any]) -> PolicyResult:
        operation = action.get("operation", "")
        if operation != "approve_state":
            return PolicyResult(ok=True)

        resource_type = action.get("resource_type", "")
        if resource_type != "api_key":
            return PolicyResult(ok=True)

        resource = action.get("resource") or action.get("key") or {}
        if isinstance(resource, dict):
            expires_at = resource.get("expires_at")
        else:
            expires_at = action.get("expires_at")

        if expires_at is not None:
            return PolicyResult(ok=True)

        policy_decision = action.get("policy_decision")
        if not policy_decision and "proof_req" in action:
            policy_decision = action["proof_req"].get("policy_decision")

        if policy_decision == PolicyDecision.SET_EXPIRY_OR_ROTATION_SCHEDULE:
            return PolicyResult(
                ok=True,
                status="POLICY_ADMISSIBLE",
                metadata={"decision": policy_decision},
            )

        return PolicyResult(
            ok=False,
            status="POLICY_DECISION_REQUIRED",
            reason=(
                "key without expiry cannot be approved without policy_decision="
                f"'{PolicyDecision.SET_EXPIRY_OR_ROTATION_SCHEDULE}'"
            ),
            required_decision=PolicyDecision.SET_EXPIRY_OR_ROTATION_SCHEDULE,
            metadata={"expires_at": expires_at, "action": operation},
        )
