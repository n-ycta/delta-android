## Version 0.1.18

- Pin shared Delta UI 0.3.7 (000691d) automatically (ui-sync).
- Phone sign-in has exactly two buttons, Scan/Stop and Join, with a live camera preview; an invitation arrives from a QR code or a `delta://pair` link.
- The invitation reader accepts every format the core and console produce: `delta://pair` links, the `delta join <url> <code>` command, the JSON pairing object and addresses without a scheme. An invitation that points to the device that created it is reported clearly.
- A pairing link opened outside the app is delivered once, not on every return to the app.
- Plugin API calls go to the local node first and only look for another node when the local one does not have the capability.
- Portable apps (Media) render in their isolated origin again (checked by the Android emulator test).
- The platform limitations below remain unchanged.

## Version 0.1.17

- Pin shared Delta UI 0.3.7 (d105370) automatically (ui-sync).
- Phone sign-in by QR code or link with a live camera.
- Hub nodes are now available on the phone.
- Invitation fixes.
- Apps installed from the catalog update automatically.
- APK updates use our own safe mechanism (SHA256SUMS verified, system installer confirmation, signature enforced).
- The platform limitations below remain unchanged.

## Version 0.1.16

- Pin shared Delta UI 0.3.7 (b0ed0c7) automatically (ui-sync).
- In-app updates (Settings → Core connection): checks the official GitHub releases, downloads the APK, verifies SHA256SUMS and hands it to the system installer. Android always confirms the installation and enforces the signature; nothing installs silently and nothing downloads on a metered network without consent.
- Nodes without supervisor/exec/packages (the phone's own node) now say so in the Processes, Components and Console tabs; missing CPU/memory telemetry shows a dash.
- Node rows are cards on phones.
- Publish verified LifeOS 0.3.4: compact calendar/deadline agenda, mobile statistics, visual icon grid and themed date picker.
- Include habit/category, WebView persistence and populated responsive regression fixes.
- Native first-run: connect an existing Delta node or import an existing identity before offering standalone setup.
- Android pairing uses an actual one-time delta://pair invitation and QR, not Linux/Windows commands or a required phone URL.
- Native Settings accepts links/QR too; late OS deep links work, explicit trust/service selection is preserved, one-time join is not replayed after a follow-up preference-write failure.
- Verify the signed remote core.info response before completing setup.
- Secure UUID fallback supports contexts without crypto.randomUUID; no Math.random channel nonces.
- Include invitation, onboarding, expiry, responsive and actual two-Core pairing regression tests.
- The platform limitations below remain unchanged.

## Version 0.1.15

- Keep the safe Delta launcher/name and shared UI/LifeOS updates from 0.1.14.
- Fix emulator acceptance warm-up accidentally pressing the new Connect button; tolerate a bounded UiAutomation Binder-attachment failure without replaying app actions.

## Version 0.1.14

- Installed application name: Delta, preserving the existing package ID and data.
- Reduce launcher foreground and monochrome marks to two thirds, centred inside round/adaptive safe zones.
- Test the three-choice connection/import/standalone onboarding before generating a new identity.

- Pin shared Delta UI 0.3.7 (eaecc24) automatically (ui-sync).
- Publish verified LifeOS 0.3.4: compact calendar/deadline agenda, mobile statistics, visual icon grid and themed date picker.
- Include habit/category, WebView persistence and populated responsive regression fixes.
- Native first-run: connect an existing Delta node or import an existing identity before offering standalone setup.
- Android pairing uses an actual one-time delta://pair invitation and QR, not Linux/Windows commands or a required phone URL.
- Native Settings accepts links/QR too; late OS deep links work, explicit trust/service selection is preserved, one-time join is not replayed after a follow-up preference-write failure.
- Verify the signed remote core.info response before completing setup.
- Secure UUID fallback supports contexts without crypto.randomUUID; no Math.random channel nonces.
- Include invitation, onboarding, expiry, responsive and actual two-Core pairing regression tests.
- The platform limitations below remain unchanged.

## Version 0.1.13

- Pin shared Delta UI 0.3.6 (f5c2782) automatically (ui-sync).
- Keep persistent app frames in stable DOM order; alternating two applications must not move iframe ancestors or reload their documents.
- Cover early/missed ready events and allow a separate 35-second RPC deadline.
- Bound dropdown SVG geometry and hide the retired Vector portable launcher.
- Publish the verified LifeOS 0.3.2 package.
- The platform limitations below remain unchanged.

## Version 0.1.12

- Pin shared Delta UI 0.3.2 (6f9fa64) automatically (ui-sync).
- Preserve the authenticated shell through transient Web restarts; distinguish actual authorization rejection and localize reconnect feedback.
- Acknowledge update actions immediately, refresh active jobs every second, group components in collapsible node sections, highlight progress and expose bounded cross-node parallelism when supported.
- Preserve a single plugin frame across visible surfaces and suppress stale already-open placeholders.
- Add screen-scale magnetic window snapping with alignment guides and Alt bypass; commit layout changes only at gesture end.
- Add Studio address/search and back/forward/reload controls, with an external-browser fallback for sites that refuse framing.
- Back up and migrate only redundant whole-app Console/Media desktops; retain customized arrangements.
- Update the verified Media UI catalog to 0.3.6 and permit the explicit browse capability.
- Add actual-component reconnect, update, snapping and frame-ownership browser regressions.
- The platform limitations below remain unchanged.

## Version 0.1.11

- Pin shared Delta UI 0.3.2 (0935e3f) automatically (ui-sync).
- Preserve the authenticated shell through transient Web restarts; distinguish actual authorization rejection and localize reconnect feedback.
- Acknowledge update actions immediately, refresh active jobs every second, group components in collapsible node sections, highlight progress and expose bounded cross-node parallelism when supported.
- Preserve a single plugin frame across visible surfaces and suppress stale already-open placeholders.
- Add screen-scale magnetic window snapping with alignment guides and Alt bypass; commit layout changes only at gesture end.
- Add Studio address/search and back/forward/reload controls, with an external-browser fallback for sites that refuse framing.
- Back up and migrate only redundant whole-app Console/Media desktops; retain customized arrangements.
- Update the verified Media UI catalog to 0.3.6 and permit the explicit browse capability.
- Add actual-component reconnect, update, snapping and frame-ownership browser regressions.
- The platform limitations below remain unchanged.

## Version 0.1.10

- Pin shared Delta UI 0.3.1 (7d88a05) automatically (ui-sync).
- Reflow the mobile plugin catalog into fluid cards, a two-column tab selector and a dedicated search/filter toolbar at 320px and wider.
- Center segmented-control icons explicitly and provide 44px touch targets.
- Keep the mobile dock manager reachable with a short label, aligned navigation slots and a separate now-playing row.
- Remove the unrelated history-service notice from the catalog; keep history guidance on history screens.
- Add RU/EN light/dark browser checks for mobile overflow, icon centers, hit-testing, installation controls, manager and hidden-dock reveal.
- The platform limitations below remain unchanged.

## Version 0.1.9

- Pin shared Delta UI 0.3.0 (5a000ee) automatically (ui-sync).
- Update the Media catalog to the verified 0.3.5 UI package.
- Allow only the six explicit offline-cache capabilities through the Media UI broker; keep unrelated operations denied.
- The platform limitations below remain unchanged.

## Version 0.1.8

- Pin shared Delta UI 0.3.0 (ed4f03f) automatically (ui-sync).
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

## Version 0.1.7

- Pin shared Delta UI 0.3.0 (d278f0f) automatically (ui-sync).
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

Local process execution/npm plugin installation/desktop telemetry are deliberately excluded on Android; use a paired trusted desktop/VPS node. New local profiles bind to loopback. Pairing does not provide NAT traversal. Independent signed UI activation, silent app-binary updates and arbitrary unverified plugin HTML frames are not enabled. Portable static apps are separately verified and isolated; Media decoding/background playback on real Android devices remains a separate acceptance requirement.
