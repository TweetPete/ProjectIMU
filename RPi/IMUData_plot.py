import sys
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from MathLib import resize

sys.path.append('.')
import RTIMU
import os.path
import time 
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

wx = []
wy = []
wz = []
acx = []
acy = []
acz = []
mx = []
my = []
mz = []
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
    i = 0
    while True:
        if imu.IMURead():
            time.sleep(0.02)
            data = imu.getIMUData()
            #gyro = data["gyro"]
            #wx.append(gyro[0])
            #wy.append(gyro[1])
            #wz.append(gyro[2])
            accel = data["accel"]
            acx.append(accel[0])
            acy.append(accel[1])
            acz.append(accel[2])
            #compass = data["compass"]
            #mx.append(compass[0])
            #my.append(compass[1])
            #mz.append(compass[2])
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
    ydata = wx[-100:]
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
    ydata = [acx[-1000:],acy[-1000:],acz[-1000:]]
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
