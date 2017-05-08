from MathLib import pythagoras, toVector, toValue
from Settings import g, DECANGLE
from math import atan2, asin, isclose
from Quaternion import Quaternion

class Euler(object):
        
    def __init__(self, acceleration, magneticField):
        """ calculates the bearing from raw acceleration and magnetometer values
            accelaration in m/s2 and magnetic field in gauss
        """
        ax, ay, az = toValue(acceleration)
        mx, my, mz = toValue(magneticField)
        if isclose(pythagoras(ax,ay,az),0.,abs_tol = 0.001): raise ValueError( "Acceleration is not significant" )
        if isclose(pythagoras(mx,my,mz),0.,abs_tol = 0.001): raise ValueError( "MagneticFlux is not significant" )
        
        phi = -atan2(ay, -az) #phi = asin(-ay/g*cos(theta))
        theta = asin(ax/g)
        
        # transformation to horizontal coordinate system - psi = 0
        q = Quaternion(toVector(phi, theta, 0.))
        mHor = q.vecTransformation(magneticField)
        mxh, myh, _ = toValue(mHor)
        
        psi = -atan2(myh, mxh) - DECANGLE
        
        self.values = toVector(phi, theta, psi)

#     def update(self, rotationRate):
#         """ updates bearing by just using Euler angles and the rotation rate 
#         """
#         
#         phi, theta, _ = toValue(self.values)
#         wx, wy, wz = toValue(rotationRate * DT)
#                 
#         dPhi = (wy * sin(phi) + wz * cos(phi)) * tan(theta) + wx 
#         dTheta = wy * cos(phi) - wz * sin(phi)
#         dPsi = (wy * sin(phi) + wz * cos(phi)) / cos(theta)
#         
#         self.values += toVector(dPhi, dTheta, dPsi) 
