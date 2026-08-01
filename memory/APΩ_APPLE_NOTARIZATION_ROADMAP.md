# APΩ Apple Notarization Roadmap

## Current state (probed)

- APOmegaOS `.pkg` built: `workbench/APOmegaOS/build/APOmegaOS-1.0.0.pkg`.
- Only `Apple Development` certificates exist in keychain:
  - `Apple Development: nguyencuong.2509@icloud.com (SZMFL93XVU)` (2 identities).
- No `Developer ID Application` or `Developer ID Installer` certificate.
- No App Store Connect API key (`.p8`), no `notarytool` keychain profile.
- Apple notarization is **G11 pending** for the APΩ EndpointSecurity bind.

## Why this is blocked

Apple requires **both** of the following to notarize macOS software distributed outside the Mac App Store:

1. **Apple Developer Program membership** — paid, $99 USD/year for individuals.
   - Source: https://developer.apple.com/support/compare-memberships/
   - Free Apple accounts only receive `Apple Development` certificates, which are for local debugging and are *not* accepted by Gatekeeper for public distribution.
2. **A Developer ID certificate** created in the Apple Developer portal.
   - `Developer ID Application` to sign the `.app` bundle.
   - `Developer ID Installer` to sign the `.pkg` installer.
   - Source: https://developer.apple.com/help/account/certificates/create-developer-id-certificates

Without (1) and (2), no CLI tool (`xcrun notarytool`, `asc`, `appledev`, `fastlane`) can complete notarization.

## Skills installed / available

| Skill / tool | What it does | What it cannot do |
|--------------|--------------|-------------------|
| `apomega-notarization` (local) | Local script `notarize.py`: checks cert, signs `.pkg` with `productsign`, runs `xcrun notarytool submit`, staples with `xcrun stapler`. | Cannot create or download a Developer ID cert. |
| `asc-notarization` (skills.sh) | Guide for `xcodebuild archive/export` + `asc notarization submit` using App Store Connect API key. | Cannot create Developer ID certificates (ASC API does not support it). |
| `apple-developer-toolkit` (skills.sh) | Can list certificates / notarize with `appledev store notarization submit` if API key is present. | Cannot create Developer ID certificates; needs API key. |
| `fastlane` | Can manage certs/profiles (`match`, `sigh`) and notarize (`notarize` action). | Needs Apple ID + 2FA + paid membership + cert. |

## Path to completion

### Step 1: Apple Developer Program (creator decision)

The creator must either:

- Confirm the existing Apple ID `nguyencuong.2509@icloud.com` is already enrolled in the paid Apple Developer Program, or
- Authorize the $99/year enrollment at https://developer.apple.com/programs/enroll/ and provide the Apple ID / Team ID.

This is an external provider payment route. **Do not proceed without explicit creator authorization.**

### Step 2: Generate a Certificate Signing Request (CSR)

```bash
openssl req -new -newkey rsa:2048 -nodes -keyout APOmegaOS_DeveloperID.key \
  -out APOmegaOS_DeveloperID.csr -subj "/emailAddress=nguyencuong.2509@icloud.com, CN=APOmegaOS Developer ID, C=US"
```

Keep `APOmegaOS_DeveloperID.key` secure and outside git.

### Step 3: Create Developer ID certificates in the portal

1. Log in to https://developer.apple.com/account/resources/certificates/add
2. Select `Developer ID Application` → upload `APOmegaOS_DeveloperID.csr` → download `.cer`
3. Select `Developer ID Installer` → upload the same CSR → download `.cer`
4. Double-click each `.cer` to add to `login` keychain. They should appear with the private key from the CSR.

### Step 4: Export .p12 (optional, for CI)

```bash
security find-identity -v -p basic
# note the SHA-1 of the Developer ID Installer cert
security export -k login.keychain-db -t privKeys -f pkcs12 -o APOmegaOS_DeveloperID.p12
```

### Step 5: Create a notarytool keychain profile

```bash
xcrun notarytool store-credentials apomega-notary \
  --apple-id nguyencuong.2509@icloud.com \
  --team-id SZMFL93XVU
# prompt: app-specific password from https://appleid.apple.com
```

### Step 6: Run the notarization pipeline

```bash
cd /Users/andy/workbench/APOmegaOS
python3 .devin/skills/apomega-notarization/scripts/notarize.py \
  --pkg build/APOmegaOS-1.0.0.pkg \
  --team-id SZMFL93XVU
```

The script will:
1. Find the `Developer ID Installer` cert.
2. Run `productsign`.
3. Submit to `xcrun notarytool`.
4. Staple the ticket.
5. Run `pkgutil --check-signature` and `spctl --assess`.

## Verification checklist

- [ ] Apple Developer Program active.
- [ ] `security find-identity -v -p basic | grep "Developer ID Installer"` returns a valid identity.
- [ ] `xcrun notarytool history --keychain-profile apomega-notary` works.
- [ ] `build/APOmegaOS-1.0.0_signed.pkg` exists and is notarized.
- [ ] `spctl --assess -t install build/APOmegaOS-1.0.0_signed.pkg` returns `accepted`.

## Evidence

- Keychain probe: `security find-identity -v -p basic` → only Apple Development cert.
- Apple membership table: free Apple Account does **not** include Notarization & Developer ID.
- `asc-notarization` SKILL.md: "PKG notarization needs a Developer ID Installer certificate... not available through the App Store Connect API."
- **Runtime probe (2026-08-01T06:18Z)**: `xcodebuild -exportArchive` with `method=developer-id` and `teamID=9ZM26YJTP4` failed with:
  - `No signing certificate "Developer ID Application" found`
  - `No profiles for 'com.nguyencuong.APOmegaOS.APOmegaEndpoint' were found`
  - `No profiles for 'com.nguyencuong.APOmegaOS' were found`
  - The resolved team name was `(null)` in `IDEDistributionTeamStep`, strongly indicating the team is not a paid Apple Developer Program team or has no Developer ID certificates.
- **Credential probe (2026-08-01T06:28Z)**: `xcrun altool --list-providers -u nguyencuong.2509@icloud.com` with the Apple ID main password accepted the credentials but returned:
  - `Please sign in with an app-specific password. You can create one at account.apple.com.`
  - This confirms the Apple ID / main password pair is valid, but notarization / App Store Connect tools require an **app-specific password**, not the main password.
- **CSR generated (2026-08-01T06:35Z)**: `build/certs/APOmegaOS_DeveloperID.csr` and `build/certs/APOmegaOS_DeveloperID.key` created for uploading to the Apple Developer portal when the Developer ID certificate is requested.
