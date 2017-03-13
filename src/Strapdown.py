""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""

from numpy import matrix
from Quaternion import Quaternion
from Bearing import Bearing
from Velocity import Velocity
from MathLib import toVector

class Strapdown(object):
    def __init__(self):
        """ creates Strapdown object which includes the current bearing, velocity and position
            bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """
                        
        self.bearing = Bearing()
        self.velocity = Velocity()
        self.position = matrix([0,0,0])
        self.quaternion = Quaternion(toVector(0,0,0))
        

        
