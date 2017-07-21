import matplotlib.pyplot as plt
from FileManager import CSVImporter
from MathLib import toVector
from math import pi

filePath = "sample_10minY10min_BW3.csv"
col_gyro = (0,1,2,3,4) #rad/s
col_accel = range(3,7) #-g
col_mag = range(6,10) #muT
d = CSVImporter(filePath, columns=col_gyro, skip_header = 7, hasTime=False)
v = d.values#*-9.80665#*180/pi
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
