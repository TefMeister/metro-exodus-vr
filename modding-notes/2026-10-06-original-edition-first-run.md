# 2026-10-06 (dev PC, `/lm`, unattended): the original edition runs here

The Enhanced Edition cannot run on the dev PC's graphics card, so Tefa installed the original 2019 Metro Exodus.
This session did the first-run checklist on it.

- **Runs as shipped:** started through Steam, intro films skipped with Escape, main menu reached.
- **Runs with our file:** a small logging `dxgi.dll` loads and passes everything through.
- **Windowed:** turning fullscreen off in the settings file gives a window the size of the screen; resizing it from
  outside to 1280x720 works, and the picture fills it. Tefa still has to confirm it looks right.
- **Music muted** in the settings file, and the game keeps it.
- **Renderer:** the game runs DirectX 12 by default. The settings file cannot switch it, because the renderer is
  created before the file is applied. The command-line switch `-force_rapi 2` should give DirectX 11, but it has to
  go through Steam, which asks a person to confirm once.
- **The reader** (static, no game): found the camera's view and projection matrices in memory and the function
  that builds them each frame, which is the place to make two eyes. The leftover VR switches never draw two eyes:
  `-build_key oculus` mostly moves the window to a second monitor (the old Oculus "extended mode").

Not established: whether `-force_rapi 2` really gives DirectX 11; whether the camera addresses are right (static
only); whether the window size holds over a whole session. Details: dossier "2026-10-06 ... first live session" and
`dev-archive/recon/2026-10-06-original-edition-static/`.
