"""Read Metro Exodus's camera matrices (view, projection, view*projection) from the running game, read-only.
Usage: python metro_cam.py [count] [interval_s]"""
import ctypes, ctypes.wintypes as W, struct, sys, time

k = ctypes.windll.kernel32
PROCESS_VM_READ, PROCESS_QUERY_INFORMATION = 0x0010, 0x0400
RVAS = {'view': 0x2111640, 'proj': 0x2111680, 'viewproj': 0x21116c0}

def pid_of(name):
    import subprocess
    out = subprocess.run(['tasklist', '/fi', f'imagename eq {name}', '/fo', 'csv', '/nh'], capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = line.strip('"').split('","')
        if parts and parts[0].lower() == name.lower():
            return int(parts[1])
    return None

class ME(ctypes.Structure):
    _fields_ = [('dwSize', W.DWORD), ('th32ModuleID', W.DWORD), ('th32ProcessID', W.DWORD), ('GlblcntUsage', W.DWORD),
                ('ProccntUsage', W.DWORD), ('modBaseAddr', ctypes.c_void_p), ('modBaseSize', W.DWORD), ('hModule', W.HMODULE),
                ('szModule', ctypes.c_char * 256), ('szExePath', ctypes.c_char * 260)]

def module_base(pid, name):
    snap = k.CreateToolhelp32Snapshot(0x8 | 0x10, pid)
    me = ME(); me.dwSize = ctypes.sizeof(ME)
    ok = k.Module32First(snap, ctypes.byref(me))
    while ok:
        if me.szModule.decode().lower() == name.lower():
            k.CloseHandle(snap); return me.modBaseAddr
        ok = k.Module32Next(snap, ctypes.byref(me))
    k.CloseHandle(snap)

def read(h, addr, n):
    buf = ctypes.create_string_buffer(n); got = ctypes.c_size_t()
    if not k.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, n, ctypes.byref(got)): return None
    return buf.raw

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    gap = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    pid = pid_of('MetroExodus.exe'); base = module_base(pid, 'MetroExodus.exe')
    h = k.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    print('pid', pid, 'base %x' % base)
    for i in range(count):
        for name, rva in RVAS.items():
            raw = read(h, base + rva, 64)
            m = struct.unpack('16f', raw)
            print('%-8s' % name, ' | '.join(' '.join('%9.4f' % v for v in m[r*4:r*4+4]) for r in range(4)))
        if i + 1 < count: time.sleep(gap); print('--')
    k.CloseHandle(h)

main()
