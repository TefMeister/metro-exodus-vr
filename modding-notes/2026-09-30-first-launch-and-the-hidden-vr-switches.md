# 2026-09-30 — first launch, and the hidden VR switches

Unattended `/lm` session on the dev PC. Tefa handed it over without the Menu-o-matiC setup.

## What happened

- **The game will not run on the dev PC.** Its graphics card (GTX 1660 SUPER) lacks DXR 1.1, the
  ray-tracing level the Enhanced Edition needs. The game says so in a warning box; "Run Anyway" plays
  the intro films, builds shaders on the title screen for about six minutes, then crashes inside
  Windows' Direct3D 12 runtime `[verified-live 2026-09-30, n=1]`. The exe has no older renderer to fall
  back to `[inferred-static 2026-09-30]`. So **every live test of this game belongs to the home PC.**
- **A static read found two dormant VR switches** (details in the dossier's 2026-09-30 folds):
  - `vr_stereo`, a renderer setting that swaps in a `post_vr` screen shader but never actually draws
    two eyes, because the eye number it would use is always -1 `[inferred-static 2026-09-30]`.
  - `-build_key oculus`, a launch switch checked in 72 places across gameplay, menus and rendering,
    most likely the VR build variant from 4A's Arktika.1 era `[hypothesis]`.
- Windowing for the home PC: `user.cfg` lines `r_fullscreen off`, `r_res_hor 1280`, `r_res_vert 720`
  `[inferred-static 2026-09-30]`, untested.

## What is NOT established

- That the missing DXR 1.1 support is what caused the crash. It fits the warning, but the dump only
  shows where it crashed.
- What `-build_key oculus` or `vr_stereo on` do in a running game. Both are static reads.
- Whether the `user.cfg` lines give a window. The file did not exist yet on the dev PC.

## Automation score (the five capabilities)

| Capability | State on this game |
| --- | --- |
| Self-launch | ✅ through Steam, plus BM_CLICK on the warning box |
| Menu → gameplay | ❌ never reached the main menu (crash) |
| Console / commands | ❌ untested; `user.cfg` is the route |
| Character + camera | ❌ untested |
| Self-close | ⚠️ only through the crash box's Close button |

Evidence: `dev-archive/recon/2026-09-30-first-launch-dev-pc/`.
