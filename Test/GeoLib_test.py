import unittest
from GeoLib import earthCurvature
from math import pi

class GeoLib_test(unittest.TestCase):
    def test_earthCurvature(self):
        a = 6378137.0
        f = 1/298.257223563
        Rn, Re = earthCurvature(a,f,pi/4)
        self.assertAlmostEqual(Re, 6388838.2901, delta=0.0001)
        self.assertAlmostEqual(Rn, 6367381.8156, delta=0.0001)
        
if __name__ == '__main__':
    unittest.main() 