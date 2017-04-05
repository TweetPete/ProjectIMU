""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""

from Bearing import Bearing
from MathLib import toVector
from Position import Position
from Quaternion import Quaternion
from Velocity import Velocity
from Kalman import Kalman
from numpy import diag


class Strapdown(object):
    def __init__(self, acceleration, magneticField):
        """ creates Strapdown object which includes the current bearing, velocity and position
            bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """
                        
        self.bearing = Bearing(acceleration, magneticField)
        self.quaternion = Quaternion(self.bearing.values)
        self.velocity = Velocity()  # vector (if known)
        self.position = Position()  # or GNSS.getPos()
        
def main():
    # read sensors
    acceleration = toVector(1., 2., 9.81)
    magneticField = toVector(3., 5., 7.)
    s = Strapdown(acceleration, magneticField)
    print('bearing\n', s.bearing.values)
    print('velocity\n', s.velocity.values)
    print('position\n', s.position.values)
    
    rotationRate = toVector(0.1, 0.2, 0.1)
    acceleration = toVector(1.5, 2.4, 8.75)
    
    s.quaternion.update(rotationRate)
    s.bearing.values = s.quaternion.getEulerAngles()
    s.velocity.update(acceleration, s.quaternion)
    s.position.update(s.velocity)
    
    print('bearing\n', s.bearing.values)
    print('velocity\n', s.velocity.values)
    print('position\n', s.position.values)
    
    K = Kalman()
    K.timeUpdate(s.quaternion)
    print(K.bearingError, K.gyroBias)
    print(diag(K.P))
    
if __name__ == "__main__":
    main()         
        

    
        
