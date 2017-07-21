import gpsd, time
from math import cos, sin, pi
from MathLib import toVector

from random import uniform, random

class GNSS(object):
    def __init__(self ):
        self.pos = toVector(0.,0.,0.)
        self.vel = toVector(0.,0.,0.)
        self.error = toVector(0.,0.,0.)
        self.time = time.time()
        self.new = False # True when new measurement was received
        self.connected = False

    def connect(self):
        while not self.connected:
            try: 
                gpsd.connect() # Connect to the local gpsd
                self.connected = True
            except:
                print('Could not connect to gpsd socket')
                time.sleep(5)
    
    def stream(self):
        self.connect()
        while True: 
            try:
                pkt = gpsd.get_current()
                az = pkt.track*pi/180
                vx = pkt.speed()*cos(az)
                vy = pkt.speed()*sin(az)
                self.pos = toVector(pkt.lat*pi/180, pkt.lon*pi/180, pkt.altitude())
                self.vel = toVector(vx, vy, pkt.climb)
                #self.mode = pkt.mode
                self.time = time.time()
                self.new = True # is True when new GPS measurement arrived and has not been used
                if __name__ == '__main__':
                    print("%.1f, %3.7f, %3.7f, %4.1f, %3.3f, %3.3f, %3.3f, %.2f, %.2f, %.2f" %
                           (time.time(), pkt.lat, pkt.lon, pkt.altitude(), vx, vy, pkt.climb, pkt.error['x'], pkt.error['y'], pkt.error['v']))
            except : 
                #raise
                if __name__ == '__main__':
                    print("No 3D fix available")
                else: 
                    pass
            time.sleep(1)

if __name__ == '__main__':
    print("Time[s], Lat[deg], Lon[deg], he[m], vx[ms], vy[ms], vz[ms]")
    data = GNSS()
    data.stream()