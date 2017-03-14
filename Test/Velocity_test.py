import unittest

from MathLib import toVector
from Velocity import Velocity
from Settings import DT, G
from Quaternion import Quaternion

class Velocity_test(unittest.TestCase):
    
    def test_init(self):
        vel = Velocity(toVector(3,4,-6))
        self.assertEqual(3,vel.values[0])
        self.assertEqual(4,vel.values[1])
        self.assertEqual(-6,vel.values[2])
        
    def test_update(self):
        vel = Velocity(toVector(3., 1., 2.))
        acc = toVector(0.1, 2., 10.)
        vel.update(acc , Quaternion(toVector(0., 0., 0.)))
        self.assertEqual(3.+DT*(0.1-G[0]),vel.values[0])
        self.assertEqual(1.+DT*(2.-G[1]),vel.values[1])
        self.assertEqual(2.+DT*(10.-G[2]),vel.values[2])        
    
if __name__=='__main__':
    unittest.main()        