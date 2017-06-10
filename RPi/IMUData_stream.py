import sys, getopt
from datetime import datetime

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

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

print("Time, gyroX, gyroY, gyroZ, accelX, accelY, accelZ, magX, magY, magZ, phi, theta, psi\n")
while True:
  if imu.IMURead():
    start = datetime.now()
    # x, y, z = imu.getFusionData()
    # print("%f %f %f" % (x,y,z))
    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    gyro = data["gyro"]
    accel = data["accel"]
    compass = data["compass"]
    t = data['timestamp']
    euler = data['fusionPose']
    #d = datetime.now()
    #t = d.hour*3600+d.minute*60+d.second+d.microsecond*1e-6
    print("%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n" %
      (t/1e6, gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2], 
      compass[0], compass[1], compass[2], euler[0], euler[1], euler[2]))
    end = datetime.now()
    diff = end-start
    if (poll_interval*1./1000.)>diff.total_seconds(): 
      time.sleep(poll_interval*1.0/1000.0 - diff.total_seconds()-0.0002)
    
    #end2 = datetime.now()
    #diff2 = end2 - start
    #print("intervall: %f\n" % (diff2.total_seconds(),))	
