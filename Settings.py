""" contains common variables used during the Strapdown-algorithm
"""

from MathLib import toVector
from numpy import deg2rad

# http://icgem.gfz-potsdam.de/calc?modeltype=longtime&modelid=7fd8fe44aa1518cd79ca84300aef4b41ddb2364aef9e82b7cdaabdb60a9053f1
g = 9.80665-0.042#9.81267447770499275

G = toVector(0, 0, g)  # m/s2

# https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
#Lat 52.52, Lon 13.40, date 2017-04-13
EARTHMAGFIELD = toVector(18636.7, 1197.4 ,45940.6)/1000#WMM # Declination = 3° 40' 34"
DECANGLE = deg2rad(3. + 40./60. + 34./3600.)