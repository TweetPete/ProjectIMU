from math import atan2, tan, sin, cos
from MathLib import pythagoras, toVector, toValue

class Bearing(object):
    
    def __init__(self):
        self.bearing = toVector(0.,0.,0.)
    
    def initBearing(self, acceleration, magneticField):
        """ calculates the bearing from raw acceleration and magnetometer values
            accelaration in m/s2 and magnetic field in gauss
        """
        ax, ay, az = toValue(acceleration)
        mx, my, _ = toValue(magneticField)
        
        phi = atan2(ay, az)
        theta = tan(-ax / pythagoras(ay, az))
        psi = atan2(-mx, my)  # +- D Deklinationswinkel
        
        self.bearing = toVector(phi, theta, psi)

    def update(self, rotationRate):
        """ updates bearing by just using Euler angles and the rotation rate 
        """
        
        phi, theta, _ = toValue(self.bearing)
        wx, wy, wz = toValue(rotationRate)
                
        dPhi = (wy*sin(phi) + wz*cos(phi)) *tan(theta) + wx 
        dTheta = wy *cos(phi) - wz*sin(phi)
        dPsi = (wy *sin(phi) + wz* cos(phi))/cos(theta)
        
        return toVector(dPhi, dTheta, dPsi) 