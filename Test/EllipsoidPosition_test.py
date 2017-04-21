import unittest
from math import pi
from EllipsoidPosition import EllipsoidPosition
from MathLib import toVector
from Velocity import Velocity
from numpy import rad2deg, deg2rad
from Settings import DT

class Position_test(unittest.TestCase):
    def test_init(self):
        pos_berlin = toVector(52.521918/180*pi, 13.413215/180*pi, 100.)
        p = EllipsoidPosition(pos_berlin)
        self.assertEqual(52.521918/180*pi, p.values[0])
        self.assertEqual(13.413215/180*pi, p.values[1])
        self.assertEqual(100., p.values[2])
        self.assertIsInstance(p.a, (int, float))
        self.assertIsInstance(p.f, (int, float))
        
    def test_update(self):
        pos = toVector(deg2rad(10.), deg2rad(200.), 0.)
        vel = Velocity(toVector(5., 4., 1.))
        p = EllipsoidPosition(pos)
        p.update(vel)
        self.assertAlmostEqual(10., rad2deg(p.values[0]), delta = 0.00001) 
        self.assertAlmostEqual(200., rad2deg(p.values[1]), delta = 0.00001)
        self.assertEqual(1.*DT, p.values[2])
        
    def test_update_2(self):
        p = EllipsoidPosition(toVector(deg2rad(51.),deg2rad(10.),0.))
        vel = Velocity(toVector(1./DT,2./DT,0.)) #equal to 1 and 2 meters 
        p.update(vel)
        self.assertAlmostEqual(51.+8.988903268e-06,rad2deg(p.values[0].item()), delta =10e-06) 
        self.assertAlmostEqual(10.+1.28368253e-05,rad2deg(p.values[1]), delta = 10e-06) 
        
if __name__ == '__main__':
    unittest.main()  