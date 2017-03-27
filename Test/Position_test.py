from MathLib import toVector
from Position import Position
from Settings import DT
from Velocity import Velocity
import unittest


class Position_test(unittest.TestCase):
    
    def test_init(self):
        pos = Position(toVector(100, 200, 300))
        self.assertEqual(100, pos.values[0])
        self.assertEqual(200, pos.values[1])
        self.assertEqual(300, pos.values[2])
        
    def test_update(self):
        pos = Position(toVector(500., 1100., 250.))
        vel = Velocity(toVector(10., 20., 5.))
        pos.update(vel)
        self.assertEqual(500. + DT * 10., pos.values[0])
        self.assertEqual(1100. + DT * 20., pos.values[1])
        self.assertEqual(250. + DT * 5., pos.values[2])
    
if __name__ == '__main__':
    unittest.main()        
