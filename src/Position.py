from MathLib import toVector
from Velocity import Velocity as v
from Settings import DT

class Position(object):
    
    def __init__(self):
        self.position = toVector(0,0,0)
        
    def update(self):
        self.position += DT*v.velocity