from numpy import zeros, eye, vstack
from MathLib import toVector
from Settings import DT
class Kalman(object):
    
    def __init__(self):
        self.bearingError = toVector(0.,0.,0.) #stateElements
        self.gyroBias = toVector(0.,0.,0.)
        
        self.gyroNoise = toVector(0.0003,0.0003,0.0003) #SensorNoise/systemNoise
        self.gyroBiasNoise = toVector(0.0001,0.0001,0.0001) #RandomWalk
        
        self.P = eye(6, 6)*10000000000
        
    def timeUpdate(self,quaternion):
        rotationMatrix = quaternion.getRotationMatrix()
        F = zeros(shape=(6,6))
        F[0:3,3:6] = rotationMatrix
        #print("F = \n", F)
        
        G = zeros(shape =(6,6))
        G[0:3,0:3] = rotationMatrix
        G[3:6,3:6] = eye(3,3)
        #print("G = \n", G)
        
        state = vstack((self.bearingError, self.gyroBias))
        noise = vstack((self.gyroNoise, self.gyroBiasNoise))
        
        newState = F*state+G*noise
        #print(newState)
        self.bearingError = newState[0:3]
        self.gyroBias = newState[3:6]
        
        Q = noise*noise.transpose()
        f = eye(6, 6)+F*DT # Transitionmatrix f = integral(F)
        self.P = f*self.P*f.transpose() + G*Q*G.transpose()
        
    def measurementUpdate(self):
        pass