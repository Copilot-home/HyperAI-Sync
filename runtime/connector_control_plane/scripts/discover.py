import argparse
import json
import os
import sys

RUNTIME_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(RUNTIME_ROOT)
sys.path.insert(0, RUNTIME_ROOT)
sys.path.insert(0, REPO_ROOT)

from connector_control_plane.adapters.notion import NotionConnectorControlAdapter
from connector_control_plane.adapters.ollama import OllamaConnectorControlAdapter
from connector_control_plane.adapters.openai import OpenAIConnectorControlAdapter
from connector_control_plane.adapters.openrouter import OpenRouterConnectorControlAdapter
from connector_control_plane.adapters.vercel import VercelConnectorControlAdapter
from connector_control_plane.credential_resolver import CredentialResolver
from connector_control_plane.registry import CapabilityRegistry


def build_adapter(connector: str, resolver: CredentialResolver):
    if connector == "openai":
        return OpenAIConnectorControlAdapter("env:OPENAI_ADMIN_KEY", resolver)
    if connector == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        return OllamaConnectorControlAdapter(None, None, host=host)
    if connector == "openrouter":
        return OpenRouterConnectorControlAdapter("env:OPENROUTER_API_KEY", resolver)
    if connector == "notion":
        return NotionConnectorControlAdapter("env:NOTION_API_KEY", resolver)
    if connector == "vercel":
        return VercelConnectorControlAdapter("env:VERCEL_TOKEN", resolver)
    raise ValueError(f"unsupported connector: {connector}")


def probe_one(adapter):
    return {
        "connector_id": adapter.connector_id,
        "family": adapter.family,
        "probe": adapter.probe(),
        "capabilities": [c.__dict__ for c in adapter.discover_capabilities()],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("connector", choices=["openai", "ollama", "openrouter", "notion", "vercel", "all"])
    parser.add_argument("--full", action="store_true", help="include identity, accounts, billing")
    args = parser.parse_args()

    resolver = CredentialResolver()
    targets = ["openai", "ollama", "openrouter", "notion", "vercel"] if args.connector == "all" else [args.connector]

    registry = CapabilityRegistry()
    adapters = [build_adapter(t, resolver) for t in targets]
    for adapter in adapters:
        registry.register(adapter)

    reports = []
    for adapter in adapters:
        report = probe_one(adapter)
        if args.full and report["probe"]["ok"]:
            report["identity"] = adapter.discover_identity()
            report["accounts"] = adapter.list_accounts()
            report["workspaces"] = adapter.list_workspaces()
            report["billing"] = adapter.get_billing_state()
        reports.append(report)

    if len(reports) == 1:
        print(json.dumps(reports[0], indent=2, default=str, ensure_ascii=False))
    else:
        print(json.dumps({"connectors": reports}, indent=2, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
