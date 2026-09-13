# First static look (2026-09-13)

Read from the installed Steam copy on the home PC, without launching the game. Every claim
below is `[inferred-static 2026-09-13]` unless tagged otherwise: it comes from reading file headers
and strings, not from running anything.

- **Install:** `D:\SteamLibrary\steamapps\common\Metro Exodus Enhanced Edition`, 72 GB.
- **Identity:** Metro Exodus Enhanced Edition, Steam app 1449560, build 24973569, fully downloaded (72 GB). Game exe `MetroExodus.exe`; `Benchmark.exe` sits beside it. No separate launcher exe.
- **Engine:** 4A Games' own 4A Engine `[reported]`; the exe carries the string `4A Engine` `[inferred-static 2026-09-13]`. Middleware shipped beside the exe: PhysX 3, NVIDIA HairWorks (Direct3D 11 and 12 builds), DLSS, Ansel, GeForce Experience SDK, BugTrap crash reporting, Corsair and Cg lighting SDKs, a telemetry DLL, and an unidentified `pros.sdk.x64.dll`.
- **Binary:** **64-bit** (PE32+), `MetroExodus.exe` 25.7 MB, header link date 2026-08-27 (a recent patch build). Ordinary sections plus `.bind` (the Steam DRM wrapper's section) `[inferred-static 2026-09-13]`.
- **Renderer:** **Direct3D 12 only**: `D3D12CreateDevice`, `CreateDXGIFactory2`, ray-tracing and DLSS strings, and the DirectX shader compiler (`dxcompiler_pc.dll`, `dxil.dll`) ships beside it. No Direct3D 11 or Vulkan device strings found in the exe. Direct3D 12 is not in the static import table, so it is loaded at run time `[inferred-static 2026-09-13]`. The Enhanced Edition requires a ray-tracing graphics card `[reported]`. Input: DirectInput 8, XInput and raw HID.
- **Protection:** The Steam DRM wrapper (`.bind`); no Denuvo, VMProtect or Themida string found `[inferred-static 2026-09-13]`. Not tested live.
- **Console:** About 350 console-variable-style names (`r_base_fov_option`, `r_res_hor`, `r_forcehudmode`, …) and `AllocConsole` are in the exe, so a developer console or config-variable system very likely exists `[inferred-static 2026-09-13]`. How to open it: unchecked.
- **Leftover VR code:** ⭐ **Leftover VR code is inside the exe.** A `-vr_profile` command-line string, dozens of VR tuning names (`vr_hand_speed`, `vr_grab_lerp_dur`, `vr_bias_hmd_height`, `vr_max_aim_angle`, `vr_noclip_dur`), `oculus_touch_presets`, "Negate VR HMD Offset", `allow_in_vr`, `post_vr`, and VR weapon classes (`weapon_item_vr_attach`, `vr_missile_weapon`) `[inferred-static 2026-09-13]`. 4A Games shipped a VR game, *Arktika.1* (2017), on this engine `[reported]`, which is the likely origin `[hypothesis]`. **No OpenVR, OpenXR or Oculus runtime DLL names were found**, so the headset connection itself may have been stripped and only the gameplay-side VR code left. Unchecked either way.
- **Other files:** Game content is in `.vfs` archives (`content_*.vfs0`–`vfs7`, most just under 2 GB each) indexed by `content.vfx`, plus `patch.vfx0`, `typed_strings.bin` and `sku_cfg.bin`. Not yet looked at.

## Method

PE header read with a short script: machine type, link timestamp, section names and sizes, and the
static import table. Then a search of the exe's strings for renderer names (`d3d11`, `d3d12`,
`dxgi`, `vulkan`), protection markers (`denuvo`, `vmprotect`, `themida`, `.bind`), console-variable
shapes (`r_*`, `g_*`) and VR words (`vr_`, `oculus`, `openvr`, `openxr`, `hmd`). A string match
shows a name is present in the file, not that the code path is used.

## Next static questions

1. Is `-vr_profile` a real launch option, and what does the exe do with it?
2. Are the `vr_*` names live settings, or labels left behind with no code under them?
3. Is there any trace of a headset runtime being loaded at run time (a DLL name built from pieces, a
   `LoadLibrary` near the VR code)?
4. How the console is opened, and whether `r_base_fov_option` is the field-of-view control.
