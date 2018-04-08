from CoolProp.CoolProp import PropsSI


class compressor(object):
    def __init__(self,Model):
        self.model = Model
        self.pisVol = 8.9
        self.refType = "R600a"
    def volEff(self,te):
        if self.model == "VNX1113Y":
            return te/100.0  #python 对整型和浮点数区分比较严 100 整型 ，100.0 浮点数
        else:
            return 0.8+te/100
    def isoEff(self):
        return 0.6
