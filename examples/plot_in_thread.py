import matplotlib.pyplot as plt
import time
import threading
from matplotlib.animation import FuncAnimation
from FileManager import FileManager
from MathLib import toVector, runningAverage
from Strapdown import Strapdown, convArray2IMU
from math import pi
from numpy import rad2deg

data1 = []
data2 = []
s = Strapdown()
phi_list = []
theta_list = []
psi_list = []
i_list = []
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro', animated=True)

# This just simulates reading from a socket.
def data_listener():
#      read sensors
#     filePath = "data\\arduino10DOF\Tilt180_w100Hz.csv"
#     d = FileManager(filePath, columns=range(0,10), skip_header = 7, hasTime = False)
#     _, rotationArray, _ = s.convArray2IMU(d.values)
#     for i in range(d.length):
#         wx = rotationArray[0,i]
#         time.sleep(0.01)
#         data1.append(wx)
#         data2.append(i)
    rot_mean = toVector(0.,0.,0.)
    acc_mean = toVector(0.,0.,0.)
    mag_mean = toVector(0.,0.,0.)
    
    # read sensors
    filePath = "data\\arduino10DOF\\10min_calib_360.csv"
    d = FileManager(filePath, columns=range(0,10), skip_header = 7, hasTime = True)
    accelArray, rotationArray, magneticArray = convArray2IMU(d.values)
       

    for i in range(1,int(47999)):   #62247
        #dt = diff[i]
        # for 10 - 15 minutes
        if not s.isInitialized:
            rot_mean = runningAverage(rot_mean, rotationArray[:,i], 1/i)
            acc_mean = runningAverage(acc_mean, accelArray[:,i], 1/i)
            mag_mean = runningAverage(mag_mean, magneticArray[:,i], 1/i)
            if i >= 45500:#100*60*7.5 :    
                s.Initialze(acc_mean, mag_mean)
                gyroBias = rot_mean#toVector(0.019686476,-0.014544547,0.002910090)
        
                print('STRAPDOWN INITIALIZED with %i values\n' % (i,))    
                print('Initial bearing\n', s.getOrientation()*180/pi)
                print('Initial velocity\n', s.getVelocity())
                print('Initial position\n', s.getPosition())
                print('Initial gyro Bias\n', gyroBias*180/pi)
        else:
            time.sleep(0.01)

            phi,theta,psi = rad2deg(s.getOrientation()) 
            phi_list.append(phi)
            theta_list.append(theta)
            psi_list.append(psi)
            i_list.append(i)   
            
            acceleration = accelArray[:,i]
            rotationRate = rotationArray[:,i]-gyroBias
            magneticField = magneticArray[:,i]
            
            s.quaternion.update(rotationRate)
            s.velocity.update(acceleration, s.quaternion)
            s.position.update(s.velocity)
                
def init():
    ax.set_xlim(45500,47999)
    ax.set_ylim(-190,190)
    return ln,

def animate(i):
    ln.set_data(i_list, phi_list)#, zs = [0,zb[i]])
        
    
#     vx, vy, vz = s.getVelocity()
#     px, py, pz = s.getPosition()
#     s1 = ' Roll: %.4f\n Pitch: %.4f\n Yaw: %.4f\n\n' % (rad2deg(phi),rad2deg(theta),rad2deg(psi))
#     s2 = ' vx: %.2f\n vy: %.2f\n vz: %.2f\n\n' % (vx, vy, vz)
#     s3 = ' px: %.2f\n py: %.2f\n pz: %.2f\n' % (px,py,pz)
#     plt.figtext(0, 0, s1+s2+s3)

#     ln.set_data(data2, data1)
#     if data2:
#         ax.set_xlim(max(data2)-1000,max(data2))
    return ln,

if __name__ == '__main__':
    thread = threading.Thread(target=data_listener)
    thread.daemon = True
    thread.start()
    
    ani = FuncAnimation(fig, animate, init_func = init, blit=True, interval = 100)
    plt.show()