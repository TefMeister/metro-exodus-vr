# Original edition (app 412020) static recon + logging proxy, 2026-10-06

From: `/lm` reader helper, dev PC. Static file reading only; the game was running and was not touched.
Target: `E:\SteamLibrary\steamapps\common\Metro Exodus\MetroExodus.exe`, Steam build 6544595,
26,793,168 bytes, sha256 `d4ab0e9b076d324f6b8ddad601fd9dda68c0c593adb7b0019944d560bc9875a5`,
PE32+ x64, header link date 2020-05-27.

Folds into: dossier §1 (identity: a second edition), §3 (renderer), §4 (DRM, injection), §9 (cvars), §11 (the
"no DX11 renderer" dead end is Enhanced-only), §12.

## Binary and DRM (§3, §4)
- Sections `.text .rdata .data .pdata _RDATA .rodata .rsrc .reloc .bind`; entry point sits inside `.bind`
  (entropy 7.96). Same Steam DRM wrapper as the Enhanced Edition; `.text` entropy 6.51, so the code is not
  encrypted on disk. No Denuvo / VMProtect / Themida / SteamStub strings `[inferred-static 2026-10-06]`.
- No Direct3D or DXGI in the static import table. The exe loads `dxgi.dll`, `d3d11.dll`, `d3d12.dll`,
  `vulkan-1.dll`, `dxcompiler.dll` by name at run time (UTF-16/ASCII strings beside `CreateDXGIFactory`,
  `CreateDXGIFactory1/2`, `D3D11CreateDevice`, `D3D12CreateDevice`, `vkCreateInstance`) `[inferred-static 2026-10-06]`.
- Static imports that could serve as an early proxy instead: `WINMM.dll`, `DINPUT8.dll`, `XINPUT9_1_0.dll`,
  `HID.DLL`. `version.dll` is not imported.

## Renderer selection (§3, §9)
- Cvar is **`r_api`** (not the Enhanced Edition's `r_api_rx`). Read from the log routine at `0x140d8b659`:
  **2 = DirectX 11, 3 = DirectX 12, 4 = Vulkan**; any other value logs "DX9 selected but not supported!
  Switching to dx11" and runs DX11 `[inferred-static 2026-10-06]`.
- Command line: **`-force_rapi <n>`** overrides it ("try to force r_api: %d", then a warning if the applied value
  differs) `[inferred-static 2026-10-06]`. `r_enable_rapi_change 1` sits in the same start-up block.
- Safe mode (after a `BadQuit`) writes `r_api 2`, i.e. forces DX11, along with `raytrace 0`, `r_dlss 0`
  `[inferred-static 2026-10-06]`.
- The dev PC's `Saved Games\Metro Exodus\76561198819413687\user.cfg` currently holds **`r_api 3` (DX12)**;
  the live session already made `user.cfg.bak-2026-10-06-before-original-edition`. For DX11: `r_api 2`, or
  launch with `-force_rapi 2` `[inferred-static 2026-10-06]`. The original edition shares this folder with the
  Enhanced one `[hypothesis]` (only one `Metro Exodus` folder exists on this PC).
- A Vulkan backend exists here (`cbackend_Vulkan` and friends), unlike the Enhanced exe.

## Windowing and music (§4, §10)
- Present: `r_fullscreen` (cfg holds `on`), `r_res_hor`, `r_res_vert`, `r_vsync`, `r_enable_res_change`.
  No `borderless`/`windowed`/`-width`/`-height` strings `[inferred-static 2026-10-06]`. Same plan as before:
  `r_fullscreen off`, `r_res_hor 1280`, `r_res_vert 720`.
- Music key: **`s_music_volume`** (cfg currently `0.50`); neighbours `s_master_volume`, `s_effects_volume`,
  `s_dialogs_volume`, `s_vo_volume` `[inferred-static 2026-10-06]`. Set `s_music_volume 0` with the game closed.

## VR leftovers (§12)
- All present in this older exe too: `-vr_profile`, `vr_stereo`, `post_vr`, `-build_key` (with
  "Invalid build_key", "Empty build_key"), `oculus`, `oculus_touch_presets`, `allow_in_vr`, `vr_only`,
  `vr_scheme`, `vr_curve_*`, `vr_hand_speed`, `vr_bias_hmd_height`, the `vr_*` weapon-physics names, and
  `ovrsb_*` (pos/rot/size/reflect) `[inferred-static 2026-10-06]`. Whether they behave the same as in the
  Enhanced exe was not traced `[hypothesis]`. Because this edition runs on the dev PC, the `-build_key oculus`
  and `vr_stereo on` flat runs could now happen here instead of the home PC.

## Logging proxy (staging)
Folder: `staging/metro-exodus-vr/logging-proxy-2026-10-06/` (lanes proxy-gen 0.28.0, llvm-mingw clang).
- **Primary: `build/dxgi.dll`**, sha256 `88d7bf4ab83bc3afe27d380935c07c88ebf7f692a1fd6d02b6f42837ade4a566`,
  19/19 exports match System32 `[compile-verified 2026-10-06]`. Catches DX11 and DX12 both.
- Spare: `build-d3d11/d3d11.dll`, sha256 `b145b8b176080b42f6a0396a4873a2d0d1f18a248fadefadbd07a6a2a869206e`,
  51/51 exports match.
- proxy-gen self-test with both built files: ALL TESTS PASSED (factory and device created through each)
  `[verified-numerically 2026-10-06]`. Not yet loaded by the game.
- Log: `metroexodus_proxy_log.txt` next to `MetroExodus.exe` (falls back to `%TEMP%`). Both proxies use the same
  log name, so install one at a time. Forward target: the real `C:\Windows\System32\<dll>`.
