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


class TestCredentialResolver(unittest.TestCase):
    def test_env_scheme(self):
        import os
        os.environ["TEST_FAKE_KEY"] = "abc"
        resolver = CredentialResolver(source=None)
        value = resolver.resolve("env:TEST_FAKE_KEY")
        self.assertEqual(value, "abc")


if __name__ == "__main__":
    unittest.main()
