# -*- coding: UTF-8 -*-
import CoolProp.CoolProp as CP

class refCycle(object):
    def __init__(self,refrigerantName, suctionTemp,evaTemp,condTemp,subcoolTemp):
        self.refType = refrigerantName
        self.Tsuct = suctionTemp +273.15   #由摄氏温度转换为绝对温度
        self.Te = evaTemp + 273.15
        self.Tk = condTemp +273.15
        self.Tsub = subcoolTemp + 273.15
    def Pk(self):
        #evaP = CP.PropsSI('P','T',evapTemp,'Q',1,ref)
        return CP.PropsSI("P",'T',self.Tk,'Q',1,self.refType)
    def Pe(self):
        return CP.PropsSI("P",'T',self.Te,'Q',1,self.refType)
    def Pratio(self):
        p1 = CP.PropsSI("P",'T',self.Tk,'Q',1,self.refType)
        p2 = CP.PropsSI("P",'T',self.Te,'Q',1,self.refType)
        return p1/p2
    def qe(self):
        h1 = CP.PropsSI("H","T",self.Tsuct,"P",self.Pe(),self.refType)
        h3 = CP.PropsSI("H","T",self.Tsub,"P",self.Pk(),self.refType)
        return h1-h3
    def wc(self):
        s1 = CP.PropsSI("S","T",self.Tsuct,"P",self.Pe(),self.refType)
        h2s =CP.PropsSI("H","S",s1,"P",self.Pk(),self.refType)
        hsuc = CP.PropsSI("H","T",self.Tsuct,"P",self.Pe(),self.refType) #等效h1 ，使用不同的变量名
        return h2s-hsuc
    def cycleCOP(self):
        return self.qe()/self.wc()
    
