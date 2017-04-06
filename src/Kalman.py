from numpy import zeros, eye, vstack, power, diag
from MathLib import toVector
from Settings import DT, g
class Kalman(object):
    
    def __init__(self):
        self.bearingError = toVector(0.,0.,0.) #stateElements
        self.gyroBias = toVector(0.,0.,0.)
        
        self.gyroNoise = toVector(0.0003,0.0003,0.0003) #SensorNoise/systemNoise
        self.gyroBiasNoise = toVector(0.0001,0.0001,0.0001) #RandomWalk
        
        self.accelNoise = toVector(0.0003,0.0003,0.0003) #SensorNoise/MeasurementNoise
        self.magnetoNoise = toVector(0.0002,0.0002,0.0002)
        
        self.P = eye(6, 6)*10000000000
        
    def timeUpdate(self,quaternion):
        rotationMatrix = quaternion.getRotationMatrix()
        F = zeros(shape=(6,6))
        F[0:3,3:6] = rotationMatrix # Jacobi-Matrix
        #print("F = \n", F)
        
        G = zeros(shape =(6,6))
        G[0:3,0:3] = rotationMatrix # derivation at point x0(current bearing)
        G[3:6,3:6] = eye(3,3)
        #print("G = \n", G)
        
        state = vstack((self.bearingError, self.gyroBias))
        noise = vstack((self.gyroNoise, self.gyroBiasNoise))
        
        newState = F*state #+G*noise
        print("Zustandsvektor a priori = :\n",newState)
        self.bearingError = newState[0:3]
        self.gyroBias = newState[3:6]
        
        qq = power(noise,2)
        Q = diag(qq.A[:,0]) #uncorrelated 
        
        f = eye(6, 6)+F*DT # Transitionmatrix f = integral(F)
        self.P = f*self.P*f.transpose() + G*Q*G.transpose()
        print("VKV-Matrix a priori = :\n", self.P)
        
    def measurementUpdate(self, acceleration, magneticField, quaternion):
        rotationMatrix = quaternion.getRotationMatrix()
        H1 = zeros(shape =(3,6))
        H1[0,1] =-g
        H1[1,0] = g
        H1 = -rotationMatrix.transpose()*H1
        
        H2 = zeros(shape=(3,6))
        H2[0,2] = 1
        H2[1,2] =-1
        H2 = rotationMatrix.transpose()*H2
        H = vstack((H1,H2))

        print("Messmatrix H =:\n",H)
        noise = vstack((self.accelNoise, self.magnetoNoise))
        rr = power(noise,2)
        R = diag(rr.A[:,0])
        #print("R =:\n", R)
        S = H*self.P*H.transpose()+R
        print("S =:\n", S)
        K = self.P*H.transpose()*S.I
        print("K =:\n", K)
        self.P = self.P - K*H*self.P
        print("VKV-Matrix a posteriori =:\n",self.P)
        
        bearing = quaternion.getEulerAngles() 
        z0 = H[:,0:3]*bearing # h0(x0, r = 0)
        print("z0 =:\n",z0)
        dz = vstack((acceleration,magneticField)) - z0
        print("dz =:\n",dz)
        oldState = vstack((self.bearingError, self.gyroBias))
        innov = dz - H*oldState
        print("innovation = :\n", innov)
        newState = oldState+K*innov
        print("Zustandsvektor a posteriori = :\n", newState)
        