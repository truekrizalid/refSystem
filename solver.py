# -*- coding: UTF-8 -*-

from Compressor import compressor 
from RefCycle import refCycle
import CoolProp.CoolProp as CP
import numpy as np
#Input physical data:
cmpName =  "VTH1113YA" 
N = 1800                    #量纲一定要注意 r/min
UAcmp = 1.03                #压缩机壳体热导,单位：（W/k)
UAk = 18.0                  #冷凝器热导
UAe = 45.3                  #蒸发器热导
UAcab = 1.91                  #箱体热导，在迭代求冷凝蒸发温度时不参与计算
sigma = 0.89                #回气管的性能参数，根据此参数计算回气管温度
Tamb = 25                 #环境温度，单位：摄氏度
DTsub = 1                 #锁定过冷度，单位：（摄氏度 or K)
Tf = -18

#系统性能计算函数
def Tsuct(Te,Tk,subDT,slh):     #计算回气温度
    return slh*(Tk-subDT-Te)+Te   

def f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td):#注意函数定义时，变量排布顺序的一致性 f1：冷凝器负荷
    cmp1 = compressor(cmpName)
    Ts = Tsuct(Te,Tk,DTsub,sigma)
    cy = refCycle(cmp1.refType,Ts,Te,Tk,Tk-DTsub)
    Qk1 = UAk*(Tk-Tamb)
    Qk2 =cmp1.mf(N,Te,Tk,Ts)*cy.qk(Td)
    return Qk2 - Qk1

#print f1(cmpName,N,UAk,sigma,Tamb, -22.8,38.3,DTsub,63)
def f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td):  #压缩机壳体负荷
    cmp2 =compressor(cmpName)
    Ts = Tsuct(Te,Tk,DTsub,sigma)
    cy2 = refCycle(cmp2.refType,Ts,Te,Tk,Tk-DTsub)
    Qc1 = UAcmp*(Td -Tamb)
    Qc2 = cmp2.mf(N,Te,Tk,Ts)*(cy2.wc()/cmp2.isoEff(Te,Tk,N)-cy2.h2_1(Td))
    return Qc2-Qc1
#f2(cmpName,N,UAcmp,sigma,Tamb,-22.8,38.3,DTsub,63)
def f3(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf):  #蒸发器负荷
    cmp3 =compressor(cmpName)
    Ts =Tsuct(Te,Tk,DTsub,sigma)
    cy3 =refCycle(cmp3.refType,Ts,Te,Tk,Tk-DTsub)
    Qe1 = UAe*(Tf - Te)   
    Qe2 = cmp3.mf(N,Te,Tk,Ts)*cy3.qe()
    return Qe2 - Qe1
#print f3(cmpName,N,UAe,sigma,-23,40,DTsub,Tf)

# 计算雅可比矩阵
def f1dTK(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td):
    dtk = 0.001
    J11= 1.0/dtk*(f1(cmpName,N,UAk,sigma,Tamb,Te,Tk+dtk,DTsub,Td)-f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td))
    return J11
def f1dTd(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td):
    dtd = 0.001
    J12 = 1.0/dtd*(f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td+dtd)-f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td))
    return J12
def f1dTe(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td):
    dte = 0.001
    J13 = 1.0/dte*(f1(cmpName,N,UAk,sigma,Tamb,Te+dte,Tk,DTsub,Td)-f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td))
    return J13
def f2dTk(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td):
    dtk = 0.001
    J21 = 1.0/dtk*(f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk+dtk,DTsub,Td)-f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td))
    return J21
def f2dTd(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td):
    dtd = 0.001
    J22 = 1.0/dtd*(f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td+dtd)-f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td))
    return J22
def f2dTe(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td):
    dte = 0.001
    J23 = 1.0/dte*(f2(cmpName,N,UAcmp,sigma,Tamb,Te+dte,Tk,DTsub,Td)-f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td))
    return J23
def f3dTk(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf):
    dtk = 0.001
    J31 = 1.0/dtk*(f3(cmpName,N,UAe,sigma,Te,Tk+dtk,DTsub,Tf)-f3(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf))
    return J31
def f3dTd(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf):
    return 0  #f3与压缩机排气温度无关，求偏导恒为0
def f3dTe(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf):
    dte = 0.001
    J33 = 1.0/dte*(f3(cmpName,N,UAe,sigma,Te+dte,Tk,DTsub,Tf)-f3(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf))
    return J33
#计算函数定义结束

# main（）开始求解系统工况
ep = 0.1 #收敛阀值
U = np.matrix([[Tamb+5],[Tamb+15],[Tf-5]]) # initial value
Tk,Td,Te =U[0,0],U[1,0],U[2,0]
#print "initial value is",Tk,Td,Te

while (abs( f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td)) < ep and abs(f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td))<ep \
and abs(f3(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf))<ep )== False :
    y = np.matrix([[ f1(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td)],[f2(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td)],[f3(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf)]])
    Jac = np.matrix([[f1dTK(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td),f1dTd(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td),\
                    f1dTe(cmpName,N,UAk,sigma,Tamb,Te,Tk,DTsub,Td)],[f2dTk(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td),\
                   f2dTd(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td), f2dTe(cmpName,N,UAcmp,sigma,Tamb,Te,Tk,DTsub,Td)],\
                   [f3dTk(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf),f3dTd(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf),f3dTe(cmpName,N,UAe,sigma,Te,Tk,DTsub,Tf)]])
    U = U - Jac**(-1)*y
    Tk,Td,Te = U[0,0],U[1,0],U[2,0]
    
# main code end
# data analysis
Ts = Tsuct(Te,Tk,DTsub,sigma)
print "Tk=",Tk,"Td=",Td,"Te=",Te,"Ts=",Ts
comp = compressor(cmpName)
cyFinal=refCycle(comp.refType,Ts,Te,Tk,DTsub)
inputPower = comp.mf(N,Te,Tk,Ts)*cyFinal.wc()/comp.isoEff(Te,Tk,N)
print inputPower
Qe = UAe*(Tf-Te)
Qk = UAk*(Tk-Tamb)
Qcmp = UAcmp*(Td - Tamb)
print Qe,Qk,Qcmp

Qcab = UAcab*(Tamb-Tf)
print "Cabinet load is",Qcab,"W"
R = Qcab/Qe
print "compressor Running ratio is:",R
