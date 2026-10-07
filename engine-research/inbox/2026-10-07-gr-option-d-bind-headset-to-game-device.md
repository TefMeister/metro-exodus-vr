# Option (d) for the keyed-mutex wall, plus a one-line check

From `/gr`, 2026-10-07. Topic: `external-research/topics/2026-10-07-skip-the-shared-texture-bind-the-headset-to-the-game-device.md`.

Dossier dead end: *"The device rejects every texture with `MISC_SHARED_KEYEDMUTEX` … Options, untried: (a) … (b) … (c) …"*

Suggested additions:
- **(d) no shared texture at all:** create the OpenXR session with the game's own `ID3D11Device` and
  `CopyResource` the back buffer into the swapchain image on the game's context. This is what
  REFramework's D3D11 path does `[inferred-static 2026-10-07]`. Cost: the game may be paced by the headset.
- **Before choosing, log one line:** does the device answer `QueryInterface(IID_ID3D11On12Device)`?
  `D3D12Core.dll` is loaded in DX11 runs; an 11on12 device would explain the refusal `[hypothesis]`.
