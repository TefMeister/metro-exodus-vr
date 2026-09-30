# What `vr_stereo` does, the `-build_key oculus` switch, and the API/DXR question (static read, 2026-09-30)

From: PD reader helper, second pass on 2026-09-30. Static only: nothing launched or touched in the game
folder. Same build as the first drop (`2026-09-30-pd-reader-windowing-and-vr-stereo-cvar.md`).
Addresses are RVAs in `MetroExodus.exe`. Method: an x64 disassembly of every function that reads
the `vr_stereo` value (RVA 0x1651f08), found with a RIP-relative reference scan. This was **not**
a decompile, so read these as readings of the machine code.

## Short answer

Turning `vr_stereo` on does **not** give a two-eye picture in this build. It switches off some
effects, swaps the final post-process shader for `post_vr`, and stops the renderer preparing the
window's back buffer. The part that picks the eye and feeds it a pose is not there. Expect a black
or frozen window, or a crash, **not** side-by-side. `[inferred-static 2026-09-30]` for the code;
what shows on screen is `[hypothesis]`.

## (a) Two views? Eye offset, projection, HMD pose?

- **A per-view index exists but nothing drives it.** The renderer object (global at RVA 0x27c5050)
  has a field at +0x108c (absolute RVA 0x27c60dc), used as a view or eye index:
  - with `vr_stereo` on, index 0 picks resource +0xce8 and index 1 picks resource +0xcf0
    (RVA 0xdec375–0xdec3c4);
  - index ≠ 0 takes a cheaper path (mode 1 instead of 5, RVA 0xdcc57b).
  `[inferred-static 2026-09-30]`
- **The only write to that field in the whole exe sets it to −1** at the start of each frame
  (RVA 0xdd565a, in `crender::render`). All ten places using displacement 0x108c were checked. So
  in this build the index never becomes 0 or 1, and the two-eye branches are never taken.
  `[inferred-static 2026-09-30]` A write through a memcpy or struct copy cannot be ruled out
  statically `[hypothesis]`.
- **No eye offset, IPD, per-eye projection or HMD pose code was found.** No `ipd`, `eye_offset`,
  `left_eye`, `hmd_pose` or projection strings exist, and no OpenVR, OpenXR or LibOVR imports.
  The only HMD-named items are gameplay (`vr_bias_hmd_height`, "Negate VR HMD Offset").
  `[inferred-static 2026-09-30]` So the view and projection matrices for each eye would have to come
  from us.

## (b) What it looks like with no headset

What the ~20 checks do when `vr_stereo` is on `[inferred-static 2026-09-30]`:

- **Screen-space reflections forced off.** Five functions check it before `meta_ssr`
  (RVA 0xe3ad52, 0xe3dc81, 0xe3de52, 0xe3e8d5, 0xe3ec0f).
- **A sun or light test returns false** (RVA 0xd8a944).
- **The final post shader becomes `post_vr`** instead of `post_ldr_*` or `post_hdr*_scrgb`
  (RVA 0xe2bee0).
- **The swap-chain back buffer is not prepared.** Two resource-state transitions on the window's
  back buffer, one of them to state 0x400 (COPY_DEST), are skipped (RVA 0xdd35da). The same
  function has an `fxaa` resolve branch gated on it (RVA 0xdec991).
- **Two small render steps are skipped outright** (RVA 0xe34bd0 and 0xe34e30). They are also
  skipped when the build key is `oculus` (see (c)).
- A few other branches (RVA 0xdd2414, 0xdd255d) are gated alongside the `oculus` build key.

**Expected result** `[hypothesis]`: one normal-width view, rendered once and not side-by-side.
Because the back-buffer transition is skipped, it may never reach the window (black or frozen
window), and it may cause a D3D12 state error at present time. No double-width render target setup
was found.

## (c) What it depends on; startup or live

- **`-build_key oculus` is a real command-line switch** (parsed at RVA 0x56ff74). The only valid
  keys are `m3` (the default, Metro Exodus) and `oculus`; anything else logs
  `!Invalid build_key`. The chosen key is compared with `oculus` in **72 places across gameplay,
  UI and renderer code**, several right next to the `vr_stereo` checks. It looks like the build
  variant switch for the VR (Arktika-era) configuration. `[inferred-static 2026-09-30]` What it
  changes in play is unknown. It is the **stronger lead** of the two and is worth one flat test.
  Risk: unknown, and it may expect content the retail files lack `[hypothesis]`.
- **`_OCULUS_=1` shader define:** added to a shader lookup key when an engine flag (RVA 0x1696c2c)
  is set. The code that sets that flag was not found, and it is not visibly tied to `vr_stereo`.
  Whether `_OCULUS_` shader variants exist in the shipped shader cache is unchecked.
  `[inferred-static 2026-09-30]`
- **No other `vr_*` render setting feeds these checks.** The gameplay `vr_*` names are separate.
  `[inferred-static 2026-09-30]`
- **Live or startup:** the value is read directly every frame at every site, with no cached copy,
  so a live change should take effect on the next frame. Whether the per-eye resources (+0xce8 and
  +0xcf0) are only created when it is on at startup is unknown. Safest: set it in `user.cfg`.
  `[inferred-static 2026-09-30]`

## (d) Crash risk at start

Medium `[hypothesis]`:

1. The `post_vr` shader must be in the shader cache. If it is missing, the loader logs
   `! shader-blob not found` and returns an empty shader.
2. Skipping the back-buffer transition can leave the swap chain in the wrong state at present time.

Both would show at the first rendered frame, not at the menu load. Try it only where the game
already runs (the home PC, see §3), and keep `vr_stereo` in a separate test from windowing.

## 3. `r_api_rx`, `-force_rapi`, and whether DXR 1.1 is hard-required

- **`r_api_rx` values:** 0 = "DirectX 11 (Obsolete)", 1 = "DirectX 12", 2 = "Vulkan"
  (RVA 0xe138a7 table). **Only DirectX 12 has a backend factory** (RVA 0xdba8c7). Vulkan gives
  "Failed to find backend_factory method", and any value other than 1 or 2 gives
  "Failed to find supported DirectX API! Only DirectX 12 and Vulkan are supported". There is no
  Vulkan loader string (`vulkan-1.dll` or `vk*`) in the exe, and the Vulkan probe logs
  "supports" and then "isn't supported" straight after. `[inferred-static 2026-09-30]`
- **`-force_rapi <n>`** (RVA 0xdb9f74) asks for an API, but it is clamped to what the startup probe
  found and logged as "applied force r_api_rx". Safe mode's `r_api_rx 2` goes through the same
  clamp, so on a DirectX 12 machine it ends up as DirectX 12. `[inferred-static 2026-09-30]`
- **No DirectX 11 path and no non-ray-traced path.** The only D3D DLL string is `d3d12.dll`. There
  is no `d3d11.dll` or `D3D11CreateDevice`. The "Raytrace Legacy Mode" string has **no code
  references** (it is dead). `r_legacy_gather` exists but is not a renderer switch.
  `[inferred-static 2026-09-30]`
- **The DXR 1.1 check** is in the system-requirements function (RVA 0x56b1dc, called from RVA
  0x40c927). It checks shader model ≥ 6.5 (`0x65`), DXR 1.1 and 16-bit float support, and builds the
  message. The dialog (RVA 0x56b47c) relabels the Windows Yes/No/Cancel buttons as
  Open Link / Quit / **Run Anyway**.
  - Run Anyway (IDCANCEL = 2) **simply returns**. Nothing is disabled or changed.
  - The only side effect of the whole check is one bit (0x20) in an engine flags word, which
    comes from a caller argument, not from the button.
  `[inferred-static 2026-09-30]`
- **So yes, DXR 1.1 is effectively required.** Run Anyway skips nothing, and the renderer still
  builds DXR 1.1 work. That matches Tefa's dev-PC crash (about 6 min on the loader, then an access
  violation reading 0x18c inside `D3D12Core.dll` on a GTX 1660 SUPER). That the crash *is* a
  missing DXR 1.1 feature is `[hypothesis]`, but no code path avoids it. **The Enhanced Edition cannot
  be tested on the dev PC.** Static work can continue there, and anything live needs the home PC.
  The original (non-Enhanced) Metro Exodus, with its DirectX 11 path, is a separate product.

## Suggested next steps

- `[FLAT]`, on the home PC: `-build_key oculus` on its own, and note what changes (menus, HUD,
  input, any VR text).
- `[FLAT]`, on the home PC: `vr_stereo on` in `user.cfg` on its own, and screenshot the window.
  Expect it not to be stereo.
- `[PD]`: the two per-view resources (+0xce8, +0xcf0) and the `post_vr` pass are where a stereo
  injection would plug in: drive the +0x108c index ourselves and render twice. That is a design
  lead, not a finding.

Scripts: `staging/metro-exodus-vr/pd-reader-2026-09-30/` (`fn.py` lists the functions that read a
global and disassembles them).
