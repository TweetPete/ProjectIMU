""" class EllipsoidPosition discribes the propagation of the ellipsoidal position
    depending a velocity and the previous position
"""

from MathLib import toValue
from Settings import DT
from GeoLib import earthCurvature
from numpy import eye
from math import cos

class EllipsoidPosition(object):
    def __init__(self, vector):
        """ gets initialized by position-vector 
            units are kept in radian using lat, lon, h-order 
            used ellisoid-model is GRS80
        """
        self.values = vector
        self.a = 6378137.0 #GRS80
        self.f = 1/298.257223563
        
    def update(self, velocity):
        """ updates the current position via a velocity-vector 
            velocity-object has attribute values in m/s 
        """
        lat,_,h = toValue(self.values)
        Rn, Re = earthCurvature(self.a,self.f,lat)
        M = eye(3,3)
        M[0,0] = 1/(Rn-h)
        M[1,1] = 1/((Re-h))*cos(lat)
        M[2,2] = 1
        
        self.values += (DT * M) * velocity.values
