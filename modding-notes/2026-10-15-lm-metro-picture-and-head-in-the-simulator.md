# 2026-10-15 (dev PC, `/lm`, unattended, one reader): Metro's own picture reaches the headset, and the head turns the view

Build `Headset output/v0.1.0-b005` (`metro_eye.dll` `b15ec24f31af`), OpenXR simulator (Quest 3 profile, 1280x1400 per
eye), DirectX 11. Two runs, the Moscow tunnel save. Evidence: `dev-archive/recon/2026-10-15-picture-and-head-in-the-simulator/`.

## 1. The picture handover: RING carries it

- LOCK failed exactly as the 2026-10-08 outcome table allowed: the game's device could not even OPEN a keyed-mutex
  texture made on the headset's device (`hr 0x80070057`, E_INVALIDARG), so the refusal is about keyed mutexes on
  that device at all, not only about creating them `[verified-live 2026-10-15, n=2 runs]`.
- The game's device is NOT DX11-on-12: `ID3D11On12Device no (hr 0x80004002)`, `ID3D11Device1 yes`, feature level
  11_1 (`0xb100`), creation flags 0 `[verified-live 2026-10-15, n=2]`. So `/gr`'s 11on12 explanation of the keyed
  mutex refusal is ruled out.
- RING took over at once and worked: `mxr ring: WORKS on the headset side - opened 6 eye textures`, game copies and
  headset pulls climbing together, `slow 0`, `headset busy 0`, `open fails 0`, `game busy` small (36-42 over ten
  minutes). The left and right serials stay one apart at most `[verified-live 2026-10-15, n=2 runs]`.
- **Metro's own picture shows in both eyes of the simulator** (loading screen, menu, gameplay); near things (the gun)
  sit differently in each eye. Turning the mouse, three captures in a row changed smoothly with no torn frame
  `[verified-live 2026-10-15, n=3 captures]` (three JPEGs is weak evidence for tearing; a headset look decides).
- The picture fills each eye stretched: the game's 16:9 picture is put into a 1280x1400 eye. Known; the lens match
  is a later job.
- Ring textures are sized from the back buffer at the first frame (1920x1061 in run 2) and kept after the window was
  resized to 1280x720; pictures kept flowing. Whether a resize leaves part of the eye picture stale is not checked
  `[hypothesis]`.

## 2. Head tracking (`head_tracking=1`, run 2)

- Runs: `mxr head: first head pose published`, `head: RECENTRED`, head poses and `eye views with the drawn pose`
  climbing (47,292 by the end), **no `NOTE: the game changed the view matrix` line**, so Metro does not rebuild its
  view during the scene render `[verified-live 2026-10-15, n=1 run]`.
- **Turning is the right way round:** simulator head yaw 30 deg left, the tunnel opening that was ahead slid to the
  right of both eyes; back to 0, the view returned to the same picture and stayed `[verified-live 2026-10-15, n=1]`.
  No spin, no drift seen over about a minute.
- **BUG: the head's height lifts the camera.** The recentre takes only the heading, not the position, so the
  simulator's standing head (y = 1.70 m) lifted Metro's camera 1.7 units, into the tunnel ceiling: a washed-out wrong
  view in the game window and the simulator. With the head at y = 0 the view is normal `[verified-live 2026-10-15,
  n=1]`. Fix: the recentre also stores the head position and only the movement from it is applied. Sent to the
  reader to build; see the board.
- Open: with head tracking on, the gun was not in its usual place in the game window (head at y = 0, yaw 0)
  `[verified-live 2026-10-15, n=1, unexplained]`. Look again after the height fix.
- The main menu is a 3D scene, so head tracking moves its camera too.

## 3. Window and focus

- This time `r_fullscreen on` was back in `user.cfg` (cause unknown; backed up, set off again). Run 1 then still came
  up borderless at full screen size; run 2 came up as a real captioned window `[verified-live 2026-10-15, n=1 each]`.
- **Metro minimises itself the moment it loses focus, and pauses** (pause menu), even resized to a 1280x720 window
  `[verified-live 2026-10-15, n=2]`. While minimised it stops presenting, so the headset gets no new pictures. Keep
  the game in front during headset tests.
- At 15:55:15 OBS crashed (Source Record add-on starting the second recording, inside NVENC setup), the same second
  the game minimised; the crash most likely took focus `[hypothesis]`. The second recording never saved, and OBS
  would not restart cleanly (a "crash detected" box held it). Run 1's game-window video is saved (10.4 min).

## 4. Driving

- Main menu: E = CONTINUE; Escape = QUIT GAME dialog, Enter = OK. Pause: Escape (the first Escape after the chapter
  starts sometimes does not register; look, press again), wait 2 s, Down x7 (extended arrow keys), Enter, Enter.
- HOLD E after a chapter loads: 3 s worked in run 1; in run 2 it needed a second, longer hold (4.5 s).
- The simulator's preview window can start squashed (584x21): resize it, or its screenshots are useless.

## Not established

- Whether the picture tears in a real headset; latency; the gun with head tracking; head position with the fix.
