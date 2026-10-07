# 2026-10-07 (/lm reader, dev PC): The Evil Within's headset bridge ported to Metro

Built in `staging/metro-exodus-vr/headset-bridge-2026-10-07/` (staging repo). Static work only: the game was never
launched, attached to, or touched by this helper.

## What it is

A new `metro_eye.dll` (sha256 `189dde8cae28…f18`, 250 KB) that keeps the 2026-10-07 camera hook unchanged in
behaviour and adds The Evil Within's OpenXR output (stereo-6dof-core `cd9efc2`: own D3D11 device and session on a
headset thread, a keyed-mutex shared texture per eye, game-swapchain filter). Head tracking (TEW `b4ab740`) is not
ported. The loader `dxgi.dll` from `eye-hook-2026-10-06` (`76d0c7688b4c`) is reused unchanged.

- **Off by default.** `metro_eye.ini` `[xr] openxr=0`: no Present hook, no graphics dll loaded; the import table is
  the same set as the eye-hook build `[compile-verified 2026-10-07]`.
- **Present hook** (`present_hook.c`): IDXGISwapChain::Present (vtable 8) and Present1 (22) via a throwaway 1x1
  swapchain; nested calls and `DXGI_PRESENT_TEST` skipped; the first game Present captures device + immediate
  context and logs back-buffer size, format, buffer count, swap effect, MSAA and device creation flags.
- **Which eye a presented picture is** (`eye_queue.c`): each scene render (`0xd859f0`) pushes its side; each game
  Present takes the OLDEST unclaimed one (first in, first out). This pairs correctly at any renderer lag, provided
  each scene render is presented exactly once. A Present with nothing queued (menus, loading) goes to both eyes.
  The Present hook is installed before the camera hook so no backlog forms.
  Knobs: `eye_source=1` (newest instead), `swap_eyes=1`, `test_pattern=1`, `layers=projection`, `runtime_json=`.
- Tests: `tests/eye_queue_test.c` (in-step, one-frame lag, newest mode, overflow, hook off) and
  `tests/pick_format_test.c` pass `[compile-verified 2026-10-07]` (run on the dev PC, not in the game).

## What is NOT known

- Whether Metro's scene render and Present are one-to-one and how far apart they run `[hypothesis]`. The dossier
  says the camera goes into a command stream the DX11 renderer replays, so a lag of one or more frames is plausible.
  The log prints, for the first 12 game Presents and every 600th: eye chosen, scene renders waiting, dropped,
  empty, render thread id, present thread id. **Steady "waiting" = pairing holds; climbing = it does not.**
- Whether the eyes arrive crossed (`swap_eyes=1` is the fix if near things separate the wrong way) `[hypothesis]`.
- Metro's back-buffer format; the bridge handles 8-bit RGBA/BGRA, 10-bit, half float and MSAA `[inferred-static]`.
- Nothing here has run: not in the game, not in the OpenXR simulator. A simulator run was not attempted because its
  preview window would take focus from the game the live session is driving.

## Next step (flat, dev PC, OpenXR simulator)

Install `build/metro_eye.dll` over the eye-hook one, put the x64 `openxr_loader.dll` beside the exe
(`third_party/openxr/fetch_loader.md`), set `[eye] enabled=1 mode=0` and `[xr] openxr=1` plus `runtime_json=` the
simulator's json. First run `test_pattern=1` (red left, blue right) to prove the layers show, then the game picture.
Read `metro_eye_log.txt`: the `present N:` lines and the `mxr diag:` serial counts for both eyes.
