""" class Position discribes the propagation of the position in a navigational frame
    depending a velocity and the previous position
"""

from MathLib import toVector
from Settings import DT


class Position(object):
    
    def __init__(self, vector=toVector(0., 0., 0.)):
        """ initialized by a position-vector
            units are given in m 
        """
        self.values = vector
        
    def update(self, velocity):
        """ updates current position based on previous position and velocity
            velocity-object has attribute values in m/s
        """
        self.values += DT * velocity.values
