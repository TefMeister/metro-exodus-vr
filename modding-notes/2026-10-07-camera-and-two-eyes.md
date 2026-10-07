# 2026-10-07 (dev PC, `/lm`, with Tefa playing to a save point): camera read live, two eyes alternate

- DirectX 11 on (Tefa added `-force_rapi 2` to the Steam launch options); window confirmed by Tefa.
- The camera's matrices were read from the running game; they follow the mouse exactly as a camera should.
- The reader built a small two-eye mod (`metro_eye.dll`): it moves the camera half an eye-width left or right on
  alternate frames. Live, the frames alternate cleanly and near things separate more than far ones.
- Driving notes: E skips films and picks the selected main-menu button; "HOLD E" continues after a chapter loads;
  the pause menu needs ~2 s before arrow keys register; changing graphics quality makes the window screen-sized again.

Not established: the eye distance in real units (assumed metres); whether temporal anti-aliasing mixes the eyes in
motion; headset output (the next build, as for The Evil Within).
