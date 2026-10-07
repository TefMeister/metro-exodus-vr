# 2026-10-07: Metro Exodus camera read live (original edition, DirectX 11)

`metro_cam.py` reads 16 floats at RVA 0x2111640 (view), 0x2111680 (projection), 0x21116c0 (view*projection) of the
running MetroExodus.exe with ReadProcessMemory (read-only).

Main menu (window 1920x1061 at the time):
  proj  2.3018 0 0 0 | 0 4.1653 0 0 | 0.0001 -0.0002 -0.0002 1 | 0 0 0.1 0     (sy/sx = 1.810 = 1920/1061)
Gameplay (prologue tunnel, 1280x720 window):
  before turn  view rows: -0.0015 0.0974 0.9952 0 | -0.0002 0.9952 -0.0974 0 | -1.0000 -0.0004 -0.0015 0 | -12.63 9.14 104.41 1
  after 10x30 px mouse right:
               view rows: -0.1412 0.0964 0.9853 0 | -0.0002 0.9952 -0.0974 0 | -0.9900 -0.0140 -0.1405 0 | -27.15 8.86 101.63 1
  proj  0.9571 0 0 0 | 0 1.7321 0 0 | (jitter) 1 | 0 0 0.1001 0

Reading: row-vector convention (translation in row 3); the 3x3 is orthonormal; column 2 is the forward axis and it
turned ~8 degrees with the mouse. Projection: sy = 1.7321 = 1/tan(30 deg) -> 60 degree vertical field of view;
sx = sy * 720/1280; clip w = view z; clip z = 0.1 (near plane) -> reversed-Z, infinite far; row 2 carries the TAA
jitter, which changes every frame.
