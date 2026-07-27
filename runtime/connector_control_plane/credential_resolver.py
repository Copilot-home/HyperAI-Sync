import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import hyperai_credentials_loader as cred_loader


class CredentialResolver:
    def __init__(self, source: Optional[Path] = None):
        self._source = source or Path.home() / ".config" / "hyperai" / "credentials.env"
        self._cache: Optional[Dict[str, str]] = None

    def _load(self) -> Dict[str, str]:
        if self._cache is None:
            if self._source.exists():
                self._cache = cred_loader.load_env_file(self._source)
            else:
                self._cache = {}
        return self._cache

    def resolve(self, credential_ref: str) -> str:
        if credential_ref.startswith("env:"):
            key = credential_ref.split(":", 1)[1]
            value = os.environ.get(key)
            if value:
                return value
            value = self._load().get(key)
            if not value:
                raise ValueError(f"credential not found: {key}")
            return value
        if credential_ref.startswith("vault:"):
            raise NotImplementedError("vault resolver not implemented")
        raise ValueError(f"unsupported credential ref scheme: {credential_ref}")

    def resolve_optional(self, credential_ref: Optional[str]) -> Optional[str]:
        if not credential_ref:
            return None
        try:
            return self.resolve(credential_ref)
        except Exception:
            return None
