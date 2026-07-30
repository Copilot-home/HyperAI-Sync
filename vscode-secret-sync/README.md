# @hyperai/vscode-secret-sync

APO-aligned cross-instance SecretStorage sync for VS Code, Cursor, Trae and other VS Code forks.

## What it does

VS Code `ExtensionContext.secrets` is per-extension and **not synced** across machines or even across different VS Code editors (Cursor, Trae, Insiders, etc.) on the same machine.

This package provides `APOSecretStorageSync`, a `SecretStorage`-shaped store that mirrors secrets into an AES-256-GCM encrypted canonical vault under `~/.axcanon/memory/secrets/vault.enc`. The master key is stored in the OS keyring (macOS `security`/`keytar` first, protected `0600` key file as fallback).

## API

```typescript
import { APOSecretStorageSync } from "@hyperai/vscode-secret-sync";

const secrets = await APOSecretStorageSync.create();

await secrets.store("openai.api_key", process.env.OPENAI_API_KEY || "");
const key = await secrets.get("openai.api_key");
await secrets.delete("openai.api_key");
const allKeys = await secrets.keys();

secrets.onDidChange((e) => {
  console.log(`secret changed: ${e.key}`);
});
```

To react to changes written by other processes, use the watcher variant:

```typescript
const secrets = await APOSecretStorageSyncWithWatcher.create();
```

## Python adapter

For Python-based APO tools use `HyperAI-Sync/tools/hyperai_vscode_secret_sync.py`:

```bash
python3 /Users/andy/HyperAI-Sync/tools/hyperai_vscode_secret_sync.py set openai.api_key "$OPENAI_API_KEY"
python3 /Users/andy/HyperAI-Sync/tools/hyperai_vscode_secret_sync.py get openai.api_key
python3 /Users/andy/HyperAI-Sync/tools/hyperai_vscode_secret_sync.py list
python3 /Users/andy/HyperAI-Sync/tools/hyperai_vscode_secret_sync.py export --format dotenv
```

## Environment knobs

- `AX_APO_CANON_LIBRARY` — used to locate the APO canon directory; the vault lives in its sibling `memory/secrets/`.
- `AX_APO_IDENTITY` / `AX_SECRET_VAULT_SERVICE` — keychain service name.
- `AX_APO_USER` — keychain account name.
- `AX_SECRET_KEY_FILE` — explicit path to a protected master key file.
- `AX_SECRET_KEY_BASE64` — explicit base64-encoded 32-byte master key.

## Security

- Master key: 32 random bytes, stored in OS keyring or a `0600` fallback file.
- Vault: AES-256-GCM, format `nonce (12) || ciphertext || tag (16)`.
- Plaintext secrets never live as project artifacts; only the encrypted vault and keyring entry are persisted.
