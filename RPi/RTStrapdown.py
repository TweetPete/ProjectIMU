import sys, getopt
from datetime import datetime
from Strapdown import Strapdown
from LowPassFilter import LowPassFilter
from MathLib import toVector, toValue, runningAverage
from Settings import g
from numpy import rad2deg
from Kalman import Kalman
from Quaternion import Quaternion

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
    print("Settings file does not exist, will be created")

se = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(se)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = 10.0 #imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

print("Initializing ...\n")

s = Strapdown()
K = Kalman()
rot_mean = toVector(0.,0.,0.)
acc_mean = toVector(0.,0.,0.)
mag_mean = toVector(0.,0.,0.)
gyroBias = toVector(0.,0.,0.)
dt_mean = 0.

i = 1

while True:
    if imu.IMURead():
        start = datetime.now()
        data = imu.getIMUData()
        gyro = data["gyro"]
        gyro_v = toVector(gyro[0],gyro[1],gyro[2])-gyroBias
        accel = data["accel"]   
        accel_v = toVector(accel[0],accel[1],accel[2])*-9.80665 
        mag = data["compass"]
        mag_v = toVector(mag[0],mag[1],mag[2])
    
        if not s.isInitialized:
            rot_mean = runningAverage(rot_mean, gyro_v, 1/i)
            acc_mean = runningAverage(acc_mean, accel_v, 1/i)
            mag_mean = runningAverage(mag_mean, mag_v, 1/i)
            if i*poll_interval/1000 >= 10 :
                s.Initialze(acc_mean, mag_mean)
                gyroBias = rot_mean
            
                print('STRAPDOWN INITIALIZED with %i values\n' % (i,))    
                print('Initial bearing\n', s.getOrientation())
                print('Initial velocity\n', s.getVelocity())
                print('Initial position\n', s.getPosition())
                print('Initial gyro Bias\n', gyroBias)
        else:
            s.quaternion.update(gyro_v)
            s.velocity.update(accel_v, s.quaternion)
            s.position.update(s.velocity)
            phi, theta, psi = toValue(rad2deg(s.getOrientation()))
            
            K.timeUpdate(s.quaternion)
            if i%10 == 0:
                K.measurementUpdate(accel_v, mag_v, s.quaternion)             
                errorQuat = Quaternion(K.bearingError)
                s.quaternion *= errorQuat
                gyroBias += K.gyroBias 
                K.resetState()
            
            if i%50 == 0: #print area
                print('Roll: %9.3f, Pitch: %9.3f, Yaw: %9.3f' % (phi, theta, psi))
                print('dt_mean: %f' % dt_mean)
                #vx, vy, vz = toValue(s.getVelocity())
                #print('vx: %.2f, vy: %.2f, vz: %.2f' % (vx,vy,vz))
                
        end = datetime.now()
        diff = end-start
        #print(diff.total_seconds())
        if (poll_interval*1./1000.)>diff.total_seconds():
            time.sleep(poll_interval/1000 - diff.total_seconds())
        end2 = datetime.now()
        diff_dt = end2 - start
        dt_mean = runningAverage(dt_mean, diff_dt.total_seconds(), 1/i) 
        i += 1