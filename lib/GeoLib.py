""" Geodetic Library
""" 

from math import sqrt, sin, cos
from MathLib import toValue, toVector

def earthCurvature(a,f,lat):
    """ calculates radius of curvature in North and East
        takes ellipsoidal parameters as argument 
    """
    e = sqrt(f*(2-f))
    Rn = a *((1-e**2)/(1-e**2*(sin(lat))**2)**(3/2))
    Re = a/sqrt(1-e**2*(sin(lat))**2)
    return Rn, Re

def ell2xyz(pos_obj):
    """ transformation of geographic coordinates to cartesian coordinates
        input is an EllipsoidPosition-object
        returns a 3x1 vector
    """
    lat, lon, he = toValue(pos_obj.values)
    _, N = earthCurvature(pos_obj.a, pos_obj.f, lat)
    x = (N + he) * cos(lat)*cos(lon)
    y = (N + he) * cos(lat)*sin(lon)
    z = N * sin(lat)*(pos_obj.b**2/pos_obj.a**2) + he*sin(lat)
    return toVector(x,y,z)