# Delta Android

Delta on your phone: an Android app with an embedded Rust node and the same shared UI ([delta-ui](https://github.com/n-ycta/delta-ui)) as Desktop and Web. No web server or Node.js is needed on the device.

Android 8.0+ (API 26) · ARM64 and x86_64 in one APK · [Delta overview](https://github.com/n-ycta/delta#readme)

## What it does

- Runs the full shared interface over a bounded native IPC. Root administrative credentials never enter JavaScript.
- Keeps a local node of its own; pair it with a reachable trusted desktop or VPS node to use that node's capabilities.
- Optional background service that owns the node independently of the screen, with an ongoing notification and a **Stop** action. Optional notifications for plugin feeds.
- Pairs by invitation code, QR image or `delta://pair` link. Links and QR codes only prefill the form; joining and incoming administrative trust always need an explicit tap.
- Android document picker, share sheet, external browser and notification-permission integration.

### What differs from Desktop and Web

The interface is the same; the **node** differs, so some capabilities live on a paired node instead:

| Capability | On the phone | Where to get it |
| --- | --- | --- |
| Shared UI, dashboards, preferences, pairing | Yes (stored by the native host, encrypted) | — |
| Local shell execution, npm plugin processes, package installation | No | A paired desktop/VPS node |
| Host telemetry (CPU, memory, disk) | No — shown as “—” | The same paired node |
| MCP, updates, provisioning, observability | Via independent plugins on a node you select | Settings → Core connection |
| Inbound connections / NAT traversal | No: the node listens on loopback only | VPN or HTTPS on the paired node |

## Install

[**Download the latest APK**](https://github.com/n-ycta/delta-android/releases/latest/download/Delta-Android-arm64-x86_64.apk) · [SHA256SUMS](https://github.com/n-ycta/delta-android/releases/latest/download/SHA256SUMS) · [Release notes](https://github.com/n-ycta/delta-android/releases/latest)

1. Download the APK on the phone and verify it against `SHA256SUMS`.
2. Allow installation from the browser or file manager you deliberately chose.
3. Install. Updates install over the existing app without clearing data.

Production uses the package `dev.delta.android`; debug previews use `dev.delta.android.preview` and are a separate app with separate data. Releases are signed with a stable private key held in encrypted CI secrets; future updates must keep that key and raise the version code.

## First run

1. Open Delta. Its local node belongs to the app's private profile: there is no account registration or owner-token paste.
2. Open **Settings → Core connection**. Enter a reachable remote node URL and an invitation code, or scan an invitation QR image, and review any incoming administrative trust before joining.
3. Select the trusted desktop/VPS node that should provide MCP, updater, provisioning and observability services.
4. Enable **Background service** only if you need it, and grant notification permission when Android asks.

## Security and privacy

- The profile, peer trust secrets and native UI documents are encrypted with an app-scoped, non-exportable Android Keystore AES-GCM key. There is no plaintext fallback.
- Cloud backup and device transfer of the private profile are disabled. **Losing the Keystore key means re-pairing**; this is not a portable identity backup. Do not clear app storage or uninstall as a troubleshooting step without knowing that.
- The node is loopback-only. Use HTTPS or a trusted private network/VPN to reach other nodes; pairing does not expose local ports.

## Android limits

Doze, battery optimization and vendor policies can delay networking or end background work; force-stop halts the service until you open the app again. No 24/7 guarantee is made. Not enabled or claimed: independently signed UI activation and rollback, in-app binary self-update, arbitrary plugin HTML frames and physical-device battery or reboot acceptance. UI updates ship with the app.

## Build from source


Requires Node 24, Rust, JDK 17, Android SDK 35 and NDK 27.2.12479018. Run `npm ci --ignore-scripts`, `npx tauri android init --ci`, `python3 scripts/prepare-android.py`, then `npx tauri android build --apk --target aarch64 x86_64 --ci`. Set `DELTA_KEYSTORE`, `DELTA_STORE_PASSWORD` and `DELTA_KEY_PASSWORD` securely for a production build. Never commit the key or passwords.

CI verifies the production APK signature and runs `tests/emulator-smoke.py` on a disposable Android 35 emulator. Emulator evidence is not a physical-device test.

## Links

[Delta](https://github.com/n-ycta/delta) · [Delta UI](https://github.com/n-ycta/delta-ui) · [Delta Desktop](https://github.com/n-ycta/delta-desktop) · [Release notes](RELEASE.md) · [Changelog](CHANGELOG.md) · [Apache 2.0 license](LICENSE)
