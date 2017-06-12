import matplotlib.pyplot as plt
from FileManager import FileManager
from MathLib import toVector
from math import pi

filePath = "data\\arduino10DOF\\Tilt180_w100Hz.csv"
col_gyro = (0,1,2,3,4) #rad/s
col_accel = range(4,7) #-g
col_mag = range(7,10) #muT
d = FileManager(filePath, columns=col_gyro, skip_header = 7, hasTime=False)
v = d.values*-9.80665#*180/pi
print(d.length)
print(d.getSampleRate())
start = 0
l = d.length
x = v[start:l,1]
y = v[start:l,2]
z = v[start:l,3]
i = range(start,l)

red_dot, = plt.plot(x, "ro")
blue_dot, = plt.plot(y, "bo")
green_dot, = plt.plot(z, "go")
    
plt.show()
