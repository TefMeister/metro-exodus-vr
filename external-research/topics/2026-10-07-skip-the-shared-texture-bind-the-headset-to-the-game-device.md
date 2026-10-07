# Skip the shared texture: give the headset runtime the game's own D3D11 device

**Status:** 🆕 new · **Priority:** high — a fourth option for the top `[PD]` row, and the one a shipping VR mod uses.

## The problem it answers

The dossier records that Metro's DX11 device refuses every texture with `MISC_SHARED_KEYEDMUTEX`
(`E_INVALIDARG`) and accepts `MISC_SHARED` and `SHARED | NTHANDLE` `[verified-live 2026-10-07, n=1]`, so
The Evil Within's handover (a separate headset device, keyed-mutex shared textures) cannot be reused.
The board lists three ways round it: (a) make the textures on the headset device, (b) plain shared
textures with a GPU event query, (c) a CPU copy.

## Option (d): no second device at all

praydog's REFramework (the VR layer under our RE2 and Village work) does not share textures between
devices on D3D11. In `src/mods/vr/D3D11Component.cpp`, `OpenXR::initialize` sets
`binding.device = hook->get_device()` — **the game's own hooked device** — in the
`XrGraphicsBindingD3D11KHR` it hands to `xrCreateSession`, and each frame it does a plain
`context->CopyResource` from the game's back buffer into the OpenXR swapchain image `[inferred-static
2026-10-07, read from the public source]`. No keyed mutex, no shared handle, nothing for Metro's device to
refuse.

**The cost:** OpenXR's frame calls then run against the game's device, so `xrWaitFrame` can pace the
game to the headset. TEW's design deliberately kept the game from ever waiting on the headset. REFramework
lives with that trade; for a first picture in the simulator it is the shortest path, and it can be
replaced by (a) or (b) later if the pacing hurts.

## A cheap diagnostic worth one log line

The dossier also notes that **`D3D12Core.dll` is loaded** in a DX11 run. Plain D3D11 devices normally
accept keyed-mutex textures; if Metro's "DX11" device is actually a **D3D11On12** device, the refusal
would make sense, since Microsoft's 11on12 layer has documented restrictions around keyed-mutex resources
(Chromium's Dawn code notes that keyed-mutex resources cannot be unwrapped from 11on12) `[hypothesis]`.
Test: `QueryInterface(device, IID_ID3D11On12Device)` and log the result. If it succeeds, (d) or a native
D3D12 binding is the natural route; if it fails, the cause is elsewhere and nothing is lost.

General D3D11 rules that rule out other causes `[reported]`: keyed-mutex sharing needs `USAGE_DEFAULT`
(the bridge already uses it), is unavailable on WARP/REF devices, and `SHARED` and `SHARED_KEYEDMUTEX`
are mutually exclusive.

## Sources

- praydog, REFramework, `src/mods/vr/D3D11Component.cpp` / `.hpp` (MIT) — <https://github.com/praydog/REFramework>
- Dawn (Chromium), `D3D11on12Util.cpp` — <https://dawn.googlesource.com/dawn/+/180ec459ea79f3be400a80f270920a243940db1a/src/dawn_native/d3d12/D3D11on12Util.cpp>
- Microsoft, `D3D11_RESOURCE_MISC_FLAG` — <https://msdn.microsoft.com/de-de/library/ff476203(v=vs.85)>
- Staging/keyed-mutex limitation discussion — <https://windows-hexerror.linestarve.com/q/so60706884-a-d3d11usagestaging-resource-cannot-be-shared-via-d3d11resourcemiscsharedkeyedmutex>
