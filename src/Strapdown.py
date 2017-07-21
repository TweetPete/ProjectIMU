""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""
from Euler import Euler
from MathLib import toVector, runningAverage, toValue
from Position import Position, EllipsoidPosition
from Quaternion import Quaternion
from Velocity import Velocity, calcVelocity
from Kalman import Kalman, KalmanPVO
from FileManager import CSVImporter, NMEAImporter, export
from PlotHelper import plotVector, plot3DFrame, plot2Dcoordinates, \
    plot3Dcoordinates, plotRGB
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from datetime import datetime 
from numpy import rad2deg, std, diff, insert, deg2rad
from math import sqrt, pi
from GeoLib import ell2xyz
from Settings import G
import simplekml

class Strapdown(object):
    def __init__(self):
        """ creates Strapdown object which includes the current bearing, velocity and position
            bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """             
        self.quaternion = Quaternion()
        self.velocity = Velocity()  # vector (if known)
        self.position = EllipsoidPosition()  # or GNSS.getPos()
        # toVector(52.521918/180*pi, 13.413215\180*pi, 100.)
        self.isInitialized = False
        
    def Initialze(self, acceleration, magneticField, position):
        self.quaternion = Quaternion(Euler(acceleration, magneticField).values)
        self.position.values = position  # if GNSS measurement is icluded  
        self.isInitialized = True        
        
    def getOrientation(self):
        return self.quaternion.getEulerAngles()
    
    def getVelocity(self):
        return self.velocity.values
    
    def getPosition(self):
        return self.position.values
    
    
def main():
    s = Strapdown()
    K = KalmanPVO()
    kml = simplekml.Kml()

    rot_mean = toVector(0.018461137, -0.01460140625, 0.002765854)
    accelBias = toVector(0., 0., 0.)
    acc_mean = toVector(0., 0., 0.)
    mag_mean = toVector(0., 0., 0.)
    pos_mean = s.getPosition()
    dt_mean = 0.01
    
    # read sensors
    filePath = "sample_10minY10min_BW3.csv"
    dIMU = CSVImporter(filePath, columns=range(0, 10), skip_header=7, hasTime=True)
    accelArray, rotationArray, magneticArray = convArray2IMU(dIMU.values)
    tIMU, deltaArray = convArray2time(dIMU.values)

    dGPS = CSVImporter("data\\UltimateGPS\\linie_dach_gps.csv", skip_header=1, columns=range(7))
    posArray, velArray = convArray2PV(dGPS.values)
    tGPS, _ = convArray2time(dGPS.values)
    # realtime 3D plot
#     fig = plt.figure()
#     axes = fig.add_subplot(111, projection='3d')
#     plt.ion()
    
    start = datetime.now()
    x_list = []
    y_list = []
    z_list = []
    vx_list = []
    vy_list = []
    vz_list = []
    phi_list = []
    theta_list = []
    psi_list = []
    wx_list = []
    wy_list = []
    wz_list = []
    ax_list = []
    ay_list = []
    az_list = []
    
    j = 1
    for i in range(121600,dIMU.length):
        dt_mean = runningAverage(dt_mean, deltaArray[i], 0.7)
        # for 10 - 15 minutes
        if not s.isInitialized:
            rot_mean = runningAverage(rot_mean, rotationArray[:, i], 1 / (i + 1))
            acc_mean = runningAverage(acc_mean, accelArray[:, i], 1 / i)
            mag_mean = runningAverage(mag_mean, magneticArray[:, i], 1 / i)
#             if tIMU[i] >= tGPS[j]:
#                 pos_mean = runningAverage(pos_mean, posArray[:,j] , 1/j)
#                 j += 1
            if i >= dIMU.length-1:#if tIMU[i]-tIMU[0] >= 10*60: # for 10 - 15 minutes    
                s.Initialze(acc_mean, mag_mean, pos_mean)
                gyroBias = rot_mean 
                accelBias = s.quaternion.vecTransformation(acc_mean)+G
        
                print('STRAPDOWN INITIALIZED with %i samples and %i position measurements\n' % (i, j))   
                e = Euler() 
                e.values = s.getOrientation()
                print('Initial bearing\n', e)
                print('Initial velocity\n', s.velocity)
                print('Initial position\n ', s.position)
                print('Initial gyro Bias\n', gyroBias)
                print('Initial accel Bias\n', accelBias)
        else:
            if i % 100 == 0:  # plot area
                euler = rad2deg(s.getOrientation())
                plt.figure(1)
                plotRGB(i*0.0134, euler)
#                 plt.figure(2)
#                 plotVector(i,gyroBias)
#                 plt.cla()
#                 fig.texts = []
#                 plot3DFrame(s,axes)
#                 plt.draw()
#                 plt.pause(0.01)

            phi, theta, psi = rad2deg(s.getOrientation()) 
            phi_list.append(phi)
            theta_list.append(theta)
            if psi <= 0:
                psi = 360. + psi
            psi_list.append(psi)
             
            x,y,z = toValue(s.position.values)
            x_list.append((x))
            y_list.append((y))
            z_list.append(z)
             
#             if i%25 == 0: kml.newpoint(name=str(i), coords=[(rad2deg(y),rad2deg(x),z)])
 
            vx, vy, vz = toValue(s.velocity.values)
            vx_list.append(vx)
            vy_list.append(vy)
            vz_list.append(vz)
             
#             wx, wy, wz = rad2deg(toValue(gyroBias))
#             wx_list.append(wx)
#             wy_list.append(wy)
#             wz_list.append(wz)
#              
#             ax, ay, az = toValue(accelBias)
#             ax_list.append(ax)
#             ay_list.append(ay)
#             az_list.append(az)
               
            acceleration = accelArray[:, i] - accelBias
            rotationRate = rotationArray[:, i] - gyroBias
            magneticField = magneticArray[:, i]
            
            s.quaternion.update(rotationRate, dt_mean)
            s.velocity.update(acceleration, s.quaternion, dt_mean)
            s.position.update(s.velocity, dt_mean)
            
            K.timeUpdate(acceleration, s.quaternion, dt_mean)

#             try: 
#                 gpsAvailable = tIMU[i] >= tGPS[j]
#             except:
#                 gpsAvailable = False
#                          
#             if gpsAvailable or i % 10 == 0:
#                 if gpsAvailable:
#                     pos = posArray[:, j]
#                     vel = velArray[:, j]
#                     j += 1
#                     if True : #55450 <= i <= 56450: # simulated no GPS 
#                         gpsAvailable = False
#                         pos = toVector(0., 0., 0.)
#                         vel = toVector(0., 0., 0.)
#                 else:
#                     pos = toVector(0., 0., 0.)
#                     vel = toVector(0., 0., 0.)
# #                 K.measurementUpdate(s.quaternion, s.position, s.velocity, pos, vel, acceleration, magneticField, gpsAvailable)
#                 K.measurementUpdate(s.quaternion, EllipsoidPosition(), s.velocity, pos, vel, acceleration, magneticField, gpsAvailable)
#                 errorQuat = Quaternion(K.oriError)
#                 s.quaternion = errorQuat * s.quaternion
# #                 s.position.correct(K.posError)
#                 s.velocity.correct(K.velError)  
#                 gyroBias = gyroBias + K.gyrError
#                 accelBias = accelBias + K.accError
#                 K.resetState()                    
                
    print("Differenz zwischen x Bias End-Start: %E" % rad2deg(gyroBias[0] - rot_mean[0]))  
    print("Differenz zwischen y Bias End-Start: %E" % rad2deg(gyroBias[1] - rot_mean[1]))
    print("Differenz zwischen z Bias End-Start: %E\n" % rad2deg(gyroBias[2] - rot_mean[2]))      
#     print("RMS_dphi = %f deg" % rad2deg(sqrt(K.P[6,6])))
#     print("RMS_dthe = %f deg" % rad2deg(sqrt(K.P[7,7])))
#     print("RMS_dpsi = %f deg" % rad2deg(sqrt(K.P[8,8])))
    # print("RMS_x = %f m" % (sqrt(K.P[0,0])))
    # print("RMS_y = %f m" % (sqrt(K.P[1,1])))
    # print("RMS_z = %f m\n" % (sqrt(K.P[2,2])))
    e.values = s.getOrientation()
    print('final orientation\n', e)
    print('final position\n', s.position)
    end = datetime.now()
    diff = end - start
    print('Time needed = ', diff.total_seconds())
    
    print(std(x_list),max(x_list).item(), min(x_list).item())
    print(std(y_list),max(y_list).item(), min(y_list).item())
    print(std(z_list),max(z_list).item(), min(z_list).item())
     
    print(std(vx_list),max(vx_list).item(), min(vx_list).item())
    print(std(vy_list),max(vy_list).item(), min(vy_list).item())
    print(std(vz_list),max(vz_list).item(), min(vz_list).item())
     
#     print(std(phi_list), max(phi_list).item(), min(phi_list).item())
#     print(std(theta_list), max(theta_list).item(), min(theta_list).item())
#     print(std(psi_list), max(psi_list).item(), min(psi_list).item())
#      
#     print(std(ax_list),max(ax_list).item(), min(ax_list).item())
#     print(std(ay_list),max(ay_list).item(), min(ay_list).item())
#     print(std(az_list),max(az_list).item(), min(az_list).item())
#      
#     print(std(wx_list),max(wx_list).item(), min(wx_list).item())
#     print(std(wy_list),max(wy_list).item(), min(wy_list).item())
#     print(std(wz_list),max(wz_list).item(), min(wz_list).item())
    
    print("mittlere Abtastrate: {:3.12f}".format(dt_mean))
    kml.save("linie_track_v3.kml")
    plt.show()
    
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

def convArray2IMU(array):  # arduino 10DOF
    acceleration = toVector(array[:, 4], array[:, 5], array[:, 6]) * -9.80665
    rotationRate = toVector(array[:, 1], array[:, 2], array[:, 3])  # *pi/180
    magneticField = toVector(array[:, 7], array[:, 8], array[:, 9]) * 1
    return acceleration.T, rotationRate.T, magneticField.T

def convArray2time(array):
    t = array[:, 0]
    delta = diff(t)
    delta = insert(delta, 0, delta[0])
    return t.T, delta.T

def convArray2PV(array):
    pos = toVector(deg2rad(array[:, 1]), deg2rad(array[:, 2]), array[:, 3])  # rad rad m
    vel = toVector(array[:, 4], array[:, 6], array[:, 6])  # ms
    return pos.T, vel.T
    
if __name__ == "__main__":
    main()         
        

    
        
