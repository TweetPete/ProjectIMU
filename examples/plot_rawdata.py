import matplotlib.pyplot as plt
from FileManager import CSVImporter
from math import pi

filePath = "data\\adafruit10DOF\\sample_imu_beuth_0801.csv"
col_gyro = range(0,4) #rad/s
col_accel = range(3,7) #-g
col_mag = range(6,10) #muT
col_eul = range(9,13)
d = CSVImporter(filePath, columns=col_gyro, skip_header = 8, hasTime=True)
v = d.values*180/pi#*-9.80665
print(d.length)
print(d.getSampleRate())
start = 0
l = d.length
x = v[start:l,1]
y = v[start:l,2]
z = v[start:l,3]
i = range(start,l)

red_dot, = plt.plot(x, "r-")
blue_dot, = plt.plot(y, "b-")
green_dot, = plt.plot(z, "g-")
    
plt.show()
