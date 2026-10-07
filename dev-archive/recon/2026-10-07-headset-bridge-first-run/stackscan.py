"""stackscan.py <pid> <tid> [bytes] - list stack values that point into loaded modules (rough call stack)."""
import ctypes, ctypes.wintypes as W, sys, struct

k = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
pid, tid = int(sys.argv[1]), int(sys.argv[2])
size = int(sys.argv[3]) if len(sys.argv) > 3 else 0x3000
hp = k.OpenProcess(0x0410 | 0x0008, False, pid)

mods = (ctypes.c_void_p * 1024)(); need = W.DWORD()
psapi.GetModuleInformation.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_void_p, W.DWORD]
psapi.GetModuleBaseNameW.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_wchar_p, W.DWORD]
k.ReadProcessMemory.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]
psapi.EnumProcessModulesEx(hp, mods, ctypes.sizeof(mods), ctypes.byref(need), 3)
class MI(ctypes.Structure):
    _fields_ = [("base", ctypes.c_void_p), ("size", W.DWORD), ("entry", ctypes.c_void_p)]
ranges = []
for i in range(need.value // 8):
    mi = MI(); psapi.GetModuleInformation(hp, ctypes.c_void_p(mods[i]), ctypes.byref(mi), ctypes.sizeof(mi))
    nm = ctypes.create_unicode_buffer(260); psapi.GetModuleBaseNameW(hp, ctypes.c_void_p(mods[i]), nm, 260)
    ranges.append((mi.base, mi.base + mi.size, nm.value))

class CTX(ctypes.Structure):
    _fields_ = [("pad", ctypes.c_byte * 0x30), ("flags", W.DWORD), ("rest", ctypes.c_byte * (1232 - 0x34))]
ctx_buf = ctypes.create_string_buffer(1232 + 16)
addr = (ctypes.addressof(ctx_buf) + 15) & ~15
ctypes.memmove(addr + 0x30, struct.pack("<I", 0x100003), 4)   # CONTEXT_CONTROL
ht = k.OpenThread(0x0008 | 0x0040, False, tid)
k.SuspendThread(ht)
k.GetThreadContext(ht, ctypes.c_void_p(addr))
rip = struct.unpack_from("<Q", ctypes.string_at(addr, 1232), 0xF8)[0]
rsp = struct.unpack_from("<Q", ctypes.string_at(addr, 1232), 0x98)[0]
buf = ctypes.create_string_buffer(size); got = ctypes.c_size_t()
k.ReadProcessMemory(hp, ctypes.c_void_p(rsp), buf, size, ctypes.byref(got))
k.ResumeThread(ht)

def where(v):
    for a, b, n in ranges:
        if a <= v < b: return f"{n}+{v - a:#x}"
    return None
print("rip", where(rip) or hex(rip))
for off in range(0, got.value - 7, 8):
    v = struct.unpack_from("<Q", buf.raw, off)[0]
    w = where(v)
    if w: print(f"  sp+{off:#06x}  {w}")
