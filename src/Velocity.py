from MathLib import toVector
from Settings import DT, G

class Velocity(object):
    
    def __init__(self):
        self.velocity = toVector(0.,0.,0.)
        
    def update(self, acceleration, quaternion):
        an = quaternion.vecTransformation(acceleration)        
        self.velocity += DT*(an-G)