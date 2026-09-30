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

