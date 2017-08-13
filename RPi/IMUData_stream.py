import sys, getopt
from datetime import datetime

sys.path.append('.')
import RTIMU
import os.path
import math

SETTINGS_FILE = "RTIMULib_peter"

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

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

total_field = 49.5898 # magneticField max Value 
print("Time, gyroX, gyroY, gyroZ, accelX, accelY, accelZ, magX, magY, magZ, phi, theta, psi\n")

while True:
    if imu.IMURead():
        start = datetime.now()
        
        data = imu.getIMUData()
        fusionPose = data["fusionPose"]
        gyro = data["gyro"]
        accel = data["accel"]
        compass = data["compass"]
        c_norm = math.sqrt(compass[0]**2+compass[1]**2+compass[2]**2)
        t = data['timestamp']
        euler = data['fusionPose']
        
        print("%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n" %
          (t/1e6, gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2], 
          total_field*(compass[0]/c_norm), total_field*(compass[1]/c_norm),
          total_field*(compass[2]/c_norm), euler[0], euler[1], euler[2]))
