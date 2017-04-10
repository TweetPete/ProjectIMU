""" Geodetic Library
""" 

from math import sqrt, sin

def earthCurvature(a,f,lat):
    e = sqrt(f*(2-f))
    Rn = a *((1-e**2)/(1-e**2*(sin(lat))**2)**(3/2))
    Re = a/sqrt(1-e**2*(sin(lat))**2)
    return Rn, Re