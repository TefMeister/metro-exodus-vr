# Engine Dossier — Metro Exodus Enhanced Edition (4A Engine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, first static look (2026-09-13); the game has not been launched yet. · **VR-readiness verdict:** TBD. Nothing seen so far rules it out, and the leftover VR code (§12) is a real head start if it is reachable.

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
- none yet.

## 12. Open risks toward the North Star
- ⭐ **Leftover VR code is inside the exe.** A `-vr_profile` command-line string, dozens of VR tuning names (`vr_hand_speed`, `vr_grab_lerp_dur`, `vr_bias_hmd_height`, `vr_max_aim_angle`, `vr_noclip_dur`), `oculus_touch_presets`, "Negate VR HMD Offset", `allow_in_vr`, `post_vr`, and VR weapon classes (`weapon_item_vr_attach`, `vr_missile_weapon`) `[inferred-static 2026-09-13]`. 4A Games shipped a VR game, *Arktika.1* (2017), on this engine `[reported]`, which is the likely origin `[hypothesis]`. **No OpenVR, OpenXR or Oculus runtime DLL names were found**, so the headset connection itself may have been stripped and only the gameplay-side VR code left. Unchecked either way.
- **Direct3D 12 with ray tracing always on** is the hardest renderer shape on the account so far: ray-traced lighting is worked out from the camera's position, so a second eye may not be as simple as drawing the scene twice `[hypothesis]`. Death Stranding (`death-stranding-vr`) is the only other Direct3D 12 project, and it has no stereo result yet.
- The Steam DRM wrapper hides the real start of the program until it has unpacked itself, so some static reading may have to wait for a running copy.
- The original (non-Enhanced) Metro Exodus has a Direct3D 11 path `[reported]`; this Enhanced Edition install does not appear to `[inferred-static 2026-09-13]`.

## Inbox folds, 2026-09-29

**Console route and VR prior art (`/gr` 2026-09-17).** No shipped console switch is known; a public Cheat Engine table (SunBeam, AltSierra117) patches the running game so F1 toggles the console `[reported]`. Hidden settings live in `Saved Games\Metro Exodus\user.cfg`, and console changes are not written back `[reported]`, which matters for the windowing job. Arktika.1 ran on the 4A Engine with Rift support, but no public source mentions the `vr_*` names in Exodus. Topic: `external-research/topics/2026-09-17-console-user-cfg-and-exodus-sdk.md`.

