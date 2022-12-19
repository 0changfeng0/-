import numpy as np
dx=-3

dxh=hex(dx)
dxh1=dx&0xFFFF
dxh2=hex(dxh1)
dxh3=dx&(2**16-1)
d=int(-1000.0)
dh=d>>8
dl=d
bytes=np.array
print(dx)
print(type(dx))
print(dxh)
print(type(dxh))
print(dxh1)
print(type(dxh1))
print(dxh2)
print(dxh3)
print(hex(dxh3))