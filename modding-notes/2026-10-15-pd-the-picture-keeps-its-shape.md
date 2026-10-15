# 2026-10-15 (`/pd`, dev PC, no launch): the picture keeps its shape in each eye

The game was not launched, and nothing here has been run in the game.

## The question

In the OpenXR simulator, Metro's 16:9 picture fills each 1280x1400 eye, stretched tall. The board row asked for each
projection layer to carry the field of view the game actually drew with.

## What was already true

- With `head_tracking=1`, b005/b006 already put the game's own lens on every projection view: `mh_fov_from_proj` turns
  Metro's projection matrix (row-vector, w = view z) into the four edge tangents, and `drawn_view` used them as the
  layer's `fov`. Run 3 on 2026-10-15 logged 18,905 eye views sent that way `[verified-live 2026-10-15, n=1 run]`.
- **The simulator still showed the picture stretched, identically framed to run 1 (head tracking off).** Its README
  says its preview "blits stereo views to a desktop window": it copies each eye image into its half of the window and
  ignores the layer's `fov` `[inferred-static 2026-10-15]` (from its documentation, not its source). So the
  simulator's preview cannot show whether the shape is right. Its `get_projection_log` tool reports the `fov` each
  layer was submitted with, and that can.
- **The gap:** with head tracking OFF, the layer took the headset's own lens, so a real headset would stretch the
  picture to the eye's shape.

## The live projection, checked against the numbers read on 2026-10-07

Gameplay (`dev-archive/recon/2026-10-07-camera-read-live`): `P[0] 0.9571`, `P[5] 1.7321`, jitter in `P[8]`, `P[9]`.
That is 30 deg up and down and 46.25 deg left and right. **1.7321 / 0.9571 = 1.810 = 1920/1061, not 1280/720**: the
window had been resized from outside, the back buffer stayed 1920x1061, and the lens kept the back buffer's shape
`[verified-numerically 2026-10-15]`. The recon README's line "sx = sy * 720/1280" does not match its own numbers. The
picture the headset receives is the back buffer, so lens and picture agree.

## What was built `[compile-verified 2026-10-15]`, `[verified-numerically 2026-10-15]`

- `MhUsed` gains `lens` (the tangents are known) apart from `valid` (the pose is known). `metro_eye.c` records the lens
  for every scene render, including frames with neither the eye shift nor head tracking.
- `mxr.c`: `drawn_view` split into `drawn_lens` (always, when known) and `drawn_pose` (head tracking only). The first
  time, the log names both lenses: `mxr: eye views carry the game's own lens: L R D U deg; the headset's is ...`. The
  diag line gains `with the game's lens N`.
- New pure helper `mh_layer_angles`. 10 new checks in `tests/mhead_test.c` (20,033 pass), expectations computed in
  double from the live matrix entries; a planted "lens only with a pose" plus a 10 % wrong right edge fail 5 of them.
- The unchanged source still rebuilds byte-for-byte to the installed b006 `2e8cf7e10db7` before the change.
- Same change in the reader's `share-cpu-2026-10-15` copy (its `metro_eye.c` and `mhead.*` were identical), which
  builds and passes its own tests (`8c4e3b0ea0b9`, not installed).
- Installed `metro_eye.dll` `ced3151c7670` (b006 kept as `metro_eye.dll.bak-2026-10-15-pd-pre-lens`), ini unchanged;
  stamped; build `Headset output/v0.1.0-b007`.

## What it means in a headset `[hypothesis]`

A compositor that honours the layer `fov` (every real runtime) shows the picture at the angles the game drew it with:
the right shape, 92.5 x 60 deg at the gameplay setting, and dark above and below it, because the headset eye is about
96 deg tall. Nothing is stretched, but the picture does not fill the eye.

## What is NOT established

- That the simulator really ignores the layer `fov` (documentation only). `get_projection_log` during the next run
  answers it, and shows the submitted angles.
- How the dark bands look and feel in a real headset.

## Next

1. **[FLAT] (free, any launch)**: read `mxr: eye views carry the game's own lens` in `metro_eye_log.txt` (expect about
   -46 46 -30 30 in gameplay) and call the simulator's `get_projection_log`; its submitted fov should match.
2. **To fill the eye** (later, a design step): draw the game with the headset's own lens, by writing the headset's
   tangents into Metro's projection (RVA 0x2111680) in the scene-render hook, the way the view is already changed and
   put back. TAA jitter, culling and the gun's own projection have to be checked first.
