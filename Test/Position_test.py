from MathLib import toVector
from Position import Position
from Velocity import Velocity
import unittest
# from unittest.mock import patch

class Position_test(unittest.TestCase):
    
    def test_init(self):
        pos = Position(toVector(100, 200, 300))
        self.assertEqual(100, pos.values[0])
        self.assertEqual(200, pos.values[1])
        self.assertEqual(300, pos.values[2])
        
    #@patch('Position.DT',1.)    
    def test_update(self):
        pos = Position(toVector(500., 1100., 250.))
        vel = Velocity(toVector(10., 20., 5.))
        pos.update(vel,1.)
        self.assertEqual(510., pos.values[0])
        self.assertEqual(1120., pos.values[1])
        self.assertEqual(255., pos.values[2])
    
if __name__ == '__main__':
    unittest.main()        
