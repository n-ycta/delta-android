## Version 0.1.6

- Pin shared Delta UI 0.3.0 (0333a6b) automatically (ui-sync).
- One global dock outside every app: Console, installed apps and desktops; configurable position (left/right/top/bottom/hidden), size, labels, order and pinning; context menu (open, pin, rename, duplicate, delete, stop, uninstall); bottom bar on phones.
- “All apps” manager: installed apps appear automatically after installation, catalog install/update, desktop previews and template gallery, dock constructor, theme.
- Apps and desktops are separate concepts; Console and Media are no longer “desktops”. New “Home” desktop with clock, quick launch, now playing and tips.
- Running apps live above the router: music keeps playing when switching apps, desktops or Console pages; mini-player in the dock.
- One global theme for the system and apps: Catppuccin Latte (Manrope), Gruvbox Light (Golos Text + Literata), Catppuccin Mocha (Onest), Tokyo Night (JetBrains Mono); tokens are passed to app frames (`applyThemeTokens`).
- Dashboard “App” widget embeds an installed app with the usual move/resize.
- SDK: media session (`reportMedia`, `onMediaCommand`) and catalog-governed intents between apps (`sendIntent`, `onIntent`).
- Fix: the launcher “Apps” and “Settings” buttons opened the same dialog; distinct icons for Console, desktops and templates.
- Fix: the toast container no longer covers top-right controls; overlays are anchored to the stage, above the global dock.
- Catalog: Delta Media 0.2.0 (player, receives `media.play`/`media.enqueue`) and new source apps Delta YouTube, Delta SoundCloud, Delta Spotify 0.1.0 (send those intents). App CSP allows the official SoundCloud and Spotify embeds.
- The platform limitations below remain unchanged.

## Version 0.1.5

- Pin shared Delta UI 0.3.0 (bcfc44f) automatically (ui-sync).
- One global dock outside every app: Console, installed apps and desktops; configurable position (left/right/top/bottom/hidden), size, labels, order and pinning; context menu (open, pin, rename, duplicate, delete, stop, uninstall); bottom bar on phones.
- “All apps” manager: installed apps appear automatically after installation, catalog install/update, desktop previews and template gallery, dock constructor, theme.
- Apps and desktops are separate concepts; Console and Media are no longer “desktops”. New “Home” desktop with clock, quick launch, now playing and tips.
- Running apps live above the router: music keeps playing when switching apps, desktops or Console pages; mini-player in the dock.
- One global theme for the system and apps: Catppuccin Latte (Manrope), Gruvbox Light (Golos Text + Literata), Catppuccin Mocha (Onest), Tokyo Night (JetBrains Mono); tokens are passed to app frames (`applyThemeTokens`).
- Dashboard “App” widget embeds an installed app with the usual move/resize.
- SDK: media session (`reportMedia`, `onMediaCommand`) and catalog-governed intents between apps (`sendIntent`, `onIntent`).
- Fix: the launcher “Apps” and “Settings” buttons opened the same dialog; distinct icons for Console, desktops and templates.
- Fix: the toast container no longer covers top-right controls; overlays are anchored to the stage, above the global dock.
- Catalog: Delta Media 0.2.0 (player, receives `media.play`/`media.enqueue`) and new source apps Delta YouTube, Delta SoundCloud, Delta Spotify 0.1.0 (send those intents). App CSP allows the official SoundCloud and Spotify embeds.
- The platform limitations below remain unchanged.

## Version 0.1.4

- Pin shared UI 0.2.1, fixing embedded forms and navigation at narrow application-pane widths.
- Restore intended Workbench control styling; preserve saved layouts, identities and Media libraries.
- The platform limitations below remain unchanged.

## Version 0.1.3

- Pin shared UI 0.2.0: full Console, composable workbench, four themes and
  templates, responsive dock, compact hideable host controls, editable overview.
- Bundle verified Media 0.1.0-alpha.3 with radio presets and reusable shared
  application surfaces. Existing libraries and workspace layouts survive asset updates.
- Retain host permission boundaries; composition never grants plugin permissions.
- Native background audio and cross-device media-library sync are not claimed.

Android 8+ native client with embedded Rust Core and the same immutable-pinned Delta UI as Desktop and Web. Universal APK includes ARM64 and x86_64, uses the production app ID dev.delta.android, and is signed with a stable private release key held in encrypted Actions secrets.

- Internal same-origin navigation remains inside the bundled application; real external HTTP(S) links use the OS browser.
- Explicit personal-key onboarding and Phosphor interface icons from shared Delta UI.
- Shared UI 0.2.0: display name, nickname and avatar settings; recovery phrases hidden by default with copy and native Markdown export controls.
- Isolated portable Delta app installation and offline Media UI startup; no owner IPC or credentials exposed to app frames.
- Canonical SVG brand with platform PNG/ICO resources; Android adaptive, round and monochrome launcher resources.
- Full shared UI over bounded native IPC; no Web server or Node.js required.
- Android Keystore AES-GCM encryption for profile, peer secrets and native UI documents, with no plaintext fallback and backup/transfer exclusions.
- Explicit foreground-service opt-in, ongoing notification, Stop action and plugin notification delivery acknowledgements.
- QR invitation images, safe pairing deep links, explicit incoming trust and service-node selection.
- Native document picker, share sheet and external browser adapters.

Verify SHA256SUMS before installation. Debug .preview builds are a separate application, not the production update channel.

Release gates verify APK signing and exercise startup, encrypted-profile persistence, Activity background/relaunch and service opt-in on an Android 35 emulator. No physical-device reboot/battery acceptance is claimed. Android Doze/vendor policies may delay or stop networking; force-stop requires a user relaunch. No 24/7 guarantee.

Local process execution/npm plugin installation/desktop telemetry are deliberately excluded on Android; use a paired trusted desktop/VPS node. New local profiles bind to loopback. Pairing does not provide NAT traversal. Independent signed UI activation, app binary self-update and arbitrary unverified plugin HTML frames are not enabled. Portable static apps are separately verified and isolated; Media decoding/background playback on real Android devices remains a separate acceptance requirement.
