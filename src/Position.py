from MathLib import toVector
from Settings import DT


class Position(object):
    
    def __init__(self, vector=toVector(0., 0., 0.)):
        self.values = vector
        
    def update(self, velocity):
        self.values += DT * velocity.values
