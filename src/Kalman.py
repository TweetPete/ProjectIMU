from numpy import zeros, eye, vstack, power, diag, deg2rad
from MathLib import toVector, toValue
from Settings import g, EARTHMAGFIELD, G
from Quaternion import Quaternion
import numpy as np
from GeoLib import earthCurvature
from math import cos

class Kalman(object):
    """ 6 state Kalman Filter using accelerometer and magnetometer measurements to compensate bearing-error und gyro-bias
        closed-loop-Error-state
    """    
    
    def __init__(self):
        """ class contains current state(a priori/a posteriori) 
            and system-noise and measurement-noise
            vc-matrix P is initialised as known through prior initialisation  
        """
        self.bearingError = toVector(0.,0.,0.) #stateElements
        self.gyroBias = toVector(0.,0.,0.)
        
        gyroNoise = deg2rad(0.03) #SensorNoise/systemNoise
        gyroBiasNoise = gyroNoise*0.01 #rad/s #RandomWalk
         
        accelNoise = 7. # m/s2
        magnetoNoise = 4. # muT 
         
        self.Q = getVKMatrix([gyroNoise]*3+[gyroBiasNoise]*3)
        
        self.R = getVKMatrix([accelNoise]*6+[magnetoNoise]*3)

        self.P = getVKMatrix([0.5]*3+[0.001]*3)
        
    def timeUpdate(self,quaternion, DT):
        """ requires current quaternion to compute linearized system-modell at point x0
            state a priori is propagated w/o noise 
            system-noise is uncorrelated
        """
        rotationMatrix = quaternion.getRotationMatrix()# derivation at point x0(current orientation)
        F = zeros(shape=(6,6))
        F[0:3,3:6] = rotationMatrix # Jacobi-matrix
        
        B = zeros(shape =(6,6)) # influence-matrix of noise
        B[0:3,0:3] = rotationMatrix 
        B[3:6,3:6] = eye(3,3)
                
        # discretisation
        f = eye(6, 6)+F*DT # transition-matrix f 
        
        self.P = f*self.P*f.T + B*self.Q*DT*B.T
        
    def measurementUpdate(self, acceleration, magneticField, quaternion, DT):
        """ acceleration and magneticField-measurements are needed to calculate the measurement-difference dz
            measurement-noise is uncorrelated
            measurement-matrix H is defined at x0
        """
        rotationMatrix = quaternion.getRotationMatrix()
        H1 = zeros(shape =(3,6))
        H1[0,1] =-g
        H1[1,0] = g
        H1 = -rotationMatrix.T*H1
        
        hn, he, _ = toValue(EARTHMAGFIELD)
        
        H2 = zeros(shape=(3,6))
        H2[0,2] = he
        H2[1,2] =-hn
        H2 = rotationMatrix.T*H2
        H = vstack((H1,H2))
        
        S = H*self.P*H.T+self.R
        K = self.P*H.T*S.I
        
        z0 = vstack((rotationMatrix.T*-G,rotationMatrix.T*-G,rotationMatrix.T*EARTHMAGFIELD))
        dz = vstack((acceleration,acceleration,magneticField)) - z0 # z(meas) - z(calc)
        state = vstack((self.bearingError, self.gyroBias))
        innov = dz - H*state
        newState = state+K*innov
        
        self.P = self.P - K*H*self.P        
        self.bearingError = newState[0:3]
        self.gyroBias = newState[3:6]
        
    def resetState(self):
        """ resets system state to zero after compensation of absolut values outside of this class
        """
        self.bearingError = toVector(0.,0.,0.)
        self.gyroBias = toVector(0.,0.,0.)

class KalmanPVO(object):
    """ 15 state Kalman Filter that estimates position, velocity, orientation, gyro-bias and accelerometer-bias
        based on inertial sensors and positional/velocity measurements
        closed-loop-Error-state
    """
    def __init__(self):
        """ class contains current state(a priori/a posteriori) 
            and system-noise and measurement-noise
            vc-matrix P is initialised as known through prior initialisation  
        """
        self.posError = toVector(0.,0.,0)
        self.velError = toVector(0.,0.,0)
        self.oriError = toVector(0.,0.,0)
        self.accError = toVector(0.,0.,0)
        self.gyrError = toVector(0.,0.,0)
        
        sysAccelNoise = 0.0046
        sysGyroNoise = deg2rad(0.03)
        sysAccelBiasNoise = sysAccelNoise*0.01
        sysGyroBiasNoise = deg2rad(0.03)*0.01
        
        positionNoise = 3. # m
        velocityNoise = 0.1 # m/s
        accelNoise = 7. # m/s2
        magnetoNoise = 4. # muT
        
        self.Q = getVKMatrix([sysAccelNoise]*3+[sysGyroNoise]*3+[sysAccelBiasNoise]*3+[sysGyroBiasNoise]*3)
        self.Q[0:3,0:3] = self.Q[0:3,0:3]*100
        self.Q[3:6,3:6] = self.Q[3:6,3:6]*1000
        self.Q[6:9,6:9] = self.Q[6:9,6:9]
        self.Q[9:12,9:12] = self.Q[9:12,9:12]
        self.P = getVKMatrix([4.3]*3+[1e-2]*3+[0.5]*3+[1e-6]*3+[1e-6]*3)
        self.R = getVKMatrix([positionNoise]*3+[velocityNoise]*3+[accelNoise]*3+[magnetoNoise]*3)
    
    def timeUpdate(self, acceleration,  quaternion, DT):
        """ requires current quaternion to compute linearized system-modell at point x0
            state a priori is propagated w/o noise 
            system-noise is uncorrelated
        """        
        rotationMatrix = quaternion.getRotationMatrix() # derivation at point x0(current orientation)
        F = np.matrix(zeros(shape=(15,15)))
        subMatrix = zeros(shape=(3,3))
        an, ae, ad = quaternion.vecTransformation(acceleration) # an_ib
        subMatrix[0,1] =  ad
        subMatrix[0,2] = -ae
        subMatrix[1,0] = -ad
        subMatrix[1,2] =  an
        subMatrix[2,0] =  ae
        subMatrix[2,1] = -an
        F[0:3,3:6] = eye(3,3)
        F[3:6,6:9] = subMatrix
        F[3:6,9:12] = -rotationMatrix
        F[6:9,12:15] = -rotationMatrix
        
        B = np.matrix(zeros(shape=(15,12))) # influence-matrix oof noise
        B[3:6,0:3] = rotationMatrix
        B[6:9,3:6] = rotationMatrix
        B[9:12,6:9] = eye(3,3)
        B[12:15,9:12] = eye(3,3)
        
        f = eye(15,15)+F*DT # transition-matrix f 

        self.P = f*self.P*f.T + B*self.Q*DT*B.T

    def measurementUpdate(self, quaternion, IMUposition, IMUvelocity, position, velocity, acceleration, magneticField, gpsAvailable):
        """ if gpsAvailable is True position and velocity measurement is required
            if not measurement-Update can be done only with acceleration and magneticField measurements
            calculating only gyro-error and gyro-bias
            measurement-noise is uncorrelated
            measurement-matrix H is defined at x0
        """
        hn, he, _ = toValue(EARTHMAGFIELD)
        rotationMatrix = quaternion.getRotationMatrix()    
            
        H = np.matrix(zeros(shape=(12,15)))
        subMatrix1 = np.matrix(zeros(shape=(3,3)))
        subMatrix1[0,1] = -g
        subMatrix1[1,0] =  g
        subMatrix2 = np.matrix(zeros(shape=(3,3)))
        subMatrix2[0,2] =  he
        subMatrix2[1,2] = -hn
        H[0:6,0:6] = eye(6,6)
        H[6:9,6:9] = -rotationMatrix.T * subMatrix1
        H[9:12,6:9] = rotationMatrix.T * subMatrix2
        
        S = H*self.P*H.T+self.R 
        K = self.P*H.T*S.I
        
        if not gpsAvailable: 
            K = self.setGainToZero(K)
        
        dz = self.getMeasurementVector(IMUposition, IMUvelocity, rotationMatrix, position, velocity, acceleration, magneticField)
        state = vstack((self.posError, self.velError, self.oriError, self.accError, self.gyrError))
        innov = dz - H*state
        newState = state+K*innov
        self.posError = newState[0:3]
        self.velError = newState[3:6]
        self.oriError = newState[6:9]
        self.accError = newState[9:12]
        self.gyrError = newState[12:15]
        
        self.P = self.P - K*H*self.P 
    
    def getMeasurementVector(self, IMUpos, IMUvel, rotMatrix, pos, vel, accel, mag):
        """ calculates difference between measured values and calculated values
            ellipsoidal distance has to be transformed into (N,E,D) with metric units
        """ 
        z0 = vstack((IMUpos.values,IMUvel.values,rotMatrix.T*-G,rotMatrix.T*EARTHMAGFIELD))
        dz = vstack((pos,vel,accel,mag)) - z0
        lat,_,h = toValue(IMUpos.values)
        Rn, Re = earthCurvature(IMUpos.a,IMUpos.f,lat)
        dz[0] = dz[0]*(Rn-h)
        dz[1] = dz[1]*(Re-h)*cos(lat)
        return dz
        
    def setGainToZero(self, K):
        """ set lines and columns concerning position, velocity and accel-bias to zero
            no influence on estimation
        """
        K[:,0:6] = 0.
        K[9:12,:] = 0.
        K[:,9:12] = 0.
        K[0:6,:] = 0.
        return K
    
    def resetState(self):
        """ resets system state to zero after compensation of absolut values outside of this class
        """
        self.posError = toVector(0.,0.,0.)
        self.velError = toVector(0.,0.,0.)
        self.oriError = toVector(0.,0.,0.)
        self.accError = toVector(0.,0.,0.)
        self.gyrError = toVector(0.,0.,0.)

def getVKMatrix(rms):
    """ rms is a list of rms values
        returns an array with n x n, where n is the length of rms
    """
    nn = power(rms,2)
    return np.matrix(diag(nn))
    
def main():
    print(getVKMatrix([1]*3+[0.5]*3))
    K = KalmanPVO()
    print(K.Q)
    q = Quaternion()
    K.timeUpdate(toVector(0.1, 0.2, 9.81), q, 0.01)
    print(K.P)
    
if __name__ == "__main__":
    main() 