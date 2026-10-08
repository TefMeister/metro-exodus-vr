# The picture handover, rebuilt without the game's keyed mutex

`/pd`, dev PC, 2026-10-08. **The game was not launched, and nothing here has been run.**

## Why

On 2026-10-07 the headset bridge showed its red/blue test picture in the OpenXR simulator, but Metro's own picture
could not follow: its DX11 device refuses every texture with `MISC_SHARED_KEYEDMUTEX` (`E_INVALIDARG`), and the
keyed mutex was the only way The Evil Within's bridge passed pictures between the game's device and the headset's.

## What was built

`staging/metro-exodus-vr/headset-bridge-2026-10-07` (`2837913`), `metro_eye.dll` `12adf66a6074`, installed as
builds `Headset output/v0.1.0-b004`. `metro_eye.ini` now has `test_pattern=0` (Metro's own picture) and
`share=auto`. The handover was split into three files: `mxr_eyes.c` (shared state, which way is in use, stats),
`mxr_eyes_lock.c` (LOCK) and `mxr_eyes_ring.c` (RING), with the pure turn-taking rules in `mxr_ring.c`.

1. **LOCK** - the same keyed-mutex textures, but made on the headset thread's own device and only opened on the
   game's. If the refusal is about *creating* them, this works and is the simplest. Any failure on either side
   switches to RING for the rest of the run, with one log line naming the step.
2. **RING** - no lock. Three plain shared textures per eye on the game's device. At each Present the game publishes
   any copy whose GPU event query has finished, picks a picture that is neither the newest published one nor the one
   the headset is reading, copies the back buffer in and ends that picture's query. The headset claims the newest
   published picture, copies it into its own texture, waits for its own copy to finish (that thread may wait), then
   lets it go. The game thread never waits.
3. On the first frame the log says whether the game's device is DX11 running on top of DX12 (`/gr`'s question).

`tests/ring_test.c` runs the turn-taking rules on two real threads with pictures written word by word: about 90,000
reads, none torn, none out of order; a writer that ignores the "being read" flag tears about 73,000 of 98,000, so
the test can fail `[verified-numerically 2026-10-08, n=2 runs]`.

## What is NOT established

- Whether LOCK's open succeeds on Metro's device: unknown until a run.
- Whether RING's pictures arrive whole on the headset device. D3D11 promises nothing between two devices without a
  keyed mutex; a finished event query on the writer is the usual stand-in `[hypothesis]`. **A diagnostic that would
  show the design is wrong, not a setting:** a picture in the simulator that is torn (top and bottom from different
  frames) or flickers between old and new while the mouse turns.
- Latency: RING publishes a picture one Present after it was copied. With alternating eyes that is one frame per eye.

## The next run (FLAT, simulator, no headset)

Launch as on 2026-10-07 with the simulator. Read `metro_eye_log.txt`:

| log says | means |
| --- | --- |
| `mxr lock: WORKS` and diag `share LOCK`, headset pulls climbing | LOCK carries the picture |
| `LOCK failed at ...` then `mxr ring: WORKS on the headset side`, diag `share RING`, pulls climbing | RING carries it |
| `game busy` climbing fast in RING | copies are overwritten before finishing; harmless unless pulls stall |
| `slow` climbing | the headset's own copy took over 500 ms; something is wrong with the headset device |
| both fail | try option (d) (dossier, 2026-10-08) |

Then look at the simulator window: Metro's picture in each eye, near objects shifted between them.
