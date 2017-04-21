""" contains common variables used during the Strapdown-algorithm
"""

from MathLib import toVector

g = 9.81
#DT = 60.105/30190 # 512Hz
DT = 0.020141559139755304 #50Hz 
#DT = 1 / 400  # sek
G = toVector(0, 0, g)  # m/s2

# https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
EARTHMAGFIELD = toVector(1221.9, 18656.6, -45964.5)/1000 #muT IGRF Lat 52.52, Lon 13.40, date 2017-04-13 
