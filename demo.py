# -*- coding: UTF-8 -*-

from Compressor import compressor 
from RefCycle import refCycle
import CoolProp.CoolProp as CP
cmp1 =compressor("VNX1116Y")
print cmp1.pistVol
print cmp1.volEff(-23.3,54.4,1500)
print cmp1.isoEff(-23.3,54.4,1500) 

cy1 =refCycle("R600a",32.2, -23.3, 54.4, 32.2)
print cy1.cycleCOP()
