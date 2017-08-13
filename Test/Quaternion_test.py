import unittest
# from unittest.mock import patch
from Quaternion import Quaternion
from math import pi, sin, cos
from MathLib import toVector, toValue, pythagoras
from numpy import matrix, deg2rad

class Quaternion_test(unittest.TestCase):
    def test_init_empty(self):
        q = Quaternion()
        q0,q1,q2,q3 = toValue(q.values)
        self.assertEqual(q0, 1.)
        self.assertEqual(q1, 0.)
        self.assertEqual(q2, 0.)
        self.assertEqual(q3, 0.)
        
    def test_init_values(self):
        q=Quaternion(toVector(1.,0.5,-0.5))
        q0,q1,q2,q3 = toValue(q.values)
        self.assertAlmostEqual(q0, 0.795, delta = 0.001)
        self.assertAlmostEqual(q1, 0.504, delta = 0.001)
        self.assertAlmostEqual(q2, 0.095, delta = 0.001)
        self.assertAlmostEqual(q3, -0.325, delta = 0.001)
        
    def test_getRotationMatrix(self):
        phi = 1.
        theta = 0.5
        psi = -0.5
        q=Quaternion(toVector(phi, theta, psi))
        mat = q.getRotationMatrix()
        mat2 = matrix([[cos(theta)*cos(psi),-cos(phi)*sin(psi)+sin(phi)*sin(theta)*cos(psi),sin(phi)*sin(psi)+cos(phi)*sin(theta)*cos(psi)],
                       [cos(theta)*sin(psi),cos(phi)*cos(psi)+sin(phi)*sin(theta)*sin(psi),-sin(phi)*cos(psi)+cos(phi)*sin(theta)*sin(psi)],
                       [-sin(theta),sin(phi)*cos(theta),cos(phi)*cos(theta)]])
        
        self.assertAlmostEqual(mat[0,0].item(), mat2[0,0].item(), delta= 0.001)
        self.assertAlmostEqual(mat[0,1].item(), mat2[0,1].item(), delta= 0.001)
        self.assertAlmostEqual(mat[0,2].item(), mat2[0,2].item(), delta= 0.001)
        
        self.assertAlmostEqual(mat[1,0].item(), mat2[1,0].item(), delta= 0.001)
        self.assertAlmostEqual(mat[1,1].item(), mat2[1,1].item(), delta= 0.001)
        self.assertAlmostEqual(mat[1,2].item(), mat2[1,2].item(), delta= 0.001)
        
        self.assertAlmostEqual(mat[2,0].item(), mat2[2,0].item(), delta= 0.001)
        self.assertAlmostEqual(mat[2,1].item(), mat2[2,1].item(), delta= 0.001)
        self.assertAlmostEqual(mat[2,2].item(), mat2[2,2].item(), delta= 0.001)
        
    def test_getEulerAngles(self):
        q = Quaternion(toVector(0.75,-0.51,pi))
        vec = q.getEulerAngles()
        phi, theta, psi = toValue(vec)
        self.assertAlmostEqual(0.75, phi, delta=0.001)
        self.assertAlmostEqual(-0.51, theta, delta=0.001)
        self.assertAlmostEqual(pi, psi, delta=0.001)
        
    #@patch('Quaternion.DT',0.01)    
    def test_update_without_rotation(self):
        q = Quaternion()
        q.update(toVector(0.0,0.0,0.0), 0.01)
        q0,q1,q2,q3 = toValue(q.values)
        self.assertEqual(q0, 1.)
        self.assertEqual(q1, 0.)
        self.assertEqual(q2, 0.)
        self.assertEqual(q3, 0.)
        
    #@patch('Quaternion.DT',0.01)    
    def test_update(self):
        q = Quaternion()
        rotationRate = toVector(-100.,50.,120.)
        q.update(rotationRate,0.01)
        q0,q1,q2,q3 = toValue(q.values)
        self.assertAlmostEqual(q0, 0.68217, delta=0.0001)
        self.assertAlmostEqual(q1, -0.44581, delta=0.0001)
        self.assertAlmostEqual(q2, 0.22291, delta=0.0001)
        self.assertAlmostEqual(q3, 0.53498, delta=0.0001)
        
    #@patch('Quaternion.DT',0.01)
    def test_update_180(self):
        q = Quaternion()
        rotationRate = toVector(0.,deg2rad(5.),0.) #rad/s
        for _ in range(3600):
            q.update(rotationRate,0.01)
        q0,q1,q2,q3 = toValue(q.values)
        self.assertAlmostEqual(q0, 0.0 , delta=0.0001)
        self.assertAlmostEqual(q1, 0.0, delta=0.0001)
        self.assertAlmostEqual(q2, 1., delta=0.0001)
        self.assertAlmostEqual(q3, 0.0, delta=0.0001)
        
    def test_concatenation(self):
        q = Quaternion()
        q_increment = Quaternion(toVector(deg2rad(10.),0.,0.))
        #q.values = mvMultiplication(q.values,q_increment.values)
        q *= q_increment
        q0,q1,q2,q3 = toValue(q.values)
        self.assertAlmostEqual(q0, 0.996, delta=0.001)
        self.assertAlmostEqual(q1, 0.087, delta=0.001)
        self.assertAlmostEqual(q2, 0., delta=0.001)
        self.assertAlmostEqual(q3, 0., delta=0.001)

    def test_concatenation_180(self):
        q = Quaternion()
        q_increment = Quaternion(toVector(deg2rad(10.),0.,0.))
        for _ in range(0,18):
            #q.values = mvMultiplication(q.values,q_increment.values)
            q *= q_increment
        q0,q1,q2,q3 = toValue(q.values)
        self.assertAlmostEqual(q0, 0., delta=0.001)
        self.assertAlmostEqual(q1, 1., delta=0.001)
        self.assertAlmostEqual(q2, 0., delta=0.001)
        self.assertAlmostEqual(q3, 0., delta=0.001)
        
    def test_concatenation_10_5_1(self):
        q = Quaternion()
        q_increment = Quaternion(toVector(deg2rad(10.),deg2rad(5.),deg2rad(1.)))
        #q.values = mvMultiplication(q.values,q_increment.values)
        q *= q_increment
        q0,q1,q2,q3 = toValue(q.values)
        self.assertAlmostEqual(q0, 0.995, delta=0.001)
        self.assertAlmostEqual(q1, 0.087, delta=0.001)
        self.assertAlmostEqual(q2, 0.044, delta=0.001)
        self.assertAlmostEqual(q3, 0.005, delta=0.001)
        
    def test_vecTransformation(self):
        q = Quaternion(toVector(0.1,0.5,0.2))
        vec1 = toVector(0.1, -2., 9.81)
        vec2 = q.vecTransformation(vec1)
        self.assertAlmostEqual(vec2[0].item(), 5.168, delta=0.001)
        self.assertAlmostEqual(vec2[1].item(), -1.982, delta=0.001)
        self.assertAlmostEqual(vec2[2].item(), 8.343, delta=0.001)
        a,b,c = toValue(vec2)
        self.assertAlmostEqual(pythagoras(0.1,-2.,9.81), pythagoras(a,b,c), delta=0.001)       
            
if __name__ == '__main__':
    unittest.main() 