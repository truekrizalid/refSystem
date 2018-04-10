from CoolProp.CoolProp import PropsSI
class compressor(object):
    def __init__(self,compModel):
        self.model = compModel
        if self.model == "VTX1111YA":
            self.pistVol = 7.3*10**(-6) # 压缩机扫气容积 单位 m^3
            self.refType = "R600a"
        elif self.model == "VTH1113YA":
            self.pistVol = 8.9*10**(-6)
            self.refType = "R600a"
        elif self.model =="VNX1116Y":
            self.pistVol = 11.3*10**(-6)
            self.refType = "R600a"
        else:
            raise ValueError
#计算容积效率            
    def volEff(self,Te,Tk,N) :
        pk = PropsSI("P","T",Tk+273.15,"Q",1,self.refType)
        pe = PropsSI("P","T",Te+273.15,"Q",1,self.refType)
        Pr = pk/pe
        if self.model == "VTX1111YA":
            volEfficiency =0.93751 + 0.02681 * (N / 4500.0) - 0.02108 * Pr **(1.0/ 1.091)
        elif self.model == "VTH1113YA":
            volEfficiency = 0.93942 - 0.00319 * (N / 4500.0) - 0.02119* Pr **(1.0/ 1.091)
        elif self.model == "VNX1116Y":
            volEfficiency = 0.92022 - 0.06544 * (N / 4500.0) - 0.01814 * Pr **(1.0/ 1.091)
        else:
            raise ValueError
        return volEfficiency
        
    def isoEff(self,Te,Tk,N):
        fr = N/4500.0
        if self.model == "VTX1111YA":
            p1 = 0.6714
            p2 = 0.00109
            p3 = 0.00063
            p4 = -0.4191
            p5 = 0.00003
            p6 = -0.00005
            p7 = -0.0121
            p8 = 0.00003
            p9 = -0.01503
            p10 = 0.01628
            p11 = -0.00025
            p12 = 0.0003
            p13 = -0.00001
            p14 = -0.00818
            p15 = 0.00008
        elif self.model == "VTH1113YA":
            p1 = 0.90796
            p2 = 0.01042
            p3 = -0.0092
            p4 = -0.83759
            p5 = 0.00015
            p6 = 0.00002
            p7 = -0.1245
            p8 = -0.00013
            p9 = -0.03298
            p10 = 0.03258
            p11 = -0.00051
            p12 = -0.00464
            p13 = -0.00011
            p14 = -0.00954
            p15 = 0.0004
        elif self.model == "VNX1116Y":
            p1 = 0.64663
            p2 = -0.00276
            p3 = 0.00034
            p4 = -0.36695
            p5 = -0.00001
            p6 = -0.00002
            p7 = -0.06473
            p8 = 0.00007
            p9 = -0.00479
            p10 = 0.01318
            p11 = -0.00013
            p12 = -0.00313
            p13 = -0.00003
            p14 = -0.00485
            p15 = 0.00002
        else :
            raise ValueError
        #15系数模型拟合压缩机等熵压缩效率，3000rpm以下数据拟合结果较好，3000rpm以上拟合结果偏低，导致计算出来的压缩机输入功率
        #比实测功率高10%以上    
        compEfficiency = p1 + p2 * Te + p3 * Tk + p4 * fr + p5 * Te**2 + p6 * Tk**2 + p7 * fr **2 + p8 * Te * Tk \
            + p9 * Te * fr + p10 * Tk * fr + p11 * Te **2 * fr + p12 * Te * fr **2 + p13 * Tk **2 * fr + p14 * Tk * fr **2 \
            + p15 * Te * Tk * fr
        return compEfficiency

    
 # test code here   
cmp1 = compressor("VTX1111YA")
print cmp1.pistVol
print cmp1.volEff(-23.3,54.4,1500)
print cmp1.isoEff(-23.3,54.4,1500)       
#test code end
            
