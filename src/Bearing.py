from math import atan2, tan, sin, cos
from MathLib import pythagoras, toVector, toValue
from Settings import DT

class Bearing(object):
        
    def __init__(self, acceleration, magneticField):
        """ calculates the bearing from raw acceleration and magnetometer values
            accelaration in m/s2 and magnetic field in gauss
        """
        ax, ay, az = toValue(acceleration)
        mx, my, mz = toValue(magneticField)
        
        phi = atan2(ay, az)
        if ay == 0 and az == 0: theta = 0 #axes wo Earth acceleration 
        else: theta = tan(-ax / pythagoras(ay, az))
        
        # transformation to horizontal coordinate system - psi = 0
        mxh = mx*cos(theta) + my *sin(phi)*sin(theta)+ mz *cos(phi)*sin(theta)
        myh = my*cos(phi) - mz*sin(phi)
        psi = atan2(-mxh, myh)  # +- D Deklinationswinkel 
        
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