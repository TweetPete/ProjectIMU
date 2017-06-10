import unittest
from unittest.mock import patch
from math import pi
from EllipsoidPosition import EllipsoidPosition
from MathLib import toVector
from Velocity import Velocity
from numpy import rad2deg, deg2rad

class Position_test(unittest.TestCase):
    def test_init(self):
        pos_berlin = toVector(52.521918/180*pi, 13.413215/180*pi, 100.)
        p = EllipsoidPosition(pos_berlin)
        self.assertEqual(52.521918/180*pi, p.values[0])
        self.assertEqual(13.413215/180*pi, p.values[1])
        self.assertEqual(100., p.values[2])
        self.assertIsInstance(p.a, (int, float))
        self.assertIsInstance(p.f, (int, float))
        
    @patch('EllipsoidPosition.DT',0.1)    
    def test_update(self):
        pos = toVector(deg2rad(10.), deg2rad(200.), 0.)
        vel = Velocity(toVector(50000., 40000., 10000.))
        p = EllipsoidPosition(pos)
        p.update(vel)
        self.assertAlmostEqual(10.04520478, rad2deg(p.values[0]), delta = 1e-8) 
        self.assertAlmostEqual(200.03538314, rad2deg(p.values[1]), delta = 1e-8)
        self.assertEqual(1000., p.values[2])
    
    @patch('EllipsoidPosition.DT',0.1)            
    def test_update_2(self):
        p = EllipsoidPosition(toVector(deg2rad(51.),deg2rad(10.),0.))
        vel = Velocity(toVector(10.,20.,0.)) #equal to 1 and 2 meters 
        p.update(vel)
        self.assertAlmostEqual(51.+8.988903268e-06,rad2deg(p.values[0].item()), delta =10e-06) 
        self.assertAlmostEqual(10.+1.28368253e-05,rad2deg(p.values[1]), delta = 10e-06) 
        
if __name__ == '__main__':
    unittest.main()  