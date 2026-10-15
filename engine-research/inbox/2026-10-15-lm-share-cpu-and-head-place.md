# 2026-10-15 (`/lm` reader, dev PC, no game launched by the reader): LOCK vs RING read from the log, the CPU way built, the head-place fix

## What the b005 log said (read from `metro_eye_log.txt`, runs at 15:50 and 16:01)
- **LOCK fails on Metro at the OPEN step**: the headset device makes the keyed-mutex textures fine, then the game
  device's `OpenSharedResource1` returns `E_INVALIDARG` (`0x80070057`), log `mxr share: LOCK failed at the game device
  opening the headset's keyed-mutex texture` `[verified-live 2026-10-15, n=2 runs]`. So Metro's device refuses keyed
  mutexes both when making AND when opening them.
- **RING opens on both sides and pictures flow**: `mxr ring: sharing 1920x1080 ... NT handles`, `mxr ring: WORKS on the
  headset side`, diag `serial L 2270/2270 R 2270/2270`, headset pulls close to game copies, `slow 0`
  `[verified-live 2026-10-15, n=2 runs]`. Whether the picture LOOKS right is a visual question this note does not answer.
- The game device answers `ID3D11On12Device`: **no** (`hr 0x80004002`), `ID3D11Device1` yes, feature level 11_1,
  flags 0 `[verified-live 2026-10-15, n=2]`. So the keyed-mutex refusal is not explained by DX11-on-DX12.
- In the 15:50 run `game copies` stopped at 8479 from 15:52:39 while headset frames carried on: the game stopped
  presenting, or our hook stopped seeing its Presents (pause / minimise / loading?) `[hypothesis]`.

## The fallback for "LOCK and RING both fail": share=cpu (built, not deployed)
staging `metro-exodus-vr/share-cpu-2026-10-15/` (commit `cd22e64`), `metro_eye.dll` `df777c76fe9f`
`[compile-verified 2026-10-15]`.
- The dossier's option (d) (the OpenXR session on the game's own device) was **not built**: it is The Evil Within's
  recorded dead end on this same simulator (froze twice, 2026-10-06), and the simulator draws its D3D11 preview with
  the session device, which would put the runtime on the game's immediate context from another thread
  `[inferred-static]`. Option (c), the CPU copy, needs nothing either device can refuse, so that is what was built.
- How it works: the game copies each picture into a STAGING texture (3 in flight per eye), reads finished ones back
  with `Map(DO_NOT_WAIT)` on later Presents (never waits), copies the rows into 3 memory pictures per eye (same
  three-picture rule as RING, `mxr_ring.c`), the headset uploads the newest with `UpdateSubresource`. Cost: one
  picture (8.3 MB at 1080p) copied on the game thread per Present, about one frame more delay than RING.
- `share=auto` is now LOCK -> RING -> CPU; `share=cpu` forces it; `share=ring` stays RING (logs that it did not move
  on); `share=lock` = LOCK -> RING only.
- **Two-device test** (`tests/share_d3d_test.c`): a "game" and a "headset" D3D11 device on the GTX 1660 SUPER, 1500
  numbered solid-colour frames with a resize mid-run, every pixel of every received picture checked. LOCK, RING, CPU
  and a forced LOCK->RING->CPU switch each: ~1,490 pictures, 0 torn, 0 wrong eye, 0 backwards, 0 wrong size; lag
  ~1.0 (LOCK), ~1.6 (RING), ~2.6 (CPU) frames `[verified-numerically 2026-10-15, n=2 runs of each]`. On an ordinary
  device LOCK works, so Metro's refusal is specific to Metro's device. This also answers RING's open `[hypothesis]`
  for this card: a finished event query WAS enough for the other device to read the texture whole, under this load
  `[verified-numerically 2026-10-15, n=2]` (not yet with Metro's own device).

## The head-place fix (built, not deployed)
staging `headset-bridge-2026-10-07` commit `1493c8e`, `metro_eye.dll` `2e8cf7e10db7` `[compile-verified 2026-10-15]`.
- Live (main session): with `head_tracking=1` the camera rose 1.7 m into the tunnel ceiling; simulator head at y=0
  gave a normal view `[verified-live 2026-10-15, n=1]`.
- The old code already subtracted the place held at the recentre: run against the new tests it passes "1.7 m at the
  recentre = no move" and "a step 0.1 right = 0.1 right" `[verified-numerically 2026-10-15]`. It fails only when the
  pose it recentred on read 0 0 0, and then lifts exactly 1.7. `publish_head` writes 0 0 0 for a pose WITHOUT a valid
  position, so the likeliest cause is the recentre taking its place from such a pose (or from a moment the head really
  was at 0) `[hypothesis]`.
- Now: the place comes only from a pose with a valid position (at or after the recentre); a frame without one keeps
  the last offset; the eye pose sent to the headset follows the same place. The logs print the first pose's position
  and validity and, at the recentre, the place taken. 9 new checks in `mhead_test.c`, all pass; the old code fails 6.

## If RING works but the picture tears or flickers (plan, not built)
1. Read the diag first: `slow` above 0 means the headset let a slot go after 500 ms while its copy was still running,
   which CAN tear. Fix: never let go early; keep the slot claimed and skip that eye this frame.
2. `slow 0` and still torn: run `share=cpu` (cannot tear between devices). Clean on CPU means RING's cross-device
   timing is the fault: replace the event query with a shared `ID3D11Fence` (game context Signal after the copy,
   headset context Wait before reading), and Flush right after the copy. Log whether Metro's device has
   `ID3D11Device5` first.
3. Flicker that CPU shows too is not the handover: check the `present N: eye ..., dropped, empty` lines (pairing
   slips, BOTH-eye pictures), try `eye_source=1`, and switch off TAA (each eye's TAA history is the other eye's frame
   in alternate-frame stereo `[hypothesis]`; also the standing VR screen-effects rule).
