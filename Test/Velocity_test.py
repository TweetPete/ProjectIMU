from MathLib import toVector
from Quaternion import Quaternion
from Velocity import Velocity
import unittest
from unittest.mock import patch
from numpy import deg2rad

class Velocity_test(unittest.TestCase):
    
    def test_init(self):
        vel = Velocity(toVector(3, 4, -6))
        self.assertEqual(3, vel.values[0])
        self.assertEqual(4, vel.values[1])
        self.assertEqual(-6, vel.values[2])
        
    @patch('Velocity.G',toVector(0.,0.,10.))  
    def test_update(self):
        vel = Velocity(toVector(3., 1., 2.))
        acc = toVector(0.1, 2., -10.)
        vel.update(acc , Quaternion(toVector(0., 0., 0.)), 1.)
        self.assertEqual(3.1, vel.values[0])
        self.assertEqual(3., vel.values[1])
        self.assertEqual(2., vel.values[2])        
    
if __name__ == '__main__':
    unittest.main()        
