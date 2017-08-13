from MathLib import toVector, toValue
from GeoLib import earthCurvature
from numpy import eye, rad2deg
from math import cos

class Position(object):
    """ class Position discribes the propagation of the position in a navigational frame
        depending a velocity and the previous position
    """
    def __init__(self, vector=toVector(0., 0., 0.)):
        """ initialized by a position-vector
            units are given in m 
        """
        self.values = vector
        
    def __str__(self):
        px, py, pz = toValue(self.values)
        return 'N: {:9.3f} m, E: {:9.3f} m, D: {:9.3f} m'.format(px, py, pz)        
        
    def update(self, velocity, DT):
        """ updates current position based on previous position and velocity
            velocity-object has attribute values in m/s
        """
        self.values += DT * velocity.values
        

class EllipsoidPosition(object):
    """ class EllipsoidPosition discribes the propagation of the position in a ECEF-frame
        depending a velocity and the previous position
    """
    def __init__(self, vector=toVector(0., 0., 0.)):
        """ gets initialized by position-vector 
            units are kept in radian using lat, lon, h-order 
            used ellisoid-model is GRS80
        """
        self.values = vector #(rad, rad, m)
        self.a = 6378137.0 #GRS80
        self.b = 6356752.314
        self.f = (self.a - self.b)/self.a
        
    def __str__(self):
        lat, lon, h = toValue(self.values)
        return 'Lat: {:4.6f} deg, Lon: {:4.6f} deg, H: {:4.3f} m'.format(rad2deg(lat), rad2deg(lon), h)        
        
    def update(self, velocity, DT):
        """ updates current position based on previous position and velocity 
            velocity-object has attribute values in m/s 
        """
        lat,_,h = toValue(self.values)
        Rn, Re = earthCurvature(self.a,self.f,lat)
        M = eye(3,3)
        M[0,0] = 1/(Rn-h)
        M[1,1] = 1/((Re-h))*cos(lat)
        M[2,2] = 1
        
        self.values += (DT * M) * velocity.values

    def correct(self, vector):
        """ vector is defined as (N, E, D) in meter 
        """
        lat,_,h = toValue(self.values)
        Rn, Re = earthCurvature(self.a,self.f,lat)
        M = eye(3,3)
        M[0,0] = 1/(Rn-h)
        M[1,1] = 1/((Re-h))*cos(lat)
        M[2,2] = 1
        
        self.values += M * vector