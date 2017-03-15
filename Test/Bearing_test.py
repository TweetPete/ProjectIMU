import unittest

from MathLib import toVector
from Settings import DT
from Quaternion import Quaternion
from Bearing import Bearing

class Bearing_test(unittest.TestCase):
    
    def test_init(self):
        acc = toVector(1., 2., 10.)
        mag = toVector(100.,50.,120.)
        b = Bearing(acc,mag)
        self.assertAlmostEqual(0.197 ,b.values[0], delta=0.01)
        self.assertAlmostEqual(-0.098, b.values[1], delta=0.01)
        self.assertAlmostEqual(-1.285, b.values[2], delta=0.01)
        
    def test_update(self):
        acc = toVector(0., 0., 10.)
        mag = toVector(0., 1., 0.)
        rotationRate = toVector(0.1, 0.2, 0.1)
        b = Bearing(acc, mag)
        b.update(rotationRate)
        self.assertAlmostEqual(0.1*DT, b.values[0], delta=0.000001)
        self.assertAlmostEqual(0.2*DT, b.values[1], delta=0.000001)
        self.assertAlmostEqual(0.1*DT, b.values[2], delta=0.000001)
    
if __name__=='__main__':
    unittest.main()   