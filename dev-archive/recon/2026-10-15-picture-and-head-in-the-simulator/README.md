# 2026-10-15: Metro's picture and head tracking in the OpenXR simulator

Dev PC, `/lm`, build `Headset output/v0.1.0-b005` (`metro_eye.dll` `b15ec24f31af`). Write-up:
`modding-notes/2026-10-15-lm-metro-picture-and-head-in-the-simulator.md`.

| file | what |
| --- | --- |
| `run1_metro_eye_log.txt` | run 1: LOCK fails at the open, RING carries the picture; head tracking off |
| `run2_metro_eye_log.txt` | run 2: the same, head tracking on |
| `sim-run1-game-picture-both-eyes.jpg` | the simulator showing Metro's own picture, both eyes |
| `sim-run1-while-turning.jpg` | one of three captures while the mouse turned |
| `sim-run2-head-at-1.7m-camera-in-ceiling.jpg` | the height bug: the head at 1.70 m lifts the camera |
| `sim-run2-head-at-0m-yaw0.jpg`, `-yaw30-left.jpg`, `-back-to-yaw0.jpg` | the turn test |
| `drive.py`, `gamewin.py`, `simwin.py` | the small input and window helpers used |

The OBS crash report (15:55:15, `obs.dll!obs_encoder_video_tex_active` from `obs-nvenc` inside `source-record`) is
not kept here because it lists local paths.

Run 3 (build b006, `metro_eye.dll` `2e8cf7e10db7`):

| file | what |
| --- | --- |
| `run3_b006_metro_eye_log.txt` | the new `head place` lines |
| `sim-run3-head-raised-11m-by-holding-E.jpg` | the simulator head at 11.4 m after the HOLD E |
| `sim-run3-b006-standing-height-yaw0.jpg`, `-yaw30-left.jpg`, `-back-to-yaw0.jpg` | the turn test at standing height |
