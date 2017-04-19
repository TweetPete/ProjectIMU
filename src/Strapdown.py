""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""
from math import pi

from Bearing import Bearing
from MathLib import toVector
from Position import Position
from Quaternion import Quaternion
from Velocity import Velocity
from Kalman import Kalman
from FileManager import FileManager
from Settings import DT


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
    f = FileManager()
    filePath = "data\Sample9DoF_R_Session1_Shimmer_B663_Calibrated_SD.csv"
    d = f.readFile(filePath)
    
    i = 1
    acceleration = toVector(d[i,0],d[i,1],d[i,2])
    rotationRate = toVector(d[i,3],d[i,4],d[i,5])*pi/180 
    magneticField = toVector(d[i,6],d[i,7],d[i,8])*100 #*4.95283270677+ 1.67182206381
        
        #acceleration = toVector(1., 2., 9.81)
        #magneticField = toVector(3., 5., 7.)
    s = Strapdown(acceleration, magneticField)
    print('bearing\n', s.bearing.values)
    print('velocity\n', s.velocity.values)
    print('position\n', s.position.values)
            
        #rotationRate = toVector(0.1, 0.2, 0.1)
        #acceleration = toVector(1.5, 2.4, 8.75)
    gyroBias = 0
    K = Kalman()
    
    for i in range(2,50):   
        print(i)     
        
        acceleration = toVector(d[i,0],d[i,1],d[i,2])
        rotationRate = toVector(d[i,3],d[i,4],d[i,5])*pi/180 - gyroBias
        magneticField = toVector(d[i,6],d[i,7],d[i,8])/100#*4.95283270677+ 1.67182206381
        
        s.quaternion.update(rotationRate)
        s.bearing.values = s.quaternion.getEulerAngles()
        s.velocity.update(acceleration, s.quaternion)
        s.position.update(s.velocity)
            
        print('bearing\n', s.bearing.values)
        print('velocity\n', s.velocity.values)
        print('position\n', s.position.values)
            
        K.timeUpdate(s.quaternion)
        K.measurementUpdate(acceleration, magneticField, s.quaternion)
        
        print("kompensierte Lage = : \n",s.bearing.values - K.bearingError)
        print("kompensierte Drehrate = : \n",rotationRate - K.gyroBias)
        
        #K.bearingError[2] = K.bearingError[2]%(2*pi)
        s.quaternion.update(K.bearingError) #angle = rate*DT
        gyroBias = K.gyroBias 
        K.resetState()
    
if __name__ == "__main__":
    main()         
        

    
        
