from Euler import Euler
from MathLib import toVector
from math import pi
import unittest
from Settings import EARTHMAGFIELD
from numpy import rad2deg

class Euler_test(unittest.TestCase):
    
    def test_init(self):
        acc = toVector(1., 2., -10.)
        mag = toVector(50., 100., 120.)
        b = Euler(acc, mag)
        self.assertAlmostEqual(-0.197 , b.values[0], delta=0.01)
        self.assertAlmostEqual(0.102, b.values[1], delta=0.01)
        self.assertAlmostEqual(1.047, b.values[2], delta=0.01)
        
    def test_init_north(self):
        acc = toVector(0.,0.,-10.)
        b = Euler(acc, EARTHMAGFIELD)
        self.assertAlmostEqual(0. , b.values[0], delta=0.01)
        self.assertAlmostEqual(0., b.values[1], delta=0.01)
        self.assertAlmostEqual(0., rad2deg((b.values[2])), delta = 0.01)
        
    def test_init_Null_acc(self):
        acc = toVector(0.,0.,0.) 
        mag = toVector(1.,1.,1.)
        self.assertRaises(ValueError,Euler,acc, mag)
        
    def test_init_Null_mag(self):
        acc = toVector(1.,1.,1.) 
        mag = toVector(0.,0.,0.)
        self.assertRaises(ValueError,Euler,acc, mag)
        
    def test_init_plane(self):
        acc = toVector(0.,0.,-9.81)
        mag = toVector(1.,1.,1.)
        b = Euler(acc, mag)
        self.assertEqual(0., abs(b.values[0]))
        self.assertEqual(0., abs(b.values[1]))
    
    def test_init_upsidedown(self):
        acc = toVector(0.,0.,9.81)
        mag = toVector(1.,1.,1.)
        b = Euler(acc, mag)
        self.assertEqual(pi, abs(b.values[0]))
        self.assertEqual(0., abs(b.values[1]))    
    
if __name__ == '__main__':
    unittest.main()   
