# Engine Dossier — Metro Exodus Enhanced Edition (4A Engine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0. First launch 2026-09-30 on the dev PC crashed before the main menu (no DXR 1.1 on its card); all live work is home-PC only. · **VR-readiness verdict:** TBD. The renderer still holds a dormant two-eye path and a `-build_key oculus` build variant (§12), but no headset code and no per-eye maths.

## 1. Identity
- Game / build / version: Metro Exodus Enhanced Edition, Steam app 1449560, build 24973569, fully downloaded (72 GB). Game exe `MetroExodus.exe`; `Benchmark.exe` sits beside it. No separate launcher exe.
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: 4A Games' own 4A Engine `[reported]`; the exe carries the string `4A Engine` `[inferred-static 2026-09-13]`. Middleware shipped beside the exe: PhysX 3, NVIDIA HairWorks (Direct3D 11 and 12 builds), DLSS, Ansel, GeForce Experience SDK, BugTrap crash reporting, Corsair and Cg lighting SDKs, a telemetry DLL, and an unidentified `pros.sdk.x64.dll`.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.): see above.
- Distinctive file formats / build tags / symbol naming: Game content is in `.vfs` archives (`content_*.vfs0`–`vfs7`, most just under 2 GB each) indexed by `content.vfx`, plus `patch.vfx0`, `typed_strings.bin` and `sku_cfg.bin`. Not yet looked at.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **64-bit** (PE32+), `MetroExodus.exe` 25.7 MB, header link date 2026-08-27 (a recent patch build). Ordinary sections plus `.bind` (the Steam DRM wrapper's section) `[inferred-static 2026-09-13]`.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: **Direct3D 12 only**: `D3D12CreateDevice`, `CreateDXGIFactory2`, ray-tracing and DLSS strings, and the DirectX shader compiler (`dxcompiler_pc.dll`, `dxil.dll`) ships beside it. No Direct3D 11 or Vulkan device strings found in the exe. Direct3D 12 is not in the static import table, so it is loaded at run time `[inferred-static 2026-09-13]`. The Enhanced Edition requires a ray-tracing graphics card `[reported]`. Input: DirectInput 8, XInput and raw HID.
- Developer console / cvar system present? how opened?: About 350 console-variable-style names (`r_base_fov_option`, `r_res_hor`, `r_forcehudmode`, …) and `AllocConsole` are in the exe, so a developer console or config-variable system very likely exists `[inferred-static 2026-09-13]`. How to open it: unchecked.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: The Steam DRM wrapper (`.bind`); no Denuvo, VMProtect or Themida string found `[inferred-static 2026-09-13]`. Not tested live.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**:
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from:
- The per-eye override maths (`K_eye = …`):

## 7. Constant-buffer fill mechanism
- Map/DISCARD ring / UpdateSubresource / D3D11.1 offset / **persistent map +
  memcpy** (trap):
- Can source contents be read cheaply (captured CPU pointer) or need staging
  read-back?:
- The chosen override patch point and why:

## 8. Pass inventory (by render target)
- Main scene (res/formats):
- Shadow passes (depth-only sizes):
- Post / AA chain (SMAA/TAA/motion vectors; downscale sizes):
- UI / HUD (how it's kept separate):

## 9. cvar / console cheat sheet
| command / cvar | effect | use |
|---|---|---|
| | | |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene (commands used):
- In-process input / camera drive method that worked:
- Frame-capture method; where images land:

## 11. Dead ends & false leads (save future time)
- **The dev PC cannot run the Enhanced Edition.** GTX 1660 SUPER: the game warns "does not support DXR1.1", Run Anyway plays the intros, the title screen builds shaders for ~6 min, then an access violation inside `D3D12Core.dll` `[verified-live 2026-09-30, n=1]`. The exe has no DirectX 11 or non-ray-traced renderer: `r_api_rx` 0 = "DirectX 11 (Obsolete)" is refused, 2 = Vulkan has no backend, and "Run Anyway" changes no setting `[inferred-static 2026-09-30]`. Evidence: `dev-archive/recon/2026-09-30-first-launch-dev-pc/`.
- **`-vr_profile` is not a headset switch.** It creates 17 GPU objects, most likely timers for profiling `[hypothesis]`.

## 12. Open risks toward the North Star
- ⭐ **Leftover VR code is inside the exe.** A `-vr_profile` command-line string, dozens of VR tuning names (`vr_hand_speed`, `vr_grab_lerp_dur`, `vr_bias_hmd_height`, `vr_max_aim_angle`, `vr_noclip_dur`), `oculus_touch_presets`, "Negate VR HMD Offset", `allow_in_vr`, `post_vr`, and VR weapon classes (`weapon_item_vr_attach`, `vr_missile_weapon`) `[inferred-static 2026-09-13]`. 4A Games shipped a VR game, *Arktika.1* (2017), on this engine `[reported]`, which is the likely origin `[hypothesis]`. **No OpenVR, OpenXR or Oculus runtime DLL names were found**, so the headset connection itself may have been stripped and only the gameplay-side VR code left. Unchecked either way.
- **Direct3D 12 with ray tracing always on** is the hardest renderer shape on the account so far: ray-traced lighting is worked out from the camera's position, so a second eye may not be as simple as drawing the scene twice `[hypothesis]`. Death Stranding (`death-stranding-vr`) is the only other Direct3D 12 project, and it has no stereo result yet.
- The Steam DRM wrapper hides the real start of the program until it has unpacked itself, so some static reading may have to wait for a running copy.
- The original (non-Enhanced) Metro Exodus has a Direct3D 11 path `[reported]`; this Enhanced Edition install does not appear to `[inferred-static 2026-09-13]`.

## Inbox folds, 2026-09-29

**Console route and VR prior art (`/gr` 2026-09-17).** No shipped console switch is known; a public Cheat Engine table (SunBeam, AltSierra117) patches the running game so F1 toggles the console `[reported]`. Hidden settings live in `Saved Games\Metro Exodus\user.cfg`, and console changes are not written back `[reported]`, which matters for the windowing job. Arktika.1 ran on the 4A Engine with Rift support, but no public source mentions the `vr_*` names in Exodus. Topic: `external-research/topics/2026-09-17-console-user-cfg-and-exodus-sdk.md`.

## Inbox folds, 2026-09-30

Two static reads by the `/lm` reader helper; full detail with code addresses in
`dev-archive/recon/2026-09-30-first-launch-dev-pc/2026-09-30-pd-reader-*.md`.

- **Static reading works despite the Steam wrapper**: the code section is not encrypted `[inferred-static 2026-09-30]`.
- **Windowing (§4, §10):** `user.cfg` in `Saved Games\Metro Exodus\<steamid>\` is run as a console script at every start. Candidate lines `r_fullscreen off`, `r_res_hor 1280`, `r_res_vert 720`. No borderless setting, no command-line window switch `[inferred-static 2026-09-30]`; untested live.
- **Crash trap (§10):** a crash sets `HKCU\Software\4A-Games\Metro Exodus\BadQuit` to 1 `[verified-live 2026-09-30, n=1]`, and the next start then offers safe mode, which lowers every graphics setting `[inferred-static 2026-09-30]`. Reset it to 0 before an unattended relaunch.
- **Launch switches (§9):** `-forcelog`, `-logpath <dir>`, `-nocrashdlg`, `-map <name>`, `-build_key`, `-force_rapi`, `-benchmark` and more; effects inferred from names only.
- ⭐ **`vr_stereo` (§12):** a real renderer setting, default off, read every frame by ~20 functions. On, it swaps the last screen shader for `post_vr`, turns some effects off and skips the present-preparation step. The eye-number slot it would use is only ever written as -1, so the two-eye branches never run: **no stereo picture as-is** `[inferred-static 2026-09-30]`. No eye offset, IPD, per-eye projection or headset pose exists; those would be ours. Medium crash risk at the first frame `[hypothesis]`.
- ⭐ **`-build_key oculus` (§12):** a real launch switch; values `m3` (default) and `oculus`, checked in 72 places across gameplay, menus and rendering, several beside the `vr_stereo` checks `[inferred-static 2026-09-30]`. Probably the Arktika-era VR build variant `[hypothesis]`. The strongest lead so far; needs one flat run on the home PC.


## 2026-10-06 (`/lm`, dev PC): the ORIGINAL edition runs here — first live session

The original 2019 edition (Steam appid 412020, build 6544595, `E:\SteamLibrary\steamapps\common\Metro Exodus`, 71 GB)
was installed on the dev PC for this project, because the Enhanced Edition cannot run on its GTX 1660 SUPER.
Full helper notes (folded from inbox, kept whole): `dev-archive/recon/2026-10-06-original-edition-static/`.

**First-run checklist, all done** `[verified-live 2026-10-06]`:
1. **Runs as shipped**: `steam://run/412020` → intro films (Escape skips each) → main menu (n=2).
2. **Runs with our file**: logging `dxgi.dll` proxy (staging `logging-proxy-2026-10-06`, `88d7bf4ab83b`, 19/19
   exports) loads and passes every call through (n=1). The exe loads `dxgi`/`d3d11`/`d3d12`/`vulkan-1` by name at run
   time; nothing is imported up front `[inferred-static 2026-10-06]`.
3. **Windowed 1280×720**: `user.cfg` `r_fullscreen off` gives a captioned window the size of the desktop (the game
   ignores `r_res_hor/r_res_vert` for the window); `SetWindowPos` to a 1280×720 client area then works, the picture
   fills it, the desktop stays 1920×1080 (n=1). **Needs Tefa's confirmation** (rule).
4. **Music muted**: `s_music_volume 0.00` in `user.cfg`, kept by the game (n=2).
- `user.cfg` lives in `%USERPROFILE%\Saved Games\Metro Exodus\<steamid>\` and is SHARED with the Enhanced Edition;
  the game rewrites it at start and exit. Backup: `user.cfg.bak-2026-10-06-before-original-edition`.
- Menus: arrows + Enter (the small screen names the selected button); the game's pointer ignores absolute mouse
  moves. Quit: main menu Escape → QUIT GAME → Enter. ⚠️ Enter on the main menu acts on NEW GAME by default.

**Renderer: Direct3D 12 by default, and `r_api` in user.cfg cannot change it.**
- Live: with `r_api 2` in user.cfg the game still created a D3D12 device and loaded `NvHairWorksDx12.win64.dll`
  `[verified-live 2026-10-06, n=1]`. (`D3D12Core.dll` alone proves nothing: every start makes a test DX12 device.)
- Static: the pick is at RVA `0xd8cf23`; `r_api` 2 = DX11, 3 = DX12 (built-in default), 4 = Vulkan; `r_api` accepts
  one change per start and renderer creation spends it before user.cfg applies `[inferred-static 2026-10-06]`.
  **`-force_rapi 2` on the command line** is read inside renderer creation and should give DX11
  (log `* [render] DX11 API selected`) — **not tested**: starting `MetroExodus.exe` directly with arguments exits
  silently (Steam wrapper), and `steam://run/412020//-force_rapi 2` brings up Steam's launch-options confirmation,
  which Tefa must press once. Or Tefa adds `-force_rapi 2` to the game's Steam launch options.

**VR leftovers in the original exe** `[inferred-static 2026-10-06]`:
- `-build_key oculus` (72 checks): its clearest effect is in DX11 window setup, acting like `-m1` — the window moves
  to the SECOND monitor (old Oculus "extended mode", the Rift as a second screen). Also a `\pc_01_citadel` path
  suffix and some menu/loading/camera changes. It meets `vr_stereo` only in the main scene renderer and two passes.
- `vr_stereo` **never draws two eyes**: eye index only ever -1; no LibOVR/OpenVR/OpenXR anywhere. It sets the
  renderer's "stereo active" flag (normally NVIDIA 3D Vision), swaps the final shader for `post_vr`, turns off SSR,
  filtered AO and TAA jitter, and changes DX11 swapchain sizing.
- **Camera to patch per eye (CPU side, works for DX11 and DX12 alike):** view matrix at RVA `0x2111640`, projection
  `0x2111680`, view×projection `0x21116c0`, built each frame by `0xde46b0` (called from the main scene render
  `0xd859f0`); swapping a per-eye view/projection before the multiply (`0xde4ad9`–`0xde4c70`) is the patch point.
  `r_base_fov` at `0x162ebe4`. Where DX11 copies them into a constant buffer: not found yet.
- Copy protection: only the Steam wrapper (`.bind`); code not encrypted; no Denuvo/VMProtect/Themida strings.

- **2026-10-07: DirectX 11 confirmed.** Tefa put `-force_rapi 2` in the game's Steam launch options; started with
  `steam://run/412020` the process command line carries it and `NvHairWorksDx11.win64.dll` loads (no Dx12 one)
  `[verified-live 2026-10-07, n=1]`. Window resized to 1280×720 the same way.

## 2026-10-07 (`/lm`, dev PC, DirectX 11): the camera read live, and TWO EYES ALTERNATE

**Camera read live** `[verified-live 2026-10-07, n=1]` (`dev-archive/recon/2026-10-07-camera-read-live/`): 16 floats at
RVA `0x2111640` (view), `0x2111680` (projection), `0x21116c0` (view×projection), read-only with ReadProcessMemory.
Row-vector layout (v × M), translation in the bottom row; the 3×3 is orthonormal; a small mouse turn right moved the
forward axis ~8°. Projection in play: `sy = 1.7321` (60° vertical), `sx = sy·720/1280`, clip w = view z, clip z = 0.1
→ **reversed-Z with near 0.1** (far infinite or very far); row 2 carries the TAA jitter each frame.
Static detail (reader, folded from inbox, file kept in that folder) `[inferred-static 2026-10-07]`: camera object at
`0x2111600` (+0x00 position, +0x10 forward, +0x40 V, +0x80 P, +0xC0 VP, +0x100 double V, +0x180 double VP, +0x4b4
fov, +0x4b8 aspect); `r_base_fov` is the vertical fov in degrees; inverse matrices are computed inside the renderer,
not stored; no previous-frame VP found. GPU path: command stream at `0x16c0c40` (0x19 set view, 0x1A set projection)
→ DX11 renderer table `0x14e3cd0` → `0x256910` / `0x256ea0` write them transposed into a CPU copy of the shader
constants (`m_V m_P m_VP m_iV m_iP m_iVP m_W m_WV m_WVP m_iW`). Shaders are compressed inside the `.vfs` archives.

**Two eyes** `[verified-live 2026-10-07, n=1]` (`dev-archive/recon/2026-10-07-two-eyes-first-run/`): the reader's
`metro_eye.dll` (staging `eye-hook-2026-10-06`, `8d0251bd3b48`), loaded by an edited `dxgi.dll` proxy
(`76d0c7688b4c`, 19/19 exports), hooks the scene render `0xd859f0`; each frame it moves the camera half an eye
(`half_ipd`, default 0.032) along its right axis, also the double view copy, rebuilds view×projection (culling
matches), draws, then takes back its own shift. Signature-checked before hooking. Live: 24 grabs ~11 ms apart in
alternate mode split into two groups every other frame, far scenery 2 px apart, the gun 3–4 px (near separates
more: correct order). The first-person gun is drawn in the same space, so it shows parallax too.
Controls: numpad 5 on/off, numpad 8 mode (alternate / left only / right only); `metro_eye.ini` next to the exe.
Installed with `enabled=0`. TAA was on and did not visibly smear the two eyes in the grabs (not examined closely).
Units: 0.032 assumed metres (near 0.1 fits) `[hypothesis]`.

## 2026-10-07 (`/lm`, dev PC): the HEADSET BRIDGE runs; the game picture cannot be shared yet

Folded from inbox `2026-10-07-pd-headset-bridge-port.md` (the reader's port) plus this session's live runs.
Evidence: `dev-archive/recon/2026-10-07-headset-bridge-first-run/`.

**The port** `[compile-verified 2026-10-07]`: staging `headset-bridge-2026-10-07`, The Evil Within's OpenXR bridge
(`cd9efc2`: own D3D11 device + session on a headset thread, a shared texture per eye, game-swapchain filter) added to
`metro_eye.dll`; head tracking not ported. Off unless `metro_eye.ini [xr] openxr=1`. Present/Present1 hooked through a
throwaway swapchain. Eye pairing: each scene render (`0xd859f0`) queues its side, each game Present takes the oldest
`[hypothesis: holds only if every scene render is presented exactly once; untested because no game picture flows]`.

**Live** `[verified-live 2026-10-07, n=1 each]`:
- Game swapchain (main menu, window not resized): 1920x1061, `DXGI_FORMAT_R8G8B8A8_UNORM` (28), 3 buffers, flip
  discard (4), no MSAA, device creation flags 0, feature level 11_1. Present runs on the render thread.
- **Never call a window function that sends a message from the render thread**: `GetWindowTextA` on the game window
  deadlocked it against the main thread (main waits on exe lock `+0x2113630`, owned by the render thread).
  `InternalGetWindowText` is safe.
- The OpenXR simulator shows only projection layers: use `layers=projection` there. With it the red/blue test
  pattern runs at 60 fps beside the game.
- **The device rejects every texture with `MISC_SHARED_KEYEDMUTEX`** (`E_INVALIDARG`) and accepts `MISC_SHARED` and
  `MISC_SHARED | MISC_SHARED_NTHANDLE`. So TEW's keyed-mutex handover cannot be used on Metro as is. Options, untried:
  (a) create the keyed-mutex textures on the headset device and only OPEN them on the game device; (b) plain shared
  textures with a GPU event query and two textures per eye taking turns, no keyed mutex; (c) a CPU copy (slow, but
  enough to see a picture).
- OBS records both windows (game + simulator) into separate files (`claude-memory/tools/obs-rec.py --also`).
- While a test runs, `steam://run/412020` started DX11 even though the Steam launch options read empty here
  `[measured 2026-10-07]` (`present_hook` got an ID3D11Device); D3D12Core.dll is also loaded in the process.
