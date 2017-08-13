import unittest
from unittest.mock import patch
from Strapdown import Strapdown
from Quaternion import Quaternion
from Velocity import Velocity
from Position import EllipsoidPosition
from MathLib import toVector, toValue

class Strapdown_test(unittest.TestCase):
    def test_init(self):
        s = Strapdown()
        self.assertIsInstance(s.quaternion, Quaternion)
        self.assertIsInstance(s.velocity, Velocity)
        self.assertIsInstance(s.position, EllipsoidPosition)
        self.assertFalse(s.isInitialized)
        
    @patch('Euler.DECANGLE',0.) 
    @patch('Euler.g',10.)   
    def test_Initialize(self):
        s = Strapdown()
        s.Initialze(toVector(0.,0.,-10.), toVector(1.,0.,0.), toVector(10.,5.,12.))
        self.assertTrue(s.isInitialized)
        q0,q1,q2,q3 = toValue(s.quaternion.values)
        self.assertEqual(q0, 1.)
        self.assertEqual(q1, 0.)
        self.assertEqual(q2, 0.)
        self.assertEqual(q3, 0.)
        x,y,z = toValue(s.position.values)
        self.assertEqual(x, 10.)
        self.assertEqual(y, 5.)
        self.assertEqual(z, 12.)
    
    def test_getOrientation(self):
        s = Strapdown()
        e1, e2, e3 = toValue(s.getOrientation())
        self.assertEqual(e1, 0.)
        self.assertEqual(e2, 0.)
        self.assertEqual(e3, 0.)
        
    def test_getVelocity(self):
        s = Strapdown()
        v1, v2, v3 = toValue(s.getVelocity())
        self.assertEqual(v1, 0.)
        self.assertEqual(v2, 0.)
        self.assertEqual(v3, 0.)
        
    def test_getPosition(self):
        s = Strapdown()
        p1, p2, p3 = toValue(s.getPosition())
        self.assertEqual(p1, 0.)
        self.assertEqual(p2, 0.)
        self.assertEqual(p3, 0.)

if __name__ == '__main__':
    unittest.main() 