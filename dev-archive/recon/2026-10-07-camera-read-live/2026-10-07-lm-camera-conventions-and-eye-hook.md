# Original edition: camera conventions, DX11 constant path, first per-eye hook (2026-10-07)

From: `/lm` reader helper, dev PC. Static file reading only (exe sha256 `d4ab0e9b...a5a5`, build 6544595); the
running game was not touched. Scripts reused: `staging/metro-exodus-vr/pd-reader-2026-10-06/lib.py`.
Folds into: dossier §6 (camera), §7 (constant buffers), §12; extends the 2026-10-06 section.
All RVAs below are image-relative (add the exe base).

## Matrix conventions `[inferred-static 2026-10-07]`
- Row-major float4x4, **row-vector maths (v * M)**, translation in row 3 (`M[3][0..2]`, bytes +0x30..+0x3b).
  Proof: `0xde46b0` builds P' = P * J with J's jitter in row 3, then VP = V * P' (lane-wise `shufps` broadcast of
  each row of the left matrix); render-state pushers `0x198460`/`0x198770` compute V*P the same way.
- **Left-handed** (projection row 2 = `[0,0,Q,1]`, camera looks down +Z) and **reversed-Z**: the default projection
  builder (`0xd892f0`, fallback branch) uses `Q = n/(n-f)`, `M[3][2] = -f*Q` with n=0.1 (`0x162ebe8`), f=100 →
  depth 1 at the near plane, 0 at the far one; finite far in that builder. Main-camera projection comes from a
  virtual (`[obj]+0x400`) not traced, so its far value is unknown `[hypothesis: same form]`.
- `r_base_fov` (`0x162ebe4`, 60) is the **vertical** FOV in degrees: `ys = 1/tan(fov*pi/360)`, `xs = ys/aspect`.
- Camera object = **`0x2111600`** (size 0x4d0, ctor `0xb7deb0`; siblings at `0x2111130`, `0x2111ad0`):
  +0x00 position (xyz), +0x10 forward, +0x20/+0x30 other basis vectors `[hypothesis]`, **+0x40 V, +0x80 P,
  +0xC0 VP**, +0x100 V in **double** (4x4, `0x2111700`), +0x180 double V*P (`0x2111780`, written by `0xde46b0`),
  +0x4b4 FOV, +0x4b8 aspect. Unjittered P copy: `0x2111fe0` (and `0x2110a90`).
- P is **TAA-jittered in place** by `0xde46b0` (only when two TAA flags `0x16df308`/`0x16df218` are set); it runs at
  the END of the scene render `0xd859f0` (called once, from `0xd8828e`).
- Inverse V / inverse P / inverse VP are made by the backend, not stored as globals (set-view `0xd80320` stores V at
  ctx+0xb0 and inverse at ctx+0x170). No previous-frame VP constant name was found.

## DX11 path to the GPU `[inferred-static 2026-10-07]`
- The game records commands in a stream at `0x16c0c40` (opcodes `0x7000xxxx`; **0x19 = set view, 0x1A = set
  projection**, 0x18 = set world). Full buffers go to the backend's slot 0x370 (executor).
- Backends: **DX11 = vtable `0x14e3cd0`** (executor `0x263e60`, set-view slot 0x80 → `0x256910`, set-proj 0x88 →
  `0x256ea0`); DX12 = `0x14e5a50`; Vulkan = `0x14e5000`.
- DX11 set-view writes the matrices **transposed** into a CPU shadow of the global constants (`*(0x1764d58)` +0x140
  + register*16, dirty bits at +0x10, one bit per cbuffer); string `dispatch_cbmap` sits in the upload code.
- Shader constant names (looked up by name, `0xf8d8d0`): **`m_W m_V m_P m_iW m_iV m_iP m_WV m_VP m_WVP m_iVP`**,
  plus `surf_params`, `m_screen`. Shaders are packed (compressed) in the `.vfs` archives, so no DXBC reflection.

## Eye hook (staging `eye-hook-2026-10-06/`, not deployed) `[compile-verified 2026-10-07]`
- `build/metro_eye.dll` (sha256 `8d0251bd3b48...e97c`): MinHook on `0xd859f0`; per frame shifts `V[3][0]` by
  -side*half_ipd (and the double copy), rebuilds VP, renders, then undoes only its own shift. Alternates L/R;
  numpad 5 = on/off, numpad 8 = alternate / left only / right only; `metro_eye.ini` knobs; refuses to hook unless
  the exe bytes match. Logs before/after numbers to `metro_eye_log.txt`; state block exported as `g_eye`
  (magic `MEYE0001`).
- `build/dxgi.dll` (sha256 `76d0c7688b4c...c537`): the logging proxy plus a thread that loads `metro_eye.dll`
  from the exe folder; 19/19 exports.
- Default 0.032 assumes metres `[hypothesis]` (near plane 0.1 in the fallback builder fits metres).
- Expect TAA to smear the two eyes together while alternating: test with TAA off (`r_taa_enabled 0`
  `[hypothesis]`) or with a fixed eye.
