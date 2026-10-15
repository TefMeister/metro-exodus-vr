"""List windows whose title contains 'OpenXR' and optionally resize the first: simwin.py [w h x y]"""
import ctypes, sys
from ctypes import wintypes
u32 = ctypes.windll.user32
found = []
def cb(h, _):
    n = u32.GetWindowTextLengthW(h)
    b = ctypes.create_unicode_buffer(n + 1)
    u32.GetWindowTextW(h, b, n + 1)
    if "OpenXR" in b.value:
        r = wintypes.RECT(); u32.GetWindowRect(h, ctypes.byref(r))
        c = wintypes.RECT(); u32.GetClientRect(h, ctypes.byref(c))
        found.append(h)
        print(hex(h), repr(b.value), "visible", u32.IsWindowVisible(h), "rect", r.left, r.top, r.right, r.bottom, "client", c.right, c.bottom)
    return True
u32.EnumWindows(ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(cb), 0)
if len(sys.argv) > 4 and found:
    w, h, x, y = map(int, sys.argv[1:5])
    # SWP_NOZORDER | SWP_NOACTIVATE | SWP_ASYNCWINDOWPOS (never block on the game's thread)
    print("SetWindowPos", u32.SetWindowPos(found[0], 0, x, y, w, h, 0x0004 | 0x0010 | 0x4000))
