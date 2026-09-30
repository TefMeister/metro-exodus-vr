# First launch on the dev PC — 2026-09-30

Unattended `/lm` run, dev PC (GTX 1660 SUPER, 1920×1080), game as shipped (nothing of ours installed).

| Step | What happened |
| --- | --- |
| Launch through Steam | A Win32 box: "System specification requirements not met — Graphics device does not support DXR1.1 or above." Buttons: Open Link / Quit / Run Anyway. See `dxr11-warning-dialog.png`. |
| Run Anyway (BM_CLICK) | Window "4A Engine", fullscreen 1920×1080 at 0,0. `legal` and `intro` films play. |
| Space | The film ended and the title screen with a spinner appeared. |
| Title screen, ~6 min | About 6 CPU cores busy, working set rose to ~7 GB: the first-run shader build `[hypothesis]`. |
| Crash | BugTrap "FATAL: MetroExodus". Access violation reading address `0x18c` at `D3D12Core.dll+0x12accc` (from the crash dump's exception record). `HKCU\Software\4A-Games\Metro Exodus\BadQuit` set to 1; reset to 0 afterwards. |

Result: the Enhanced Edition does not reach the main menu on a card without DXR 1.1
`[verified-live 2026-09-30, n=1]`. The crash sits inside the Direct3D 12 runtime, which fits the game's
own warning, but the dump alone does not prove the ray-tracing call is the cause `[hypothesis]`.

The crash dump itself is not kept here (60 MB, and it holds game memory).
