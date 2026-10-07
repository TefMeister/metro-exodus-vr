import ctypes, ctypes.wintypes as W, time, sys
from PIL import Image
import numpy as np
u=ctypes.windll.user32; g=ctypes.windll.gdi32; u.SetProcessDPIAware()
h=u.FindWindowW(sys.argv[1],sys.argv[2]); u.SetForegroundWindow(h); time.sleep(0.3)
r=W.RECT(); u.GetClientRect(h,ctypes.byref(r)); p=W.POINT(0,0); u.ClientToScreen(h,ctypes.byref(p)); w,hh=r.right,r.bottom
class BIH(ctypes.Structure):
    _fields_=[("a",W.DWORD),("w",W.LONG),("h",W.LONG),("pl",W.WORD),("bc",W.WORD),("c",W.DWORD),("s",W.DWORD),("x",W.LONG),("y",W.LONG),("cu",W.DWORD),("ci",W.DWORD)]
sdc=u.GetDC(0); mdc=g.CreateCompatibleDC(sdc); bmp=g.CreateCompatibleBitmap(sdc,w,hh); g.SelectObject(mdc,bmp)
A=[]
for i in range(24):
    g.BitBlt(mdc,0,0,w,hh,sdc,p.x,p.y,0x00CC0020)
    bi=BIH(40,w,-hh,1,32,0,0,0,0,0,0); buf=ctypes.create_string_buffer(w*hh*4)
    g.GetDIBits(mdc,bmp,0,hh,buf,ctypes.byref(bi),0)
    A.append(np.asarray(Image.frombuffer("RGBA",(w,hh),buf,"raw","BGRA",0,1).convert("L"),float)); time.sleep(0.011)
def sh(a,b,y0,y1,x0,x1,R=40):
    best=(1e9,0)
    for d in range(-R,R+1):
        xa=slice(max(x0,x0-d),min(x1,x1-d)); xb=slice(xa.start+d,xa.stop+d)
        e=abs(a[y0:y1,xa]-b[y0:y1,xb]).mean()
        if e<best[0]: best=(e,d)
    return best[1]
print('far :',[sh(A[0],A[i],120,330,420,820) for i in range(1,24)])
print('gun :',[sh(A[0],A[i],400,600,640,900) for i in range(1,24)])
