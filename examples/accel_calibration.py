from FileManager import FileManager
from numpy import mean, append
from Quaternion import Quaternion
from Euler import Euler
from MathLib import toVector
from Settings import g, G
from math import pi

filePath = "data\\arduino10DOF\gyro_calibration_long.csv"
col_gyro = range(1,4)
col_accel = range(4,7)
col_mag = range(7,10)
col_acc_mag = range(4,10)
d = FileManager(filePath, columns=col_acc_mag, skip_header = 7)
v_acc = d.values[:,0:3]*-g
v_mag = d.values[:,3:6]
a_mean = mean(v_acc, axis = 0)
m_mean = mean(v_mag, axis = 0)
print(a_mean)
print(m_mean)

q = Quaternion(Euler(toVector(a_mean[0],a_mean[1],a_mean[2]), toVector(m_mean[0],m_mean[1],m_mean[2])).values)
print("q0 = %f, q1 = %f, q2 = %f, q3 = %f" % (q.q0, q.q1, q.q2, q.q3))
print(q.getEulerAngles()*180/pi)

x_arr = toVector(0.,0.,0.)

for i in range(0,d.length):
    a = toVector(v_acc[i,0],v_acc[i,1],v_acc[i,2])
    a_n = q.vecTransformation(a)+G
#     x,y,z = toValue(a_n)
    x_arr = append(x_arr, a_n, axis = 1)
#     append(y_arr, [y])
#     append(z_arr, [z])
b = mean(x_arr[:,1:-1], axis = 1 )
print("bx = %f, by = %f, bz = %f" % (b[0], b[1], b[2]))
