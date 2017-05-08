import unittest
from LowPassFilter import LowPassFilter

class LowPassFilter_test(unittest.TestCase):
    def test_init(self):
        lp = LowPassFilter()
        self.assertEqual(lp.n, 1)
        
    def test_mean(self):
        lp = LowPassFilter()
        v = 0.
        for new in (1,2,3,4,5,6,7,8,9,10):
            v = lp.mean(v, new)
        self.assertEqual(lp.n, 11)
        self.assertEqual(v, 5.5)
        
    def test_mean_negative(self):
        lp = LowPassFilter()
        v = 0.
        for new in (1,2,3,4,5,6,7,8,9,10):
            v = lp.mean(v, -new)
        self.assertEqual(lp.n, 11)
        self.assertEqual(v, -5.5)
        
if __name__ == '__main__':
    unittest.main() 