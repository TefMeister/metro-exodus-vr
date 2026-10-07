# 2026-10-07 — the headset bridge's first live runs (dev PC, OpenXR simulator)

Build: `staging/metro-exodus-vr/headset-bridge-2026-10-07/` (the reader's port of The Evil Within's bridge), with
three fixes made live. Installed now: `metro_eye.dll` `7978b057911f`, `openxr_loader.dll`, `metro_eye.ini` with
`openxr=1 test_pattern=1 layers=projection`; build archive `Headset output/v0.1.0-b003`.

| file | what it shows |
| --- | --- |
| `log-1-freeze.txt` | run 1: hooks go in, the headset thread waits for a first frame that never comes (the game froze) |
| `log-2-first-frames.txt` | run 2 (freeze fixed): game swapchain 1920x1061 format 28, session running, two 1280x720 eye swapchains |
| `log-3-texture-probe.txt` | run 4: which shared-texture kinds Metro's DX11 device accepts |
| `simulator-test-pattern.png` | the OpenXR simulator's window, recorded with OBS: red left eye, blue right eye |
| `stackscan.py` | lists stack values that point into loaded modules (how the freeze was found) |

1. **Freeze on the first frame.** The bridge's first-frame capture called `GetWindowTextA` on the game window from
   the render thread. For another thread's window that sends `WM_GETTEXT` and waits; the game's main thread was
   blocked in `EnterCriticalSection` on a lock (exe `+0x2113630`) owned by that same render thread, so neither moved
   `[verified-live 2026-10-07, n=1]` (stack scan: main thread waiting on the lock; owner thread in `win32u` under
   `before_present` → `capture`). Fixed with `InternalGetWindowText`, which sends nothing; the next run did not freeze.
2. **Simulator shows only projection layers.** With the default quad layers its title said "waiting for stereo
   projection"; `layers=projection` made it run at 60 fps with the test pattern `[verified-live 2026-10-07, n=1]`.
3. **Metro's device refuses keyed-mutex textures.** `CreateTexture2D` returns `E_INVALIDARG` for any texture with
   `MISC_SHARED_KEYEDMUTEX` (0x100, with or without NT handle), for every bind-flag set tried, and accepts
   `MISC_SHARED` (0x2) and `MISC_SHARED | MISC_SHARED_NTHANDLE` (0x802) `[verified-live 2026-10-07, n=1]`. The
   ported handover locks each eye picture with a keyed mutex, so the game picture never reaches the headset yet.
   Why the device refuses is not known `[hypothesis: created through a layer without keyed-mutex support; D3D12Core
   is loaded in the process]`.
