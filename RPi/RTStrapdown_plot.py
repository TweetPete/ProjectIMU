import sys
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from MathLib import resize, toVector, runningAverage, toValue
from Strapdown import Strapdown
from numpy import rad2deg

sys.path.append('.')
import RTIMU
import os.path
import numpy as np

# IMU INIT

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
        
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
    
poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)
    
# HEADER

phi_list = []
theta_list = []
psi_list = []
i_list = []

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)

ln1, = ax1.plot([], [], 'ro', animated=True)
ln2, = ax2.plot([], [], 'ro', animated=True)
ln3, = ax3.plot([], [], 'ro', animated=True)
ax = [ax1, ax2, ax3]
ln = [ln1, ln2, ln3]

def data_listener():
    s = Strapdown()
    rot_mean = toVector(0.,0.,0.)
    acc_mean = toVector(0.,0.,0.)
    mag_mean = toVector(0.,0.,0.)
    gyroBias = toVector(0.,0.,0.)
    
    i = 0
    init_time = 1/6 #min
    while True:
        if imu.IMURead():
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
                if (i*poll_interval/1000)%60 == 0:
                    print('Initialized in %.1f minutes\n' % (init_time-i*poll_interval/1000./60.,))
                if i*poll_interval/1000 >= init_time :
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
                phi_list.append(phi)
                theta_list.append(theta)
                psi_list.append(psi)
                i += 1
                i_list.append(i)

def init():
    ax.set_xlim(0,3000)
    ax.set_ylim(-4,4)
    return ln,

def init_subplot():
    for axi in ax:
        axi.set_xlim(0,1000)
        axi.set_ylim(-4,4)
    return ln

def animate(k):
    xdata = i_list[-100:]
    ydata = phi_list[-100:]
    if xdata: #move x-axis
        ax.set_xlim(max(xdata)-2500,max(xdata)+500)
    x_arr = np.asarray(xdata)
    y_arr = np.asarray(ydata)
    if x_arr.shape == y_arr.shape:
        ln, = plt.plot(x_arr, y_arr, 'ro')
        return ln,
    else: 
        x_arr, y_arr = resize(x_arr,y_arr)
        ln, = plt.plot(x_arr, y_arr, 'ro')
        return ln,

def animate_subplot(k):
    xdata = i_list[-1000:]
    ydata = [phi_list[-1000:],theta_list[-1000:],psi_list[-1000:]]
    if xdata:
        for axi in ax:
            axi.set_xlim(max(xdata)-1000,max(xdata))
    x_arr = np.asarray(xdata)
    j = 0
    for lni in ln: 
        y_arr = np.asarray(ydata[j])
        if x_arr.shape == y_arr.shape:
            lni.set_data(x_arr, y_arr)
        else: 
            x_arr, y_arr = resize(x_arr,y_arr)
            lni.set_data(x_arr, y_arr)
        j += 1
    return ln

if __name__ == '__main__':
    thread = threading.Thread(target=data_listener)
    thread.daemon = True
    thread.start()
    ani = FuncAnimation(fig, animate_subplot, init_func = init_subplot, blit=True , interval = 10)
    plt.show()
