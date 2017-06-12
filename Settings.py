""" contains common variables used during the Strapdown-algorithm
"""

from MathLib import toVector
from numpy import deg2rad

g = 9.81
#DT = 60.105/30190 # 512Hz
#DT = 0.020141559139755304 #50Hz 
#DT = 1/256
#DT = 1 / 400  # sek
#DT = 10/1000
#DT = 0.0134981505504 #mean value from file 
DT = 0.013498005407441232

G = toVector(0, 0, g)  # m/s2

# https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
#EARTHMAGFIELD = toVector(1221.9, 18656.6, 45964.5)/1000 #muT IGRF Lat 52.52, Lon 13.40, date 2017-04-13 # Declination = 3° 43' 56"
EARTHMAGFIELD = toVector(18636.7, 1197.4 ,45940.6)/1000#WMM # Declination = 3° 40' 34"
DECANGLE = deg2rad(3. + 40./60. + 34./3600.)