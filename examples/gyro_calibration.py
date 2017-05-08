from FileManager import FileManager
from numpy import polyfit, std

filePath = "data\\arduino10DOF\gyro_calibration_long.csv"
col_gyro = range(1,4)
col_accel = range(4,7)
col_mag = range(7,10)
d = FileManager(filePath, columns=col_gyro, skip_header = 7)
v = d.values

x = v[:,0]
y = v[:,1]
z = v[:,2]
i = range(0,d.length)

bx = polyfit(i,x,0)
by = polyfit(i,y,0)
bz = polyfit(i,z,0)

trendx, _ = polyfit(i,x,1)
trendy, _ = polyfit(i,y,1)
trendz, _ = polyfit(i,z,1)

print("sample size : %i, during %.3f sec" % (len(x), len(x)*d.sampleRate))
print("bx %.9f, by %.9f, bz %.9f" % (bx, by, bz))
print("nx %f, ny %f, nz %f" % (std(x),std(y),std(z)))
print("trendx %f, trendy %f, trendz %f" % (trendx, trendy, trendz))

# ph = PlotHelper()
# ph.subplot(i, x, 'ro',311)
# ph.subplot((i[0], i[-1]), (bx, bx), 'k-', 311)
# ph.subplot(i, y, 'ro',312)
# ph.subplot((i[0], i[-1]), (by, by), 'k-', 312)
# ph.subplot(i, z, 'ro',313)
# ph.subplot((i[0], i[-1]), (bz, bz), 'k-', 313)
# 
# ph.show()


