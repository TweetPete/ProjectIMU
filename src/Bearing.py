from math import atan2, tan, sin, cos
from MathLib import pythagoras, toVector, toValue
from Settings import DT

class Bearing(object):
        
    def __init__(self, acceleration, magneticField):
        """ calculates the bearing from raw acceleration and magnetometer values
            accelaration in m/s2 and magnetic field in gauss
        """
        ax, ay, az = toValue(acceleration)
        mx, my, _ = toValue(magneticField)
        
        phi = atan2(ay, az)
        if ay == 0 and az == 0: theta = 0 #axes wo Earth acceleration 
        else: theta = tan(-ax / pythagoras(ay, az))
        psi = atan2(-mx, my)  # +- D Deklinationswinkel # nur gültig wenn eben
        
        self.values = toVector(phi, theta, psi)

    def update(self, rotationRate):
        """ updates bearing by just using Euler angles and the rotation rate 
        """
        
        phi, theta, _ = toValue(self.values)
        wx, wy, wz = toValue(rotationRate*DT)
                
        dPhi = (wy*sin(phi) + wz*cos(phi)) *tan(theta) + wx 
        dTheta = wy *cos(phi) - wz*sin(phi)
        dPsi = (wy *sin(phi) + wz* cos(phi))/cos(theta)
        
        self.values += toVector(dPhi, dTheta, dPsi) 