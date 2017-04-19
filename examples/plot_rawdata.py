import matplotlib.pyplot as plt
from FileManager import FileManager
from MathLib import toVector

f = FileManager()
filePath = "data\Sample9DoF_R_Session1_Shimmer_B663_Calibrated_SD.csv"
d = f.readFile(filePath)

for i in range(2000,7000,10):
    #acceleration = toVector(d[i,0],d[i,1],d[i,2])
    #rotationRate = toVector(d[i,3],d[i,4],d[i,5])*pi/180 
    magneticField = toVector(d[i,6],d[i,7],d[i,8])

    red_dot, = plt.plot(i, magneticField[0], "ro")
    blue_dot, = plt.plot(i, magneticField[1], "bo")
    green_dot, = plt.plot(i, magneticField[2], "go")
    
plt.show()
