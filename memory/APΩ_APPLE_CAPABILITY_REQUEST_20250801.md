# APΩ Apple Developer Capability Request

**Date:** 2026-08-01 (UTC)  
**Team ID:** `9ZM26YJTP4`  
**Requester:** Nguyễn Đức Cường (Andy)  
**Apple ID:** nguyencuong.2509@icloud.com  
**Purpose:** Authorize `APOmegaOS` to deploy a macOS Endpoint Security system extension for local AI runtime physical binding.

---

## 1. Required restricted entitlements

| Target | Bundle identifier | Required entitlement | Reason |
|--------|-------------------|----------------------|--------|
| Host app | `com.nguyencuong.APOmegaOS` | `com.apple.developer.system-extension.install` | Required to call `OSSystemExtensionRequest` and install/activate the embedded system extension. |
| Endpoint extension | `com.nguyencuong.APOmegaOS.APOmegaEndpoint` | `com.apple.developer.endpoint-security.client` | Required to call `es_new_client()` and subscribe to Endpoint Security `NOTIFY_*` events. |
| LaunchDaemon helper | `com.nguyencuong.APOmegaOS.APOmegaStateDaemon` | `com.apple.security.smprivilegedappservices` (via host app) + `com.apple.security.temporary-exception.mach-lookup.global-name` | Required for `SMAppService` to register the LaunchDaemon and for the app to XPC-connect to it. |

---

## 2. Product description

**APOmegaOS** is a local-first AI runtime binding agent. It uses macOS Endpoint Security in **read-only / NOTIFY mode** to observe process lifecycle events (`ES_EVENT_TYPE_NOTIFY_EXEC`, `ES_EVENT_TYPE_NOTIFY_FORK`, `ES_EVENT_TYPE_NOTIFY_EXIT`) so the local AI can maintain a physical-state ledger of its own execution environment.

- No `AUTH` callbacks are used; the extension never blocks or modifies system behavior.
- Event telemetry is kept locally in the per-user AI workspace (`~/HyperAI-Sync/`).
- The system extension is embedded inside a sandboxed host app and activates via `OSSystemExtensionRequest`.
- A separate LaunchDaemon (`APOmegaStateDaemon`) provides a signed XPC surface for durable state persistence.

This is an **internal development / personal research** tool, not a commercial security product. It is intended for local experimentation and will be signed with an Apple Development / Developer ID certificate and notarized before any distribution.

---

## 3. Bundle identifiers to register

Please ensure the following Mac App IDs are registered under Team `9ZM26YJTP4`:

```
com.nguyencuong.APOmegaOS
com.nguyencuong.APOmegaOS.APOmegaEndpoint
com.nguyencuong.APOmegaOS.APOmegaStateDaemon
```

The App ID for `APOmegaEndpoint` must **not** use a wildcard; it must be a dedicated, explicit App ID with the Endpoint Security capability enabled.

---

## 4. Capabilities to enable

For each App ID, please enable the following capabilities in the Apple Developer portal:

### Host app (`com.nguyencuong.APOmegaOS`)
- **System Extension** (`com.apple.developer.system-extension.install`)
- **App Sandbox** (`com.apple.security.app-sandbox`)
- **Hardened Runtime** (enabled at build time)

### Endpoint extension (`com.nguyencuong.APOmegaOS.APOmegaEndpoint`)
- **Endpoint Security** (`com.apple.developer.endpoint-security.client`)
- **Hardened Runtime** (enabled at build time)

### LaunchDaemon helper (`com.nguyencuong.APOmegaOS.APOmegaStateDaemon`)
- **Hardened Runtime** (enabled at build time)
- No special App Service required; it is registered via `SMAppService.daemon(plistName:)`.

---

## 5. Provisioning profiles requested

Once the capabilities above are enabled, please generate and make available for download:

- `Mac App Development` provisioning profile for `com.nguyencuong.APOmegaOS`
- `Mac App Development` provisioning profile for `com.nguyencuong.APOmegaOS.APOmegaEndpoint`
- `Mac App Development` provisioning profile for `com.nguyencuong.APOmegaOS.APOmegaStateDaemon`

For later distribution, `Mac App Direct Distribution` / `Developer ID` profiles will also be needed and will be requested separately after successful development testing.

---

## 6. Submitting the request

### Path A — Apple Developer web form (recommended)
1. Go to [https://developer.apple.com/contact/request/endpoint-security-entitlement/](https://developer.apple.com/contact/request/endpoint-security-entitlement/) or [https://developer.apple.com/system-extensions/](https://developer.apple.com/system-extensions/).
2. Select **Endpoint Security Client Entitlement**.
3. Provide Team ID `9ZM26YJTP4`.
4. Attach / paste this document as the use-case description.
5. Wait for Apple’s confirmation email and any follow-up questions.

### Path B — Apple Developer Support
If the web form is unavailable, open a Technical Support Incident (TSI) at [https://developer.apple.com/support/technical/](https://developer.apple.com/support/technical/) referencing this request.

---

## 7. Verification plan after approval

1. Download new provisioning profiles and install them in `~/Library/MobileDevice/Provisioning Profiles/`.
2. Run `xcodebuild` with `CODE_SIGNING_ALLOWED=YES` (automatic signing) or use `xcodebuild PROVISIONING_PROFILE_SPECIFIER=...` for manual signing.
3. Run `codesign -d --entitlements - APOmegaOS.app` and confirm `com.apple.developer.system-extension.install` is present.
4. Run `codesign -d --entitlements - APOmegaEndpoint.systemextension` and confirm `com.apple.developer.endpoint-security.client` is present.
5. Run `spctl --assess -t exec APOmegaOS.app` (will still reject until notarized, but should no longer show missing-entitlement errors).
6. Copy `APOmegaOS.app` to `/Applications`, launch it, click **Install Endpoint**, and approve in **System Settings > General > Login Items & Extensions > Endpoint Security**.
7. Verify `systemextensionsctl list` shows `com.nguyencuong.APOmegaOS.APOmegaEndpoint` as `activated enabled`.
8. Click **Register Daemon**, approve in **System Settings > General > Login Items & Extensions > Allow in the Background**.
9. Click **Test XPC Handshake** and confirm the daemon returns a receipt anchor.

---

## 8. Files of record

- Technical build report: `/Users/andy/HyperAI-Sync/memory/APΩ_ENDPOINT_SECURITY_BIND_REPORT_20250801.md`
- Project source of truth: `/Users/andy/workbench/APOmegaOS/project.yml`
- This request: `/Users/andy/HyperAI-Sync/memory/APΩ_APPLE_CAPABILITY_REQUEST_20250801.md`
