// =============================================================================
// PROJECT: CANON-TO-SYSTEM DETERMINISTIC PROJECTION
// METHOD: D&R PROTOCOL (CLOSED)
//
// ORIGINATOR / CREATOR:
//   alpha_prime_omega
//
// LEGAL ONTOLOGY:
//   This source file is a deterministic projection of a closed Canon.
//   Removal or alteration of this header voids legal and ontological validity.
//
// STATUS:
//   GENERATED — NON-AUTONOMOUS — NON-OWNERLESS
//
// TRACEABILITY:
//   Canon -> COG -> Projection(Π) -> Artifact
//
// =============================================================================

/**
 * APO-aligned cross-instance SecretStorage sync for VS Code and forks.
 *
 * Implements a storage utility matching the VS Code `SecretStorage` shape,
 * backed by an AES-256-GCM encrypted canonical vault and a platform-specific
 * master key (macOS keychain via `security`, optional `keytar`, or a fallback
 * `0600` key file when the canon environment mandates it).
 *
 * Secrets are NOT exposed as project artifacts. The master key lives in the OS
 * keyring or in the protected APO memory directory. The encrypted vault lives
 * at `~/.axcanon/memory/secrets/vault.enc`.
 */

import { createCipheriv, createDecipheriv, randomBytes } from "crypto";
import { execFile } from "child_process";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  statSync,
  Stats,
  unlinkSync,
  watchFile,
  writeFileSync,
} from "fs";
import { homedir } from "os";
import { dirname, join } from "path";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface APOSecretStorageChangeEvent {
  key: string;
}

export type APOSecretStorageEvent = (
  listener: (e: APOSecretStorageChangeEvent) => any,
  thisArgs?: any,
  disposables?: { dispose(): any }[]
) => { dispose(): void };

export interface APOSecretStorage {
  get(key: string): Promise<string | undefined>;
  store(key: string, value: string): Promise<void>;
  delete(key: string): Promise<void>;
  keys(): Promise<string[]>;
  onDidChange: APOSecretStorageEvent;
}

interface VaultPayload {
  schema_version: string;
  updated_at: string;
  records: Record<string, string>;
}

interface Disposable {
  dispose(): void;
}

// ---------------------------------------------------------------------------
// Master key resolution
// ---------------------------------------------------------------------------

function canonicalSecretsDir(): string {
  const axcanon = process.env.AX_APO_CANON_LIBRARY
    ? dirname(process.env.AX_APO_CANON_LIBRARY)
    : undefined;
  const base = axcanon
    ? join(axcanon, "..", "memory")
    : join(homedir(), ".axcanon", "memory");
  const dir = join(base, "secrets");
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  return dir;
}

function keychainService(): string {
  return (
    process.env.AX_APO_IDENTITY ||
    process.env.AX_SECRET_VAULT_SERVICE ||
    "com.hyperai.apo.vscode-secrets"
  );
}

function keychainAccount(): string {
  return process.env.AX_APO_USER || process.env.USER || "apo";
}

function fallbackKeyFile(): string {
  if (process.env.AX_SECRET_KEY_FILE) return process.env.AX_SECRET_KEY_FILE;
  return join(canonicalSecretsDir(), "master.key");
}

async function getKeytar(): Promise<any | undefined> {
  try {
    const keytar = await import("keytar");
    return keytar.default || keytar;
  } catch {
    return undefined;
  }
}

async function keychainGetPassword(): Promise<string | undefined> {
  const kt = await getKeytar();
  if (kt) {
    return kt.getPassword(keychainService(), keychainAccount());
  }

  if (process.platform !== "darwin") return undefined;

  try {
    const { stdout } = await execFileAsync("security", [
      "find-generic-password",
      "-s",
      keychainService(),
      "-a",
      keychainAccount(),
      "-w",
    ]);
    return stdout.trim() || undefined;
  } catch {
    return undefined;
  }
}

async function keychainSetPassword(password: string): Promise<void> {
  const kt = await getKeytar();
  if (kt) {
    await kt.setPassword(keychainService(), keychainAccount(), password);
    return;
  }

  if (process.platform !== "darwin") {
    throw new Error(
      "Platform keychain store not available. Set AX_SECRET_KEY_FILE to use a protected key file."
    );
  }

  try {
    await execFileAsync("security", [
      "add-generic-password",
      "-s",
      keychainService(),
      "-a",
      keychainAccount(),
      "-w",
      password,
      "-U",
    ]);
  } catch {
    throw new Error(
      "Failed to store master key in macOS keychain. Check keychain permissions or set AX_SECRET_KEY_FILE."
    );
  }
}

async function resolveMasterKey(): Promise<Buffer> {
  // 1. Explicit env key.
  if (process.env.AX_SECRET_KEY_BASE64) {
    return Buffer.from(process.env.AX_SECRET_KEY_BASE64, "base64");
  }

  // 2. Keychain.
  const kc = await keychainGetPassword();
  if (kc) {
    return Buffer.from(kc, "base64");
  }

  // 3. Fallback protected key file.
  const path = fallbackKeyFile();
  if (existsSync(path)) {
    const raw = readFileSync(path, { encoding: "utf-8" }).trim();
    return Buffer.from(raw, "base64");
  }

  // 4. Generate and persist.
  const key = randomBytes(32);
  const b64 = key.toString("base64");

  try {
    await keychainSetPassword(b64);
  } catch (err) {
    writeFileSync(path, b64, { mode: 0o600 });
    // eslint-disable-next-line no-console
    console.warn(
      `[apo-vault] keychain unavailable; master key written to protected file: ${path}`
    );
  }

  return key;
}

// ---------------------------------------------------------------------------
// Crypto: AES-256-GCM
// Format: nonce (12 bytes) || ciphertext || tag (16 bytes)
// ---------------------------------------------------------------------------

function encrypt(value: string, key: Buffer): Buffer {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", key, iv);
  const ciphertext = Buffer.concat([cipher.update(value, "utf-8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, ciphertext, tag]);
}

function decrypt(data: Buffer, key: Buffer): string {
  if (data.length < 28) throw new Error("Invalid encrypted blob");
  const iv = data.subarray(0, 12);
  const tag = data.subarray(data.length - 16);
  const ciphertext = data.subarray(12, data.length - 16);
  const decipher = createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(ciphertext), decipher.final()]).toString("utf-8");
}

// ---------------------------------------------------------------------------
// Vault
// ---------------------------------------------------------------------------

class APOSecretVault {
  private _vaultPath: string;
  private _key: Buffer;

  constructor(vaultPath: string, key: Buffer) {
    this._vaultPath = vaultPath;
    this._key = key;
  }

  static async create(vaultPath?: string): Promise<APOSecretVault> {
    const path = vaultPath || join(canonicalSecretsDir(), "vault.enc");
    mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
    const key = await resolveMasterKey();
    return new APOSecretVault(path, key);
  }

  load(): VaultPayload {
    if (!existsSync(this._vaultPath)) {
      return { schema_version: "APO_SECRET_VAULT_V1", updated_at: nowIso(), records: {} };
    }
    const b64 = readFileSync(this._vaultPath, "utf-8").trim();
    if (!b64) return { schema_version: "APO_SECRET_VAULT_V1", updated_at: nowIso(), records: {} };
    const blob = Buffer.from(b64, "base64");
    const json = decrypt(blob, this._key);
    return JSON.parse(json) as VaultPayload;
  }

  save(payload: VaultPayload): void {
    payload.updated_at = nowIso();
    const json = JSON.stringify(payload);
    const blob = encrypt(json, this._key);
    const b64 = blob.toString("base64");
    const tmp = `${this._vaultPath}.tmp.${process.pid}`;
    writeFileSync(tmp, b64, { mode: 0o600 });
    renameSync(tmp, this._vaultPath);
  }
}

// ---------------------------------------------------------------------------
// Event emitter
// ---------------------------------------------------------------------------

class APOSecretEventEmitter {
  private _listeners: Array<{ fn: (e: APOSecretStorageChangeEvent) => void; thisArgs?: any }> = [];

  event: APOSecretStorageEvent = (fn, thisArgs, _disposables) => {
    const wrapped = (e: APOSecretStorageChangeEvent) => fn.call(thisArgs, e);
    this._listeners.push({ fn: wrapped, thisArgs });
    return {
      dispose: () => {
        this._listeners = this._listeners.filter((l) => l.fn !== wrapped);
      },
    };
  };

  fire(key: string): void {
    const e: APOSecretStorageChangeEvent = { key };
    for (const l of this._listeners) {
      try {
        l.fn.call(l.thisArgs, e);
      } catch {
        // no-op
      }
    }
  }
}

// ---------------------------------------------------------------------------
// SecretStorage implementation
// ---------------------------------------------------------------------------

export class APOSecretStorageSync implements APOSecretStorage {
  private _vault: APOSecretVault;
  private _emitter = new APOSecretEventEmitter();
  private _cache: Record<string, string> = {};
  private _loaded = false;
  private _lastSelfWrite = 0;

  readonly onDidChange = this._emitter.event;

  constructor(vault: APOSecretVault) {
    this._vault = vault;
  }

  static async create(vaultPath?: string): Promise<APOSecretStorageSync> {
    const vault = await APOSecretVault.create(vaultPath);
    return new APOSecretStorageSync(vault);
  }

  private _ensureLoaded(): void {
    if (this._loaded) return;
    this._load();
  }

  private _load(): void {
    const payload = this._vault.load();
    this._cache = { ...payload.records };
    this._loaded = true;
  }

  private _persist(): void {
    const payload: VaultPayload = {
      schema_version: "APO_SECRET_VAULT_V1",
      updated_at: nowIso(),
      records: { ...this._cache },
    };
    this._vault.save(payload);
    this._lastSelfWrite = statSync(this._vault["_vaultPath"]).mtimeMs;
  }

  get(key: string): Promise<string | undefined> {
    this._ensureLoaded();
    return Promise.resolve(this._cache[key]);
  }

  store(key: string, value: string): Promise<void> {
    this._ensureLoaded();
    const old = this._cache[key];
    if (old === value) return Promise.resolve();
    this._cache[key] = value;
    this._persist();
    this._emitter.fire(key);
    return Promise.resolve();
  }

  delete(key: string): Promise<void> {
    this._ensureLoaded();
    if (!(key in this._cache)) return Promise.resolve();
    delete this._cache[key];
    this._persist();
    this._emitter.fire(key);
    return Promise.resolve();
  }

  keys(): Promise<string[]> {
    this._ensureLoaded();
    return Promise.resolve(Object.keys(this._cache).sort());
  }
}

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

function nowIso(): string {
  const d = new Date();
  return d.toISOString().replace(/\.\d{3}Z$/, "Z");
}

// ---------------------------------------------------------------------------
// Optional: file-system watcher for cross-process sync
// ---------------------------------------------------------------------------

export class APOSecretStorageSyncWithWatcher extends APOSecretStorageSync {
  private _watcher: any;

  constructor(vault: APOSecretVault) {
    super(vault);
  }

  static async create(vaultPath?: string): Promise<APOSecretStorageSyncWithWatcher> {
    const vault = await APOSecretVault.create(vaultPath);
    const instance = new APOSecretStorageSyncWithWatcher(vault);
    instance._startWatcher();
    return instance;
  }

  private _startWatcher(): void {
    const vaultPath = (this as any)._vault._vaultPath as string;
    if (!existsSync(vaultPath)) return;

    watchFile(vaultPath, { interval: 1000 }, (curr: Stats, _prev: Stats) => {
      if (curr.mtimeMs <= (this as any)._lastSelfWrite) return;
      (this as any)._load();
      for (const key of Object.keys((this as any)._cache)) {
        (this as any)._emitter.fire(key);
      }
    });
  }
}
