from FileManager import CSVImporter
from numpy import mean, append, std
from Quaternion import Quaternion
from Euler import Euler
from MathLib import toVector, toValue, runningAverage
from Settings import g, G
from math import pi

filePath = "data\\arduino10DOF\\1hr_Bias_stability_fast.csv"
col_gyro = range(1,4)
col_accel = range(4,7)
col_mag = range(7,10)
col_acc_mag = range(4,10)
d = CSVImporter(filePath, columns=col_acc_mag, skip_header = 7)
v_acc = d.values[:,0:3]#*-9.80665
v_mag = d.values[:,3:6]
a_mean = mean(v_acc, axis = 0)
m_mean = mean(v_mag, axis = 0)
print(a_mean)
print(m_mean)

q = Quaternion(Euler(toVector(a_mean[0],a_mean[1],a_mean[2]), toVector(m_mean[0],m_mean[1],m_mean[2])).values)
print(q)
#print(q.getEulerAngles()*180/pi)

# x_arr = toVector(0.,0.,0.)
x_mean = 0
y_mean = 0
z_mean = 0
for i in range(1,d.length):
    a = toVector(v_acc[i,0],v_acc[i,1],v_acc[i,2])
    a_n = q.vecTransformation(a)+toVector(0.,0.,1.)#G
    x,y,z = toValue(a_n)
#     x_arr = append(x_arr, a_n, axis = 1)
    x_mean = runningAverage(x_mean, x, 1/i)
    y_mean = runningAverage(y_mean, y, 1/i)
    z_mean = runningAverage(z_mean, z, 1/i)
    
print(x_mean, y_mean, z_mean)
# b = mean(x_arr[:,1:-1], axis = 1 )
# print("bx = %f, by = %f, bz = %f" % (mean(x_arr[0,1:-1]), mean(x_arr[1,1:-1]), mean(x_arr[2,1:-1])))
