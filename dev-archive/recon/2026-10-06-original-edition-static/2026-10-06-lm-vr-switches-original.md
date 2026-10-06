# VR switches and the camera, ORIGINAL edition exe (static), 2026-10-06

From: `/lm` reader helper, dev PC. Static file reading only (capstone over `.pdata` functions plus a RIP-relative
reference index). Exe: original Metro Exodus, Steam build 6544595, sha256
`d4ab0e9b076d324f6b8ddad601fd9dda68c0c593adb7b0019944d560bc9875a5`. Addresses are RVAs (image base 0x140000000).
Scripts: `staging/metro-exodus-vr/pd-reader-2026-10-06/` (`lib.py`, `fn.py`, `ctx.py`, `oc.py`, `wr.py`, `wr2.py`).
Folds into dossier §6, §9, §12 and answers the two `[PD]` rows for this edition.

## 1. `-build_key oculus`
- Parsed at 0xab73c3 into a string handle at 0x163213c. Valid values are `m3` and `oculus` `[inferred-static 2026-10-06]`.
- 72 compare sites in 70 functions (`oc.py`). Most have no nearby strings, so their purpose is unread. The readable ones:
  - ⭐ **DX11 output (0x2621a4, 0x261660):** `oculus` behaves exactly like the `-m1` switch. The DX11 swap chain goes to
    **output 1, the second monitor** ("DX11: m1: second monitor params…"). A window is then placed using the screen size
    (0x2615b0). That is Oculus **extended mode**, where a Rift DK2-era headset shows up to Windows as a second display
    `[inferred-static 2026-10-06]`. Live effect on a PC with one monitor: probably logs "second monitor not found" and
    carries on `[hypothesis]`.
  - Main scene render (0xd859f0): when `vr_stereo` is off and the key is `oculus`, it calls 0xdf6720
    (the `r_exposure_mode == 2` path). The two small passes 0xdf6990 and 0xdf6c40 are skipped when **either** is on.
  - A path builder (0xab684c) appends `\pc_01_citadel` for `oculus`, otherwise `\000`. Folder purpose unknown `[hypothesis]`.
  - Others sit in menu activation (0xb5511c), the loader/pause (0xb73e20), the actor camera (0x5725e0) and many
    unlabelled gameplay functions.
- **Next to `vr_stereo`:** only in 0xd859f0 and the two passes above.

## 2. `vr_stereo` in the DX11 path
- Cvar value at 0x16c4c78, default 0, read by 23 functions `[inferred-static 2026-10-06]`.
- **Eye index:** field +0x151c of the renderer block (absolute 0x211206c), read as -1 / 0 / 1 at about 45 sites.
  **Its only write is -1, in `crender::render` (0xd8a6e1), every frame.** The one other displacement match
  (0x95c6dc) is a stack frame. So **no code path renders two eyes**, same as the Enhanced exe `[inferred-static 2026-10-06]`.
- **No Oculus runtime:** no `LibOVRRT64_1.dll`, `ovr_*`, OpenVR or OpenXR strings anywhere `[inferred-static 2026-10-06]`.
- **What it does instead:**
  - It forces the renderer's "stereo active" flag (0x2112068) to 1 (0x25f910, 0xde4904). Normally that flag comes from
    **NVIDIA 3D Vision** (`NvAPI_Stereo_CreateHandleFromIUnknown`), gated by `r_dbg_stereo_auto_separation`, with a
    separation float. The `r_dbg_stereo_separation_base` and `r_dbg_stereo_separation_zoom` cvars exist. The projection
    code reads this flag (0xdcf3e6).
  - DX11 swap chain (0x261b30): when it is on, the swap-chain size is not written back.
  - It changes the render target picked with TAA (0x260033) and skips TAA jitter (0xde4707).
  - It turns SSR (`meta_ssr`) and filtered AO off (0xdf86b0), and changes the light test (0xdafd30 and its callers).
  - **`post_vr`** replaces the final post-process shader (0xdee53d).
  - Whether `post_vr` ships could not be checked, because the archive index names are not plain text.
- **Untested guess:** one normal view, possibly with the 3D Vision stereo maths turned on but no driver to use it
  `[hypothesis]`.

## 3. Per-frame camera (patch point for per-eye)
- **Global camera block** inside the renderer object (base 0x2110b50):
  - **view 0x2111640** (4×float4)
  - **projection 0x2111680**
  - **view×projection 0x21116c0**
  - double-precision copies from 0x2111700
  `[inferred-static 2026-10-06]`
- **Builder: 0xde46b0.** It is called from the main scene render 0xd859f0 (at 0xd87aa0) and from 0xd8961e and 0xd89925.
  It writes the projection, applies TAA jitter (gated by `vr_stereo` / `r_fxaa` / `r_taa_enabled`), multiplies view by
  projection at 0xde4ad9–0xde4c70, and sets the stereo flag. **This is where to swap in a per-eye view and projection
  before the multiply** `[inferred-static 2026-10-06]`.
- `r_base_fov` value at 0x162ebe4 (registered at 0xae3f88). Used with tan(fov/2) at 0xdcf3c6, next to a 4×4 inverse
  (0x9dac0) of the view matrix.
- Not found yet: the D3D11 constant-buffer upload (`cbuffer_manager`) that copies 0x21116c0 to the GPU. Next step:
  follow the readers of 0x21116c0 into Map/UpdateSubresource.
