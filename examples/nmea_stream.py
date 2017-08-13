import pynmea2, time
from MathLib import toVector
from Position import EllipsoidPosition, Position
from GeoLib import ell2xyz
from Velocity import Velocity
from numpy import deg2rad

msg = pynmea2.parse("$GPGGA,132525.000,5233.3292,N,01320.6101,E,2,07,1.38,25.9,M,44.7,M,0000,0000*52")
# msg = pynmea2.parse("GPGSA,A,3,14,12,32,29,24,25,31,,,,,,2.67,1.38,2.29*0D")
print('Time: {:} Lat: {:3.4f} Lon: {:3.4f} H: {:3.4f}'.format(msg.timestamp, msg.latitude,
                                                               msg.longitude, float(msg.altitude) + float(msg.geo_sep)))

p0 = EllipsoidPosition(deg2rad(toVector(msg.latitude,msg.longitude,float(msg.altitude) + float(msg.geo_sep))))
p0 = ell2xyz(p0) #xyz

t0 = msg.timestamp
t0 = (t0.hour*3600 + t0.minute*60 + t0.second - 1)

with open('D:\Masterarbeit\Code\Eclipse\ProjectIMU\data\\UltimateGPS\GPRMC_stream.csv','r') as fread:
    streamreader = pynmea2.NMEAStreamReader(fread, 'ignore')
    while 1:
        for msg in streamreader.next():
            if msg.sentence_type == 'GGA':
                he = float(msg.altitude) + float(msg.geo_sep) #m
                lat = deg2rad(msg.latitude)
                lon = deg2rad(msg.longitude)
                p = EllipsoidPosition(toVector(lat,lon,he))   
                p = ell2xyz(p)
                dp = p - p0
                p0 = p
                t = msg.timestamp
                t = (t.hour*3600 + t.minute*60 + t.second)                    
                dt = (t-t0)
                t0 = t
                v = dp/abs(dt)
                v = Velocity(v)
                p = Position(p)
                print(p, v, msg.timestamp)
            time.sleep(0.1)