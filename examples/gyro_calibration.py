from FileManager import CSVImporter
from numpy import polyfit, std
from math import pi

filePath = "data\\adafruit10DOF\\sample_Hubarm.csv"
# filePath = "test_sampleRate.csv"
col_gyro = range(0,4) #rad/s
col_accel = range(3,7) #-g
col_mag = range(6,10) #muT
d = CSVImporter(filePath, columns=col_gyro, skip_header = 8, hasTime=True)
v = d.values*180/pi#*-9.80665#

start = 0
l = 45779
x = v[start:l,1]
y = v[start:l,2]
z = v[start:l,3]
i = range(start,l)

bx = polyfit(i,x,0)
by = polyfit(i,y,0)
bz = polyfit(i,z,0)

trendx, _ = polyfit(i,x,1)
trendy, _ = polyfit(i,y,1)
trendz, _ = polyfit(i,z,1)

print("sample size : %i, during %.3f sec, sample rate : %f Hz" % (len(x), len(x)*d.sampleRate, 1/d.sampleRate))
print("bx %.9f, by %.9f, bz %.9f" % (bx, by, bz))
print("nx %f, ny %f, nz %f" % (std(x),std(y),std(z)))
print("trendx %.9f, trendy %.9f, trendz %.9f" % (trendx, trendy, trendz))