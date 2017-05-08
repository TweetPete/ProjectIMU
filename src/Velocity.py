""" class Velocity propagates the velocity based on previous velocity and acceleration
"""
from MathLib import toVector
from Settings import DT, G

class Velocity(object):
    
    def __init__(self, vector=toVector(0., 0., 0.)):
        """ initialized by velocity-vector
            units in m/s
        """
        self.values = vector
        
    def update(self, acceleration, quaternion):
        """ updates velocity based on acceleration
            acceleration given in m/s2 
        """
        an = quaternion.vecTransformation(acceleration)        
        self.values += DT * (an + G)
