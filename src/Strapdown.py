""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""
from math import pi, sqrt

from Bearing import Bearing
from MathLib import toVector
from Position import Position
from Quaternion import Quaternion
from Velocity import Velocity
from Kalman import Kalman
from FileManager import FileManager
import matplotlib.pyplot as plt
from PlotHelper import PlotHelper

class Strapdown(object):
    def __init__(self, acceleration, magneticField):
        """ creates Strapdown object which includes the current bearing, velocity and position
            bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """
                        
        self.bearing = Bearing(acceleration, magneticField)
        self.quaternion = Quaternion(self.bearing.values)
        self.velocity = Velocity()  # vector (if known)
        self.position = Position()  # or GNSS.getPos()
        # toVector(52.521918/180*pi, 13.413215\180*pi, 100.)
        
def main():
    # read sensors
    filePath = "data\mystream_realFrame_fast.csv"
    d = FileManager(filePath)

    accelArray, rotationArray, magneticArray = convArray2IMU(d.values)

    s = Strapdown(accelArray[:,0], magneticArray[:,0])
    print('Initial bearing\n', s.bearing.values)
    print('Initial velocity\n', s.velocity.values)
    print('Initial position\n', s.position.values)
            
    gyroBias = toVector(0.,0.,0.)
    K = Kalman()
    
    ph = PlotHelper()
    
    for i in range(1,100):   
        print(i)    
        ## plot 
#         euler = s.quaternion.getEulerAngles()
#         ph.subplot(i,euler[0],"ro",311)  
#         ph.subplot(i, gyroBias[0], "bo",321)
#         ph.subplot(i,euler[1],"ro",312)  
#         ph.subplot(i, gyroBias[1], "bo",322)
#         ph.subplot(i,euler[2],"ro",313)  
#         ph.subplot(i, gyroBias[2], "bo",323)
        
        plot_handle = ph.subplot(i,(K.P[0,0]),"go",311)
        ph.subplot(i,(K.P[1,1]),"go",312)
        ph.subplot(i,(K.P[2,2]),"go",313) 
        ## plot 
             
        acceleration = accelArray[:,i]
        rotationRate = rotationArray[:,i]-gyroBias
        magneticField = magneticArray[:,i]
        
        s.quaternion.update(rotationRate)
        s.bearing.values = s.quaternion.getEulerAngles()
        s.velocity.update(acceleration, s.quaternion)
        s.position.update(s.velocity)
            
#         print('bearing\n', s.bearing.values)
#         print('velocity\n', s.velocity.values)
#         print('position\n', s.position.values)
            
        K.timeUpdate(s.quaternion)
        if i%5 == 0:
            K.measurementUpdate(acceleration, magneticField, s.quaternion)
               
            bearingOld = s.quaternion.getEulerAngles()        
            s.quaternion.update(K.bearingError) #angle = rate*DT
            bearingNew = s.quaternion.getEulerAngles()
            print("Differenz zwischen neuer und alter Lage \n",bearingNew-bearingOld)
            gyroBias = K.gyroBias 
            K.resetState()
        
    ph.show(handle = (plot_handle,), label =('Varianz Winkel-Error',))

def convArray2IMU(array):
    acceleration = toVector(array[:,1],array[:,2],array[:,3]+3.05)
    rotationRate = toVector(array[:,4],array[:,5],array[:,6])*pi/180 
    magneticField = toVector(array[:,7],-array[:,8],array[:,9])
    return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()

if __name__ == "__main__":
    main()         
        

    
        
