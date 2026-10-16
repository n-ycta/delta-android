# Delta Android — experimental P0 host

The Rust core is embedded in the application. This is **not** a link to a remote Web panel, and Node.js/npm is not needed on the user's device. Screens are imported from the same immutable `delta-ui` package used by Web; there is no copied frontend.

## Available in this first development slice

- Persistent local node identity, core capability/component discovery and the shared native UI.
- Versioned, size-bounded root-document IPC; owner credentials are not sent to JavaScript.
- Mobile assembly excludes desktop process execution, npm package installation and host telemetry. Unsupported integrations are not simulated.
- Desktop: reuse `DELTA_HOME` / `~/.delta`, verify node identity before attaching to an existing running profile, otherwise embed the same profile. Exclusive host lease prevents duplicate GUI runtimes. Closing the window hides it to the tray; Exit node is explicit.

## Not ready / acceptance gates

Full parity with Web's MCP/SSH/update/plugin-projection services, QR pairing UI, platform file/share/notification adapters, Keystore-backed trust secrets, background Android service, independent signed UI updates, workspaces, signed stable installers and physical-device reboot/sleep checks are **not complete**. Plugin HTML frames are disabled by CSP until isolation is integrated and tested. Do not mark ANDROID-01/DESKTOP-01/P0/P1 complete from this preview.

Android uses application-private persistent storage and is currently foreground-only: Android may stop it. Debug APK signing from CI is not a stable update channel; keep production profiles out of debug builds. No 24/7 promise.

## Build

`npm ci && npm run build:ui`. Native build additionally requires Rust and the platform Tauri prerequisites. Desktop: `npx tauri build --bundles appimage` (Linux), `--bundles nsis` (Windows). Android: `npx tauri android init --ci`, then `npx tauri android build --debug --apk --target aarch64 --ci` with Android SDK/NDK installed.

