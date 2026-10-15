"""Tiny driver for Metro: hold a key (scancode) or move the mouse, game window foregrounded first.
usage: drive.py hold <scan_hex> <seconds> | drive.py mouse <dx> <dy> <count> [delay_s] | drive.py tap <scan_hex>
"""
import ctypes, sys, time
from ctypes import wintypes

u32 = ctypes.windll.user32
ULONG_PTR = ctypes.c_size_t

class KI(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]

class MI(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]

class U(ctypes.Union):
    _fields_ = [("ki", KI), ("mi", MI), ("pad", ctypes.c_byte * 32)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", U)]

def send(inp):
    u32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def key(scan, up=False):
    i = INPUT(type=1)
    ext = 0x0001 if scan in (0x48, 0x50, 0x4B, 0x4D) else 0  # arrows
    i.u.ki = KI(0, scan, 0x0008 | ext | (0x0002 if up else 0), 0, 0)
    send(i)

def mouse(dx, dy):
    i = INPUT(type=0)
    i.u.mi = MI(dx, dy, 0, 0x0001, 0, 0)
    send(i)

def front():
    h = u32.FindWindowW(None, "4A Engine")
    if not h:
        sys.exit("no game window")
    u32.ShowWindow(h, 9)
    u32.SetForegroundWindow(h)
    time.sleep(0.4)
    if u32.GetForegroundWindow() != h:
        sys.exit("could not foreground the game")

front()
cmd = sys.argv[1]
if cmd == "hold":
    s = int(sys.argv[2], 16)
    key(s); time.sleep(float(sys.argv[3])); key(s, True)
elif cmd == "tap":
    s = int(sys.argv[2], 16)
    key(s); time.sleep(0.08); key(s, True)
elif cmd == "mouse":
    dx, dy, n = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    d = float(sys.argv[5]) if len(sys.argv) > 5 else 0.03
    for _ in range(n):
        mouse(dx, dy); time.sleep(d)
print("ok")
