# How to get DX11 on the original edition: `-force_rapi 2`, not user.cfg (static), 2026-10-06

Supersedes: 2026-10-06-lm-original-edition-recon.md §"Renderer selection" (the line "For DX11: `r_api 2`, or launch with `-force_rapi 2`")

From: `/lm` reader helper, dev PC. Static reading only. Same exe (sha256 `d4ab0e9b…75a5`). Addresses are RVAs.

Live observation it explains (the `/lm` session's): `user.cfg` held `r_api 2`, the game rewrote the file and kept `r_api 2`,
yet it loaded `NvHairWorksDx12.win64.dll` (DX12) `[verified-live 2026-10-06, n=1]`, reported by the coordinator.

- **The pick:** in renderer "create & configure" (0xd8cd80), at 0xd8cf23: `r_api` (value at 0x16c5318, default **3**,
  range 0–4) maps 2 → DX11 backend factory 0x255540, 3 → DX12 0x297e90, 4 → Vulkan 0x266bd0 `[inferred-static 2026-10-06]`.
- **The `r_api` setter has a lock.** The set handler (0x1a2f40) ignores a new value if `-force_rapi` was applied
  (flag 0x16c531c) or if a value was already applied (0x16c531d). After a set it locks. `r_enable_rapi_change` (0x1a2fa0)
  only clears that lock. Renderer create also locks it (0xd8ce88) `[inferred-static 2026-10-06]`.
- **Why user.cfg did not work:** start-up runs `r_enable_rapi_change 1` → `config_load user.cfg` (0xacb692 to 0xacb6c1).
  The live result (DX12 chosen, but the cvar still 2 when the file was saved) fits the renderer being created **before**
  user.cfg is applied: create takes the default 3 and locks, then the unlock and user.cfg set the cvar to 2 too late.
  So `r_api` in user.cfg would not take effect at start `[hypothesis]`; the creation order was not traced statically.
- **Not evidence of DX12:** `D3D12Core.dll` is loaded anyway. The capability probe (0xe1c1d0 → 0x297c70) creates a test
  DX12 device on every start. `NvHairWorksDx12` is only loaded from DX12 backend code (0x2b22d0), so that one is real
  evidence `[inferred-static 2026-10-06]`.
- ⭐ **The DX11 switch: launch with `-force_rapi 2`.** It is read **inside** renderer creation (0xd8cf1e → 0xd8b370),
  immediately before the pick. It ignores the lock, clamps only to [0, highest supported API], logs
  `* [render] try to force r_api: 2` and `applied force r_api: 2`, and sets 0x16c531c so nothing later can change it.
  Expected log line: `* [render] DX11 API selected` `[inferred-static 2026-10-06]`; untested live.
  - The value must be a separate word after a space: `-force_rapi 2`.
