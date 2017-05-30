""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""
from Euler import Euler
from MathLib import toVector, mvMultiplication
from math import pi
from Position import Position
from Quaternion import Quaternion
from Velocity import Velocity
from Kalman import Kalman
from FileManager import FileManager
from PlotHelper import plotVector, plot3DFrame
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Settings import g, DT
from numpy import rad2deg
from LowPassFilter import LowPassFilter

class Strapdown(object):
    def __init__(self):
        """ creates Strapdown object which includes the current bearing, velocity and position
            bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """             
        self.quaternion = Quaternion()
        self.velocity = Velocity()  # vector (if known)
        self.position = Position()  # or GNSS.getPos()
        # toVector(52.521918/180*pi, 13.413215\180*pi, 100.)
        self.isInitialized = False
        
    def Initialze(self, acceleration, magneticField):
        self.quaternion = Quaternion(Euler(acceleration,magneticField).values)
        self.isInitialized = True
        #self.position = (toVector(n,e,d)) if GNSS measurement is icluded 
        
    def getOrientation(self):
        return self.quaternion.getEulerAngles()
    
    def getVelocity(self):
        return self.velocity.values
    
    def getPosition(self):
        return self.position.values
    
def main():
    
    s = Strapdown()
    K = Kalman()
    lp_rot = LowPassFilter()
    lp_acc = LowPassFilter()
    lp_mag = LowPassFilter()
    rot_mean = toVector(0.,0.,0.)
    acc_mean = toVector(0.,0.,0.)
    mag_mean = toVector(0.,0.,0.)
    
    # read sensors
    filePath = "data\\arduino10DOF\\10min_calib_wTilt.csv"
    d = FileManager(filePath, columns=range(0,10), skip_header = 7)
    accelArray, rotationArray, magneticArray = convArray2IMU(d.values)
    
    # realtime 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.ion()
    
    for i in range(1,d.length):   

        # for 10 - 15 minutes
        if not s.isInitialized:
            rot_mean = lp_rot.mean(rot_mean, rotationArray[:,i])
            acc_mean = lp_acc.mean(acc_mean, accelArray[:,i])
            mag_mean = lp_mag.mean(mag_mean, magneticArray[:,i])
            if i >= 100*60*7 :
                s.Initialze(acc_mean, mag_mean)
                gyroBias = rot_mean
        
                print('STRAPDOWN INITIALIZED with %i values\n' % (i,))    
                print('Initial bearing\n', s.getOrientation())
                print('Initial velocity\n', s.getVelocity())
                print('Initial position\n', s.getPosition())
                print('Initial gyro Bias\n', gyroBias)
        else:
                
            if i%20 == 0: # plot area
                #euler = rad2deg(s.getOrientation())
                #plt.figure(1)
                #plotVector(i*DT,euler)
                #plt.figure(2)
                #plotVector(i,gyroBias)
                #print("VK-Matrix der Zustandselemente: \n", K.P) 
                plt.cla()
                fig.texts = []
                plot3DFrame(s.quaternion,ax)
                plt.draw()
                plt.pause(0.05)

                
            acceleration = accelArray[:,i]
            rotationRate = rotationArray[:,i]-gyroBias
            magneticField = magneticArray[:,i]
            
            s.quaternion.update(rotationRate)
            s.velocity.update(acceleration, s.quaternion)
            s.position.update(s.velocity)
                
#             K.timeUpdate(s.quaternion)
#             if i%10 == 0:
#                 K.measurementUpdate(acceleration, magneticField, s.quaternion)
#                          
#                 bearingOld = s.getOrientation()        
#                 errorQuat = Quaternion(K.bearingError)
#                 s.quaternion *= errorQuat
#                 #s.quaternion.update(K.bearingError/DT) #angle = rate*DT
#                 print(s.quaternion.values)
#                 bearingNew = s.getOrientation()
#                 print("Differenz zwischen neuer und alter Lage \n",rad2deg(bearingNew-bearingOld))
#                 gyroBias += K.gyroBias 
#                 K.resetState()
            
    #plt.show()
    print('final orientation\n', s.getOrientation())
    
# def convArray2IMU(array): #MYSTREAM APP
#     acceleration = toVector(array[:,1],array[:,2],array[:,3]+3.05)
#     rotationRate = toVector(array[:,4],array[:,5],array[:,6])*pi/180 
#     magneticField = toVector(array[:,7],-array[:,8],array[:,9])
#     return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()

# def convArray2IMU(array): #ROJEK IMU
#     acceleration = toVector(array[:,3],array[:,4],array[:,5])*-g
#     rotationRate = toVector(array[:,0],array[:,1],array[:,2])*pi/180 
#     magneticField = toVector(array[:,6],array[:,7],array[:,8])*100
#     return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()

def convArray2IMU(array): #arduino 10DOF
    acceleration = toVector(array[:,4],array[:,5],array[:,6])*-g
    rotationRate = toVector(array[:,1],array[:,2],array[:,3])#*pi/180
    magneticField = toVector(array[:,7],array[:,8],array[:,9])*1
    return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()

if __name__ == "__main__":
    main()         
        

    
        
