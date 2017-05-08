from FileManager import FileManager
from MathLib import toVector
import matplotlib.pyplot as plt 

filePath = "data\\arduino10DOF\gyro_calibration_long.csv"
d = FileManager(filePath, columns=range(1,4), skip_header = 7)
v = d.values

x = v[:,0]
y = v[:,1]
z = v[:,2]
i = range(0,d.length)

x0 = toVector(x[0], y[0], z[0])
#K = 0.1
plt.ion()
for i in range(1,d.length-1):
    meas = toVector(x[i], y[i], z[i])
    K = 1/i
    x0 += K*(meas - x0)
#     plt.plot(i,x0[0],'ro')
#     plt.show()
#     plt.pause(0.05)
print(x0)
