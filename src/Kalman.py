""" Kalman Filter using accelerometer and magnetometer measurements to compensate bearing-error und gyro-bias
    closed-loop-Error-state
"""

from numpy import zeros, eye, vstack, power, diag, random, deg2rad
from MathLib import toVector, toValue
from Settings import DT, g, EARTHMAGFIELD, G

class Kalman(object):

    
    def __init__(self):
        """ class contains current state(a priori/a posteriori) 
            and system-noise and measurement-noise
            vcv-matrix P is initialised as not trustworthy 
        """
        self.bearingError = toVector(0.,0.,0.) #stateElements
        self.gyroBias = toVector(0.,0.,0.)
        
        gyroNoise = deg2rad(0.03) #deg2rad(0.005) #SensorNoise/systemNoise
        gyroBiasNoise = deg2rad(0.03)*DT#deg2rad(0.00005) #rad/s #RandomWalk
         
        Q = eye(6,6)
        Q[0,0] = gyroNoise**2
        Q[1,1] = gyroNoise**2
        Q[2,2] = gyroNoise**2
        Q[3,3] = gyroBiasNoise**2/100    
        Q[4,4] = gyroBiasNoise**2/100 
        Q[5,5] = gyroBiasNoise**2/100
        self.Q = Q*DT
        
        accelNoise = 1.20#0.14 #m/s2
        magnetoNoise = 1.0*25#0.22 #muT
        
        R = eye(9,9)
        R[0,0] = accelNoise**2
        R[1,1] = accelNoise**2
        R[2,2] = accelNoise**2
        R[3,3] = accelNoise**2
        R[4,4] = accelNoise**2
        R[5,5] = accelNoise**2
        R[6,6] = magnetoNoise**2
        R[7,7] = magnetoNoise**2
        R[8,8] = magnetoNoise**2
        self.R = R

        #self.P = eye(6, 6)*1e-12
        P = eye(6,6)
        P[0,0] = 0.009821580755979031**2
        P[1,1] = 0.013130360737943313**2
        P[2,2] = 0.009461406104873041**2
        P[3,3] = 0.#0.002913**2
        P[4,4] = 0.#0.002099**2
        P[5,5] = 0.#0.002994**2
        self.P = P
        
    def timeUpdate(self,quaternion):
        """ requires current quaternion to compute linearized system-modell at point x0
            state a priori is propagated w/o noise 
            system-noise is uncorrelated
        """
        rotationMatrix = quaternion.getRotationMatrix()# derivation at point x0(current bearing)
        F = zeros(shape=(6,6))
        F[0:3,3:6] = rotationMatrix # Jacobi-Matrix
        #print("F = \n", F)
        
        # use different variable name 
#         G = zeros(shape =(6,6))
#         G[0:3,0:3] = rotationMatrix 
#         G[3:6,3:6] = eye(3,3)
        #print("G = \n", G)
        
        state = vstack((self.bearingError, self.gyroBias))
        
        # discretisation
        f = eye(6, 6)+F*DT # Transitionmatrix f 
#         g = G*DT
        
        newState = f*state #+G*noise
#        print("Zustandsvektor a priori = :\n",newState)
        self.bearingError = newState[0:3]
        self.gyroBias = newState[3:6]
        
#         Q = self.getNoiseMatrix(self.gyroNoise, self.gyroBiasNoise)

        self.P = f*self.P*f.transpose() + self.Q#g*self.Q*g.transpose()
#         print("VKV-Matrix a priori = :\n", self.P)
        
    def measurementUpdate(self, acceleration, magneticField, quaternion):
        """ acceleration and magneticField-measurements are needed to calculate innovation z
            measurement-noise is uncorrelated
            measurement-matrix H is defined at x0
        """
        rotationMatrix = quaternion.getRotationMatrix()
        H11 = zeros(shape =(3,6))
        H11[0,1] =-g
        H11[1,0] = g
        H22 = zeros(shape =(3,6))
        H22[0,4] = -g*DT*10
        H22[1,3] = g*DT*10
        H11 = -rotationMatrix.transpose()*H11
        H22 = -rotationMatrix.transpose()*H22
        H1 = vstack((H11,H22))
        
        he, hn, _ = toValue(EARTHMAGFIELD)
        
        H2 = zeros(shape=(3,6))
        H2[0,2] = he
        H2[0,5] = he*DT*10
        H2[1,2] =-hn
        H2[1,5] =-hn*DT*10
        H2 = rotationMatrix.transpose()*H2
        H = vstack((H1,H2))
        
        # discretisation
        #H = H*DT
#         print("Messmatrix H =:\n",H) 
        #h = eye(6, 6)+H*DT # Transitionmatrix h = integral(F)
        S = H*self.P*H.transpose()+self.R
#        print("S =:\n", S)
        K = self.P*H.transpose()*S.I
        #K = eye(6,6)*10e-6
        #print("K =:\n", K)
        self.P = self.P - K*H*self.P # maybe use Josephs-Form
#         print("VKV-Matrix a posteriori =:\n",self.P)
        
        #bearing = quaternion.getEulerAngles()
        #x0 = vstack((bearing, toVector(0.,0.,0.))) #gyro bias = 0
        #z0 = vstack((H1*x0,rotationMatrix.transpose()*EARTHMAGFIELD)) # h0(x0, r = 0)
        z0 = vstack((rotationMatrix.transpose()*-G,rotationMatrix.transpose()*-G,rotationMatrix.transpose()*EARTHMAGFIELD))
#         print("z0 =:\n",z0)
        dz = vstack((acceleration,acceleration,magneticField)) - z0
#         print("dz =:\n",dz)
        #print("dz in\% =:\n",dz/z0*100)
        oldState = vstack((self.bearingError, self.gyroBias))
        innov = dz - H*oldState
        #print("innovation = :\n", innov)
        newState = oldState+K*innov
#         print("Zustandsvektor a posteriori = :\n", newState)
        self.bearingError = newState[0:3]
        self.gyroBias = newState[3:6]
        
    def resetState(self):
        self.bearingError = toVector(0.,0.,0.)
        self.gyroBias = toVector(0., 0., 0.)
        
    def getNoiseMatrix(self,rms1, rms2):
        noise1 = random.normal(0,rms1,3)
        noise2 = random.normal(0,rms2,3)
        noise = vstack((noise1.reshape(3,1), noise2.reshape(3,1)))
        nn = power(noise,2)
        return diag(nn[:,0]) #uncorrelated 
        
    