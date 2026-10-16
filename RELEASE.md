Android 8+ native client with embedded Rust Core and the same immutable-pinned Delta UI as Desktop and Web. Universal APK includes ARM64 and x86_64, uses the production app ID dev.delta.android, and is signed with a stable private release key held in encrypted Actions secrets.

- Full shared UI over bounded native IPC; no Web server or Node.js required.
- Android Keystore AES-GCM encryption for profile, peer secrets and native UI documents, with no plaintext fallback and backup/transfer exclusions.
- Explicit foreground-service opt-in, ongoing notification, Stop action and plugin notification delivery acknowledgements.
- QR invitation images, safe pairing deep links, explicit incoming trust and service-node selection.
- Native document picker, share sheet and external browser adapters.

Verify SHA256SUMS before installation. Debug .preview builds are a separate application, not the production update channel.

Release gates verify APK signing and exercise startup, encrypted-profile persistence, Activity background/relaunch and service opt-in on an Android 35 emulator. No physical-device reboot/battery acceptance is claimed. Android Doze/vendor policies may delay or stop networking; force-stop requires a user relaunch. No 24/7 guarantee.

Local process execution/npm plugin installation/desktop telemetry are deliberately excluded on Android; use a paired trusted desktop/VPS node. New local profiles bind to loopback. Pairing does not provide NAT traversal. Independent signed UI activation, app binary self-update and arbitrary plugin HTML frames are not enabled.
