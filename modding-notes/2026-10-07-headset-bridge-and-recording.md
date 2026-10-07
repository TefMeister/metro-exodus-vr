# 2026-10-07 — first recordings, and the headset bridge's first live runs

Dev PC, `/lm`, unattended (Tefa at work, with two notes from afar).

## Recording

- OBS now records each flat-screen run, the game window only. The first run (menu → save → look around → walk)
  came out at 1280x720, 60 fps, 7944 of 7960 frames written `[verified-live 2026-10-07, n=1]`.
- OBS can also record the game and the OpenXR simulator into two separate files at once (the Source Record add-on;
  the second file starts about half a second later). Both test-pattern videos are in the MEGA transfer folder.

## The headset bridge

The reader ported The Evil Within's OpenXR bridge into `metro_eye.dll`. Live, three things turned up:

1. It froze the game on the first frame (it asked for the window title the wrong way). Fixed.
2. The simulator only shows full-view (projection) layers. With that setting, Metro sends it the red/blue test
   picture at a steady 60 fps.
3. **Metro's graphics device will not make the locked shared pictures the bridge hands over.** Plain shared pictures
   are fine. So the game's own picture does not reach the headset yet; the handover has to be rebuilt without the
   lock (three ways listed in the dossier).

## Not established

- Whether the eye pairing (scene render ↔ Present) holds: no game picture has flowed yet.
- Why the device refuses the lock.

## Two notes from Tefa

- Toxic-air zones run the filter out; idling in one killed the player (the start of the current save is one).
- Holding E also skips the loading-story screen.
