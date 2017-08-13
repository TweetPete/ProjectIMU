from MathLib import pythagoras, toVector, toValue, mvMultiplication
from math import sin, cos, atan2, asin
from numpy import matrix, insert, long

class Quaternion (object):
    """ class Quaternion describes the transformation between 2 coordinate systems using 4 parameters
    """
    def __init__(self, euler=toVector(0., 0., 0.)):
        """ Quaternion is initiated by Euler angles
            the angles are given in radians using ZYX-convention
        """
        phi, theta, psi = toValue(euler)
        
        ph2 = phi / 2
        th2 = theta / 2
        ps2 = psi / 2
        
        q0 = cos(ph2) * cos(th2) * cos(ps2) + sin(ph2) * sin(th2) * sin(ps2)
        q1 = sin(ph2) * cos(th2) * cos(ps2) - cos(ph2) * sin(th2) * sin(ps2)
        q2 = cos(ph2) * sin(th2) * cos(ps2) + sin(ph2) * cos(th2) * sin(ps2)
        q3 = cos(ph2) * cos(th2) * sin(ps2) - sin(ph2) * sin(th2) * cos(ps2)
        
        self.values = toVector(q0, q1, q2, q3)
    
    def __str__(self):
        q0, q1, q2, q3 = toValue(self.values)
        return 'q0: {:2.3f}, q1: {:2.3f}, q2: {:2.3f}, q3: {:2.3f}'.format(q0,q1,q2,q3)    

    def __mul__(self, value):
        """ multiplicates self with another Quaternionen combining both rotations
            return is a new Quaternion-object 
        """
        new_quat = Quaternion()
        if isinstance(value, Quaternion):
            new_quat.values = mvMultiplication(self.values, value.values)
            return new_quat
        elif isinstance(value, (int, long, float)): 
            print('scalar multiplication is not implemented yet')
        
    def getRotationMatrix(self):
        """ creates the 3x3 rotation matrix from quaternion parameters 
            represents the same relation between coordinate systems
            return a numpy.matrix
        """
        q0, q1, q2, q3 = toValue(self.values)
        
        r11 = q0**2+q1**2-q2**2-q3**2
        r22 = q0**2-q1**2+q2**2-q3**2
        r33 = q0**2-q1**2-q2**2+q3**2
        r12 = 2 * (q1 * q2 - q0 * q3)
        r13 = 2 * (q1 * q3 + q0 * q2)
        r23 = 2 * (q2 * q3 - q0 * q1)
        r21 = 2 * (q1 * q2 + q0 * q3)
        r31 = 2 * (q1 * q3 - q0 * q2)
        r32 = 2 * (q2 * q3 + q0 * q1)
        
        return matrix([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])
    
    def getEulerAngles(self):
        """ calculates Euler angles from the current Quaternion
            result is given in a 3x1 vector in radians
        """
        
        q0, q1, q2, q3 = toValue(self.values)
    
        try:
            phi = atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 ** 2 + q2 ** 2))
            st = 2 * (q0 * q2 - q3 * q1)
            st =  1 if st > 1 else st #gimbal lock
            st = -1 if st < -1 else st
            theta = asin(st)    
            psi = atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 ** 2 + q3 ** 2))
        except ValueError:
            raise ValueError('Quaternion is invalid', q0, q1, q2, q3)
        
        return toVector(phi, theta, psi)
    
    def update(self, rotationRate, DT):
        """ updates the quaternion via the rotation of the last period
            the rotation rate is a 3x1 vector - wx, wy, wz
            approximated quaternion differential equation
        """
        w = rotationRate * DT
        wx, wy, wz = toValue(w)
        norm = pythagoras(wx, wy, wz)

        # exact formula 
#         r1 = cos(norm/2)
#         factor = 1/norm * sin(norm/2)
#         r234 = w*factor

        # series expansion 
        r1 = 1 - (1 / 8) * norm ** 2 + (1 / 384) * norm ** 4 - (1 / 46080) * norm ** 6
        factor = 0.5 - (1 / 48) * norm ** 2 + (1 / 3840) * norm ** 4 - (1 / 645120) * norm ** 6
        r234 = w * factor
        r = insert(r234, 0, r1)
        
        self.values = mvMultiplication(self.values, r.transpose())
         
    def vecTransformation(self, vector):
        """ transformation via quaternion like q . vector . q*
            the vector has the dimension 3x1
            return a 3x1 vector
        """
        vector = insert(vector, 0, 0)
        vector = vector.transpose()
        
        f1 = mvMultiplication(self.values,vector)
        
        conjQuat = self.getConjugatedQuaternion()
        res = mvMultiplication(f1, conjQuat.values)
        return res[1:4]

    def getConjugatedQuaternion(self):
        """ returns the conjugated quaternion 
        """
        conjQuat = Quaternion()
        q0,q1,q2,q3 = toValue(self.values)
        conjQuat.values = toVector(q0,-q1,-q2,-q3)
        return conjQuat
    
def main():
    q = Quaternion()
    q2 = Quaternion()
    z = q*q2
    print(z)
    
if __name__ == "__main__":
    main()  