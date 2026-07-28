import unittest
from typing import Any

from connector_control_plane.adapters.openai import OpenAIConnectorControlAdapter
from connector_control_plane.capability import Capability
from connector_control_plane.credential_resolver import CredentialResolver
from connector_control_plane.receipt import EvidenceReceipt
from connector_control_plane.registry import CapabilityRegistry
from connector_control_plane.state import ConnectorState, ConnectorSubstate


class FakeResolver:
    def __init__(self, values=None):
        self.values = values or {}

    def resolve(self, credential_ref: str) -> str:
        key = credential_ref.split(":", 1)[1]
        return self.values.get(credential_ref, "sk-fake")

    def resolve_optional(self, credential_ref: str) -> str:
        return self.resolve(credential_ref)


class TestEvidenceReceipt(unittest.TestCase):
    def test_receipt_hash(self):
        r = EvidenceReceipt.start("m1", "openai", "key.list", "openai.key.list", "R1", "env:OPENAI_ADMIN_KEY")
        r.finish("VERIFIED", "op-1")
        self.assertEqual(r.status, "VERIFIED")
        self.assertIsNotNone(r.evidence_hash)
        self.assertIsNotNone(r.finished_at)


class TestCapabilityRegistry(unittest.TestCase):
    def test_register_and_resolve(self):
        class DummyAdapter:
            connector_id = "x"
            family = "A"

            def discover_capabilities(self):
                return [Capability("x", "op1", "AVAILABLE")]

        registry = CapabilityRegistry()
        registry.register(DummyAdapter())
        self.assertEqual(registry.list_connectors(), ["x"])
        caps = registry.resolve_capability("op1")
        self.assertEqual(len(caps), 1)


class TestOpenAIAdapter(unittest.TestCase):
    def test_preflight_dry_run(self):
        adapter = OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", FakeResolver())
        action = {"operation": "key.list", "risk_class": "R1"}
        self.assertTrue(adapter.preflight(action)["ok"])
        self.assertTrue(adapter.dry_run(action)["ok"])

    def test_state_enums(self):
        self.assertEqual(ConnectorState.ORCHESTRATION_READY.value, "ORCHESTRATION_READY")
        self.assertEqual(ConnectorSubstate.MANUAL_VERIFICATION_REQUIRED.value, "MANUAL_VERIFICATION_REQUIRED")

    def test_key_hygiene_guardrail_denies_approve_state_without_expiry(self):
        adapter = OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", FakeResolver())
        action = {
            "operation": "approve_state",
            "resource_type": "api_key",
            "resource": {"id": "key-1", "expires_at": None},
        }
        result = adapter.preflight(action)
        self.assertFalse(result["ok"])
        self.assertEqual(result["risk_class"], "R5")
        self.assertEqual(result["policy_result"]["status"], "POLICY_DECISION_REQUIRED")
        self.assertEqual(
            result["policy_result"]["required_decision"],
            "set_expiry_or_rotation_schedule",
        )

    def test_key_hygiene_guardrail_allows_with_policy_decision(self):
        adapter = OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", FakeResolver())
        action = {
            "operation": "approve_state",
            "resource_type": "api_key",
            "resource": {"id": "key-1", "expires_at": None},
            "policy_decision": "set_expiry_or_rotation_schedule",
        }
        result = adapter.preflight(action)
        self.assertTrue(result["ok"])
        self.assertEqual(result["policy_result"]["status"], "POLICY_ADMISSIBLE")

    def test_key_hygiene_guardrail_ignores_non_approve_state(self):
        adapter = OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", FakeResolver())
        action = {
            "operation": "key.list",
            "resource_type": "api_key",
            "resource": {"id": "key-1", "expires_at": None},
        }
        result = adapter.preflight(action)
        self.assertTrue(result["ok"])

    def test_key_hygiene_guardrail_ignores_non_api_key_resource(self):
        adapter = OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", FakeResolver())
        action = {
            "operation": "approve_state",
            "resource_type": "project",
            "resource": {"id": "proj-1"},
        }
        result = adapter.preflight(action)
        self.assertTrue(result["ok"])

    def test_key_hygiene_guardrail_allows_when_expiry_present(self):
        adapter = OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", FakeResolver())
        action = {
            "operation": "approve_state",
            "resource_type": "api_key",
            "resource": {"id": "key-1", "expires_at": "2026-12-31T23:59:59Z"},
        }
        result = adapter.preflight(action)
        self.assertTrue(result["ok"])


class TestCredentialResolver(unittest.TestCase):
    def test_env_scheme(self):
        import os
        os.environ["TEST_FAKE_KEY"] = "abc"
        resolver = CredentialResolver(source=None)
        value = resolver.resolve("env:TEST_FAKE_KEY")
        self.assertEqual(value, "abc")


if __name__ == "__main__":
    unittest.main()
