# 2026-10-12 (dev PC, `/pd`, no game launch): head tracking built into `metro_eye.dll`

**The game was not launched, and nothing here has been run in it.**

## What it does

`metro_eye.ini [xr] head_tracking=1` (needs `layers=projection`; default 0, so the installed game behaves as before):

1. The headset thread locates the head (VIEW in LOCAL) every headset frame and publishes it (`mhead.c`, a
   sequence-numbered slot; the game never waits).
2. At each scene render the camera hook turns Metro's own view matrix by the head: `V' = V * M`, then the eye shift
   along the head's right. Metro's view space is x right, y up, z forward (clip w = view z), OpenXR's is z back, so the
   head pose is mirrored through z on the way in. The first pose is the recentre (heading only; pitch and roll stay
   real); numpad 2 recentres. `head_position=1` (default) moves the camera with the head too, 1 m = 1 world unit
   `[hypothesis]`.
3. The double-precision view copy (RVA `0x2111700`, camera object +0x100) is turned the same way, as the eye shift
   already did to it.
4. After the render the game's view (float and double) is put back from saved copies, not undone by arithmetic, so
   nothing of ours can pile up from frame to frame (no spin). If the game itself changed the view during the render,
   a `NOTE:` line says so once and the diag line counts it: the old shift-undo assumed it never does.
5. Each picture carries the head pose and the game's own lens (from its projection, jitter included) through the eye
   queue and both handover ways (LOCK: inside the keyed mutex; RING: per slot), and its projection layer is
   submitted with exactly that pose and lens, so the compositor only corrects the latency.

## Verified

- `tests/mhead_test.c`: 20,014 checks `[verified-numerically 2026-10-12]`. Directions in plain terms (head turned left:
  a point 30 deg left comes to the centre; up; tilt; step right; step back; position off), recentre keeps pitch,
  20,000 random cameras/heads/points against an independent quaternion route (no matrices), the eye pose, the lens,
  the published pose. With the z mirror planted wrong, the turn-left, look-up and recentre checks fail (and all
  random cases) — tilt cannot tell, by nature.
- Builds; the eye-queue, format and ring tests still pass `[compile-verified 2026-10-12]`.
- Installed `metro_eye.dll` `b15ec24f31af`; ini unchanged (head tracking off). Build `Headset output/v0.1.0-b005`.

## Not established

- Whether the game rebuilds its view matrix inside the scene render (the `NOTE:` line will say).
- Units (1 m = 1 world unit), comfort, and how the first-person gun behaves when the head turns (it is drawn in the
  same space, so it should stay put in the world, not follow the head; a live look decides).
- Whether the picture handover itself works (`[FLAT]` row before this one).

## Next live test (can share the handover launch)

With the handover row's settings, add `head_tracking=1`. In the simulator turn the head 30 deg left
(`set_head_pose`, yaw 30):
- the game window's view turns left and **stays** (no drift); back to 0 returns it; the log shows
  `mxr head: first head pose published`, `head: RECENTRED`, and the diag line's `eye views with the drawn pose` climbing;
- the view turns the WRONG way: the z mirror is wrong for this game after all (the self-test says it is right for a
  z-forward view, so check the view's handedness);
- it keeps turning (spins): should be impossible with the saved-copy restore; capture the log;
- `NOTE: the game changed the view matrix`: the game touches the view mid-render; note how often.
