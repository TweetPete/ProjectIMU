import sys, getopt
from datetime import datetime
from Strapdown import Strapdown
from MathLib import toVector, toValue, runningAverage
from numpy import rad2deg
from Kalman import KalmanPVO
from Quaternion import Quaternion
from Position import EllipsoidPosition
from Euler import Euler

sys.path.append('.')
import RTIMU, os.path, threading, NMEA_stream, math

SETTINGS_FILE = "RTIMULib_peter"

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

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
print("Recommended Poll Interval: %dmS\n" % imu.IMUGetPollInterval())

SatObs = NMEA_stream.GNSS()
thread = threading.Thread(target=SatObs.stream)
thread.daemon = True
thread.start()
print("Started GPS stream in a new thread")

print("Initializing ...\n")
s = Strapdown()
K = KalmanPVO()
rot_mean = toVector(0.018461137,-0.01460140625,0.002765854)
accelBias = toVector(0., 0., 0.)
acc_mean = toVector(0.,0.,0.)
mag_mean = toVector(0.,0.,0.)
gyroBias = toVector(0.,0.,0.)
pos_mean = s.getPosition()
dt_mean = 0.01
t_old = 0.

i = 1
j = 1
init_time = 600 # seconds

total_field = 49.5898 # magnitude of magnetic flux

while True:
    if imu.IMURead():
        start = datetime.now()
        data = imu.getIMUData()
        gyro = data["gyro"]
        gyro_v = toVector(gyro[0],gyro[1],gyro[2])-gyroBias
        accel = data["accel"]   
        accel_v = toVector(accel[0],accel[1],accel[2])*-9.80665 -accelBias
        mag = data["compass"]
        c_norm = math.sqrt(mag[0]**2+mag[1]**2+mag[2]**2)
        mag_v = toVector(total_field*(mag[1]/c_norm),total_field*(mag[0]/c_norm),total_field*(mag[2]/c_norm))
        t = data["timestamp"]/1e6
        delta = t - t_old
        t_old = t
      
        if not s.isInitialized:
            rot_mean = runningAverage(rot_mean, gyro_v, 1/i)
            acc_mean = runningAverage(acc_mean, accel_v, 1/i)
            mag_mean = runningAverage(mag_mean, mag_v, 1/i)
            if SatObs.new:
                pos_mean = runningAverage(pos_mean, SatObs.pos, 1/j)
                SatObs.new = False
                j += 1 
            if i*dt_mean >= init_time :
                s.Initialze(acc_mean, mag_mean, pos_mean)
                gyroBias = rot_mean
            
                print('STRAPDOWN INITIALIZED with %i samples and %i position measurements\n' % (i, j))   
                e = Euler() 
                e.values = s.getOrientation()
                print('Initial bearing\n', e)
                print('Initial velocity\n', s.velocity)
                print('Initial position\n ', s.position)
                print('Initial gyro Bias\n', gyroBias)
        else:
            s.quaternion.update(gyro_v, dt_mean)
            s.velocity.update(accel_v, s.quaternion, dt_mean)
            s.position.update(s.velocity, dt_mean)
            
            K.timeUpdate(accel_v, s.quaternion, dt_mean)
            if (SatObs.new and SatObs.sats >= 6) or i%10 == 0: 
                K.measurementUpdate(s.quaternion, s.position, s.velocity, SatObs.pos, SatObs.vel, accel_v, mag_v, SatObs.new)
                errorQuat = Quaternion(K.oriError)
                s.quaternion = errorQuat * s.quaternion
                s.position.correct(K.posError)
                s.velocity.correct(K.velError)  
                gyroBias = gyroBias + K.gyrError
                accelBias = accelBias - K.accError
                K.resetState()  
                SatObs.new = False
            
            ##################################################### print area
            if i%50 == 0:
                phi, theta, psi = toValue(rad2deg(s.getOrientation()))
                vx, vy, vz = toValue(s.getVelocity())
                x, y, z = toValue(s.getPosition())
                ex,ey, ez = toValue(SatObs.PDOP)
                time_str = '%.6f, %3.1f' % (t, 1/dt_mean)
                euler_str = '%9.3f, %9.3f, %9.3f' % (phi, theta, psi)
                velo_str = '%2.3f, %2.3f, %2.3f' % ( vx, vy, vz)
                pos_str = '%3.7f, %3.7f, %4.3f' % ( rad2deg(x), rad2deg(y), z)
                sat_str = '%.2f, %.2f, %.2f, %2i' % ( ex,ey,ez,SatObs.sats)
                print(time_str + ', ' + euler_str + ', ' + velo_str + ', ' + pos_str + ', ' +sat_str)
            #####################################################

        if i != 1:
            dt_mean = runningAverage(dt_mean, delta, 1)
        i += 1   
