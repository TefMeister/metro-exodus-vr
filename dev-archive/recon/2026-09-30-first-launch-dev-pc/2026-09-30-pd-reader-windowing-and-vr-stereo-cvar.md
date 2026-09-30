# Windowing keys, command-line switches, and a live `vr_stereo` cvar (static read, 2026-09-30)

From: PD reader helper for the 2026-09-30 live session. Static only: nothing launched, nothing in the
game folder touched. Build: Steam app 1449560, exe link date 2026-08-27 (same build as the dossier).
Addresses below are RVAs in `MetroExodus.exe` (image base 0x140000000).

## 0. The DRM wrapper does not block static reading

`.text` entropy is 6.53 (normal code, not encrypted); only the entry point sits in `.bind` (RVA
0x31fa310). Code cross-references to strings resolve cleanly. `[inferred-static 2026-09-30]`

## 1. Windowed 1280x720

- `r_fullscreen` is a **boolean flag cvar**: registered at RVA 0xd7d57d as bit 0x200000 of a flags word
  (RVA 0x15ad7b0), which is set on disk, so the default is fullscreen on. `[inferred-static 2026-09-30]`
- Boolean cvars print as `on`/`off` and accept "'on/off' or '1/0'" (RVA 0x91000/0x91040).
  `[inferred-static 2026-09-30]`
- `r_res_hor` and `r_res_vert` are integer cvars, looked up by name in the cvar registry
  (RVA 0x6d766b) and set in a separate settings reader (RVA 0x9cf0e). `[inferred-static 2026-09-30]`
- **No borderless or window-mode cvar exists.** No `r_window*`, `borderless`, `r_adapter` or
  `r_monitor` strings. **No command-line windowing switch exists** (`-windowed`, `-width`, etc. are
  absent). `[inferred-static 2026-09-30]`
- Start-up order (RVA 0x585dbc): it sets the file names `user.cfg` and `profile.cfg`, runs
  `r_enable_res_change 1` and `r_enable_rapi_change 1`, then runs **`config_load <user.cfg path>`**,
  then `exec-user-script`. So `user.cfg` is a console script run at every start, and any cvar line
  in it applies. `[inferred-static 2026-09-30]`
- **Proposed `user.cfg` lines** (format `name value`, one per line):
  ```
  r_fullscreen off
  r_res_hor 1280
  r_res_vert 720
  ```
  `[hypothesis]`: this is untested live, and the menu may rewrite the file on exit.
- Location: the game asks Windows for the Saved Games folder. `<user>\Saved Games\Metro Exodus\` already
  exists on the dev PC, but holds only `steam_autocloud.vdf`. Players say the file is in a
  `<steamid>` subfolder `[reported]`. It probably appears only after the first real start, so let
  the game make it once, then edit it. `[hypothesis]`
- ⚠️ **Automation trap:** after a crash the next start shows a Yes/No box, "Previous launch was
  unsuccessful. Would you like to start in safe mode?". Answering Yes runs `r_api_rx 2`,
  `r_quality_level 0`, `r_af_level 0`, `r_shading_rate 1`, `r_fur 0`, `r_dx11_tess 0`,
  `r_dlss_rx 0` and `r_dlisp 1`. The registry key `Software\4A-Games\Metro Exodus` and the value
  `BadQuit` sit beside it, so that value is the likely flag. `[inferred-static 2026-09-30]`

## 2. Command-line switches found (not the full list)

`-forcelog`, `-logpath <dir>`, `-logflush`, `-nocrashdlg`, `-fulldmp`, `-d3d_debug`, `-nvperf`,
`-identifiers`, `-cpu <n>`, `-sleep`, `-map <name>`, `-save`, `-server`, `-build_key`, `-benchmark`
plus `-bench_*` (`_runs`, `_ui`, `_track`, `_output`, `_options`, `_preset_name`, `_track_count`),
`-openautomate`, `-force_rapi`, `-force_physx`, `-nogpu`, `-forcenohdr`, `-deependark`,
`-dxrt_fullmesh`, `-edr_mode`, `-use_shaders_lib`, `-backend_serial`, `-vfs_no_dups`, `-patch_cfg`,
`-patch_rev`, `-trace`, `-intel`, `-corsair_error_log`, `-vr_profile`. `[inferred-static 2026-09-30]`
(each one's effect is unchecked unless stated)

- **Intro skip:** no switch found. Start-up queues `legal` and then `intro` (`%s%s.webm` beside the
  exe) and plays them through `r_video <name>`. There is a `skip_video` action and a
  `video_skip_hint`, so a key press probably skips them. `[hypothesis]`
- **Console:** no switch found. A console command handler exists (`~ Unknown command: %s`,
  `~ command disabled.`, `execute_console_cmd_handler`), but opening it needs the known memory patch
  `[reported]`. `user.cfg` gives the same cvar access without a console.

## 3. The VR names are live code, not leftover labels

- **`vr_stereo` is a live boolean console variable in the renderer.** It is an initialised cvar
  object in `.data` (name pointer at RVA 0x1651ee8, value at RVA 0x1651f08, default 0/off), uses the
  same cvar class as `r_dbg_aq`, is added to the global cvar registry at start-up (RVA 0x4e0d0), and
  about **20 renderer functions test its value** (for example RVA 0xdcc57b, 0xdd35da, 0xe34bd6).
  `[inferred-static 2026-09-30]` Whether `vr_stereo on` draws anything useful without a headset
  runtime is `[hypothesis]`, and it is the best lead in this file.
- **`-vr_profile` is live code:** two functions (RVA 0xdbb991, 0xe14105) `strstr` the command line
  for it, and when it is present they call the render device's vtable slot +0x3c0 17 times, keeping
  17 handles. `[inferred-static 2026-09-30]` It looks like GPU timing or profiling, not a headset
  path. `[hypothesis]`
- Every `vr_*` gameplay name (hand speed, grab lerp, aim angle, missile weapon, HMD height bias,
  curve settings) is referenced by code or by a cvar/property table. They are compiled in, not dead
  strings. `[inferred-static 2026-09-30]`
- A shader define `%s/_OCULUS_=1` is referenced by the shader-cache loader (RVA 0xddf48a), so a
  shader variant for Oculus may be requested. `[inferred-static 2026-09-30]`
- **No headset runtime anywhere:** there is no OpenVR, OpenXR, LibOVR or `ovr_` import or string. The
  only imports are the standard system, Steam, PhysX, NVIDIA and Corsair DLLs. So the rendering and
  gameplay VR code survives, but the headset connection was removed. `[inferred-static 2026-09-30]`

## Suggested next steps

- `[FLAT]` Write the three `user.cfg` lines, start the game, and measure the window **and** the desktop
  resolution.
- `[FLAT]` Add `vr_stereo on` to `user.cfg` on a separate run and compare a screenshot with a run
  without it.
- `[PD]` Decompile the ~20 functions that read `vr_stereo` to see what they change (render size,
  views, passes).

Tools used: Python PE parsing, a RIP-relative cross-reference scan, and capstone. Scripts are in
`staging/metro-exodus-vr/pd-reader-2026-09-30/`.
