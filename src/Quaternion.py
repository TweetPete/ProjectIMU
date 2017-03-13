""" class Quaternion describes the relation between 2 coordinate systems using 4 parameters
"""

from math import sin, cos, pow, atan2, asin
from numpy import matrix, insert
from MathLib import pythagoras, toVector, toValue, mvMultiplication

class Quaternion (object):

    def __init__(self, rotationRate):
        """ Quaternion es initiated by Euler angles
            the angles are given in radians
        """
        phi, theta, psi = toValue(rotationRate)
        
        ph2 = phi / 2
        th2 = theta / 2
        ps2 = psi / 2
        
        self.q0 = cos(ph2) * cos(th2) * cos(ps2) + sin(ph2) * sin(th2) * sin(ps2)
        self.q1 = sin(ph2) * cos(th2) * cos(ps2) - cos(ph2) * sin(th2) * sin(ps2)
        self.q2 = cos(ph2) * sin(th2) * cos(ps2) + sin(ph2) * cos(th2) * sin(ps2)
        self.q3 = cos(ph2) * cos(th2) * sin(ps2) - sin(ph2) * sin(th2) * cos(ps2)
        
    def getRotationMatrix(self):
        """ creates the 3x3 rotation matrix from quaternion parameters 
            represents the same relation between coordinate systems
        """
        r11 = 2 * pow(self.q0, 2) - 1 + 2 * pow(self.q1, 2)
        r22 = 2 * pow(self.q0, 2) - 1 + 2 * pow(self.q2, 2)
        r33 = 2 * pow(self.q0, 2) - 1 + 2 * pow(self.q3, 2)
        r12 = 2 * (self.q1 * self.q2 + self.q0 * self.q3)
        r13 = 2 * (self.q1 * self.q3 - self.q0 * self.q2)
        r23 = 2 * (self.q2 * self.q3 + self.q0 * self.q1)
        r21 = 2 * (self.q1 * self.q2 - self.q0 * self.q3)
        r31 = 2 * (self.q1 * self.q3 + self.q0 * self.q2)
        r32 = 2 * (self.q2 * self.q3 - self.q0 * self.q1)
        
        return matrix([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])
    
    def getEulerAngles(self):
        """ calculates Euler angles from the current Quaternion
            result is given in a 1x3 vector 
        """
#         phi = atan2(2*(self.q2*self.q3 - self.q0*self.q1), 2*self.q0**2 - 1 + 2*self.q3**2)
#         theta = -atan2(2*(self.q1*self.q3 + self.q0*self.q2), sqrt(1-(2*self.q1*self.q3 + 2*self.q0*self.q2)**2))
#         psi = atan2(2*(self.q1*self.q2 - self.q0*self.q3), 2*self.q0**2 - 1 + 2*self.q1**2)
    
        # Wikipedia
        phi = atan2(2*(self.q0*self.q1 + self.q2*self.q3), 1 - 2*(self.q1**2 + self.q2**2))
        theta = asin(2*(self.q0*self.q2 - self.q3*self.q1))
        psi = atan2(2*(self.q0*self.q3 + self.q1*self.q2), 1 - 2*(self.q2**2 + self.q3**2))
        
        return toVector(phi, theta, psi)
    
    def update(self, rotationRate):
        """ updates the quaternion via the rotation of the last period
            the rotation rate is a 1x3 vector - wx, wy, wz
            approximated quaternion differential equation
        """
        w = rotationRate  # changing rate of the orientation vector - w * T (wo earth rotation rate and transport rate)
        wx, wy, wz = toValue(w)
        norm = pythagoras(wx, wy, wz)
        
#         r1 = cos(norm/2)
#         factor = 1/norm * sin(norm/2)
#         r234 = w*factor

        # series expansion (Reihenentwicklung)
        r1 = 1 - (1 / 8) * norm ** 2 + (1 / 384) * norm ** 4 - (1 / 46080) * norm ** 6
        factor = 0.5 - (1 / 48) * norm ** 2 + (1 / 3840) * norm ** 4 - (1 / 645120) * norm ** 6
        r234 = w * factor
        r = insert(r234, 0, r1)
        
        newQuat = self.quatMultiplication(r.transpose())
 
        self.q0 = newQuat[0].item()
        self.q1 = newQuat[1].item()
        self.q2 = newQuat[2].item()
        self.q3 = newQuat[3].item()

    def quatMultiplication(self, vector):
        """ transformation via quaternion like q . vector
            the vector has the dimension 4x1
        """
        quaternion = toVector(self.q0, self.q1, self.q2, self.q3) 
         
        return mvMultiplication(quaternion, vector)
    
    def vecTransformation(self, vector):
        vector = insert(vector, 0, 0)
        vector = vector.transpose()
        
        f1 = self.quatMultiplication(vector)
        conjQuat = toVector(self.q0, -self.q1, -self.q2, -self.q3)
        res = mvMultiplication(f1, conjQuat)
        return res[1:4]