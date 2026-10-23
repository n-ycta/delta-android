# Delta Android

Android 8+ application with an embedded Rust Core and the same immutable-pinned `delta-ui` used by Desktop and Web. No Web server or Node.js is required. The release APK includes ARM64 and x86_64 native libraries.

## Application

- Full shared interface over bounded native IPC. Root administrative credentials never enter JavaScript.
- Local dashboards and preferences are persisted by the native host, not by a Web storage plugin.
- The profile, peer trust secrets and native UI documents are encrypted with an app-scoped, non-exportable Android Keystore AES-GCM key. There is no plaintext fallback. Cloud backup/device transfer of the private profile is disabled. Losing the Keystore key requires re-pairing; this is not a portable identity backup.
- A user-enabled foreground service owns the Core independently of the Activity/WebView. It has an ongoing notification and a Stop action. Optional notifications for plugin feeds are acknowledged only after Android accepts delivery.
- Activity restoration and explicit relaunch reuse the same encrypted profile. Boot restoration is best effort and respects Android policy.
- QR invitation images and `delta://pair` links only prefill pairing; joining and incoming administrative trust require explicit user actions.
- Android document picker, share sheet, external browser and notification permission adapters.
- The mobile Core deliberately excludes local shell execution, npm process supervision/package installation and desktop host telemetry. Use a paired trusted desktop/VPS node for those capabilities. MCP, provisioning, updates and observability require their independent plugins on an explicitly selected service node.

## Installation and signing

[**Download the latest APK**](https://github.com/n-ycta/delta-android/releases/latest/download/Delta-Android-arm64-x86_64.apk) · [SHA256SUMS](https://github.com/n-ycta/delta-android/releases/latest/download/SHA256SUMS) · [Release notes](https://github.com/n-ycta/delta-android/releases/latest)

Download the APK directly on your phone, verify its checksum and allow installation from the browser/file manager you deliberately chose. The universal package supports ARM64 phones and x86_64 emulators; Android 8.0 (API 26) or later is required. Updates can be installed over the existing production app without clearing its data. Production uses `dev.delta.android`; debug previews use a separate `.preview` ID. A stable private signing key is held in encrypted GitHub Actions secrets, not in source control. Future updates must retain that key and increase the version code. Keep production data out of debug builds.

## First run

1. Open Delta. Its local node belongs to the app's private OS profile; there is no public account registration or browser owner-token paste.
2. Open **Settings → Core connection**. Enter a reachable remote Core URL and invitation code, or scan an invitation QR image. Review incoming administrative trust before joining.
3. Select the trusted desktop/VPS node for optional MCP, updater, provisioning and observability services. Android does not run npm plugins locally.
4. Enable **Background service** only if needed and grant notification permission when Android asks. The ongoing notification provides a Stop action. System notifications for plugin feeds are a separate opt-in.

Do not clear app storage or uninstall the app as a troubleshooting step without understanding that its Keystore-bound local identity is not a transferable backup. A reinstall may require re-pairing.

## Android restrictions

Doze, battery optimization and vendor policies can delay networking or terminate background work. Force-stop stops the service until the user launches the app again. No 24/7 guarantee is made. The new local Core is loopback-only: it can call a reachable paired remote Core, but pairing does not provide NAT traversal or inbound exposure. Use HTTPS or a trusted private network/VPN.

Independent signed UI activation/rollback, silent app-binary updates, arbitrary plugin HTML frames and physical-device battery/reboot acceptance are not enabled or claimed. UI updates ship with the app.

## Build and acceptance

Requires Node 24, Rust, JDK 17, Android SDK 35 and NDK 27.2.12479018. Run `npm ci --ignore-scripts`, `npx tauri android init --ci`, `python3 scripts/prepare-android.py`, then `npx tauri android build --apk --target aarch64 x86_64 --ci`. Set `DELTA_KEYSTORE`, `DELTA_STORE_PASSWORD` and `DELTA_KEY_PASSWORD` securely for a production build. Never commit the key or passwords.

CI verifies the production APK signature and runs `tests/emulator-smoke.py` on a disposable Android 35 emulator. Emulator evidence is not a physical-device test.
