from MathLib import pythagoras, toVector, toValue
from Settings import g, DECANGLE, EARTHMAGFIELD, G
from math import atan2, asin, isclose, pi
from Quaternion import Quaternion
from numpy import rad2deg

class Euler(object):
        
    def __init__(self, acceleration = -G, magneticField = EARTHMAGFIELD):
        """ calculates the bearing from raw acceleration and magnetometer values
            accelaration in m/s2 and magnetic field in gauss
            angles are saved in radians
            calling w/o arguments creates a vector with phi, theta, psi = 0
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
        
        psi = atan2(myh, mxh) - DECANGLE
        
        self.values = toVector(phi, theta, psi)

    def __str__(self):
        return '{:deg}'.format(self)
    
    def __format__(self, f):
        phi, theta, psi = toValue(self.values)
        if f == 'deg':
            return 'Roll: {:4.3f} deg, Pitch: {:4.3f} deg, Yaw: {:4.3f} deg'.format(rad2deg(phi), rad2deg(theta), rad2deg(psi))
        elif f== 'rad':
            return 'Roll: {:4.3f} rad, Pitch: {:4.3f} rad, Yaw: {:4.3f} rad'.format(phi, theta, psi)

def main():
    E = Euler()
    E.values = toVector(pi/2, pi/4, pi/6)
    print('{:rad}'.format(E))
    print(E)
    
if __name__ == "__main__":
    main()  
