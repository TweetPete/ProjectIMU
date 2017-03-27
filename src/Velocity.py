from MathLib import toVector
from Settings import DT, G


class Velocity(object):
    
    def __init__(self, vector=toVector(0., 0., 0.)):
        self.values = vector
        
    def update(self, acceleration, quaternion):
        an = quaternion.vecTransformation(acceleration)        
        self.values += DT * (an - G)
