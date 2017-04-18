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
    d = f.readFile()

    for i in range(1,2):   
        print(i) 
        acceleration = toVector(d[i,0],d[i,1],d[i,2])
        rotationRate = toVector(d[i,3],d[i,4],d[i,5])*pi/180
        magneticField = toVector(d[i,6],d[i,7],d[i,8])
        
        #acceleration = toVector(1., 2., 9.81)
        #magneticField = toVector(3., 5., 7.)
        s = Strapdown(acceleration, magneticField)
        print('bearing\n', s.bearing.values)
        print('velocity\n', s.velocity.values)
        print('position\n', s.position.values)
            
        #rotationRate = toVector(0.1, 0.2, 0.1)
        #acceleration = toVector(1.5, 2.4, 8.75)
            
        s.quaternion.update(rotationRate)
        s.bearing.values = s.quaternion.getEulerAngles()
        s.velocity.update(acceleration, s.quaternion)
        s.position.update(s.velocity)
            
        print('bearing\n', s.bearing.values)
        print('velocity\n', s.velocity.values)
        print('position\n', s.position.values)
            
        K = Kalman()
        K.timeUpdate(s.quaternion)
        K.measurementUpdate(acceleration, magneticField, s.quaternion)
        
        print("kompensierte Lage = : \n",s.bearing.values - K.bearingError)
        print("kompensierte Drehrate = : \n",rotationRate - K.gyroBias)
        
        K.bearingError = 0 
        K.gyroBias = 0
    
    
if __name__ == "__main__":
    main()         
        

    
        
