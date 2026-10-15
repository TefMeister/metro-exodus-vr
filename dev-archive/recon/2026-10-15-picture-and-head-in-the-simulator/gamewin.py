"""Game window state, optionally restore it: gamewin.py [restore | size W H]"""
import ctypes, sys, time
from ctypes import wintypes
u32 = ctypes.windll.user32
h = u32.FindWindowW(None, "4A Engine")
def show():
    r = wintypes.RECT(); u32.GetWindowRect(h, ctypes.byref(r))
    c = wintypes.RECT(); u32.GetClientRect(h, ctypes.byref(c))
    st = u32.GetWindowLongW(h, -16) & 0xFFFFFFFF
    print("iconic", u32.IsIconic(h), "zoomed", u32.IsZoomed(h), "rect", r.left, r.top, r.right, r.bottom,
          "client", c.right, c.bottom, "caption", bool(st & 0x00C00000 == 0x00C00000), "fg", u32.GetForegroundWindow() == h)
show()
if len(sys.argv) > 1 and sys.argv[1] == "restore":
    u32.ShowWindowAsync(h, 9)
    time.sleep(1.0)
    u32.SetForegroundWindow(h)
    time.sleep(1.0)
    show()
if len(sys.argv) > 3 and sys.argv[1] == "size":
    w, hh = int(sys.argv[2]), int(sys.argv[3])
    r = wintypes.RECT(0, 0, w, hh)
    u32.AdjustWindowRectEx(ctypes.byref(r), u32.GetWindowLongW(h, -16), False, u32.GetWindowLongW(h, -20))
    print("SetWindowPos", u32.SetWindowPos(h, 0, 20, 20, r.right - r.left, r.bottom - r.top, 0x0004 | 0x4000))
    time.sleep(1.0)
    show()
