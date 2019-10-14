import CoolProp.CoolProp as CP
from RefCycle import refCycle
import numpy as np
import scipy.linalg as alg
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


ref = "R600a"
subcoolDegree = 2
suctionTemp = 32
condTemp = np.linspace(35,45,11)
evapTemp = np.linspace(-30,-20,11)
COP = np.zeros(11*11).reshape(11,11)
Wc = np.zeros(11*11).reshape(11,11)


fig = plt.figure(figsize=(11, 7), dpi=100)
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(condTemp, evapTemp)
for i in range(len(X)):
    for j in range(len(Y)):
        COP[i,j]=refCycle(ref,suctionTemp,Y[i,j],X[i,j],X[i,j]-subcoolDegree).cycleCOP()
        Wc[i,j]=refCycle(ref,suctionTemp,Y[i,j],X[i,j],X[i,j]-subcoolDegree).wc()

ax.plot_surface(X, Y, COP[:], cmap=cm.viridis, rstride=1, cstride=1)
#ax.plot_surface(X, Y, Wc[:], cmap=cm.viridis, rstride=1, cstride=1)
ax.set_xlabel('$Condensing Temperature$')
ax.set_ylabel('$Evaporating Temperature$')
plt.show()

qex =refCycle(ref,suctionTemp,evapTemp,40,40-subcoolDegree).cycleCOP()
print(qex)
plt.plot(evapTemp,qex)
plt.show()