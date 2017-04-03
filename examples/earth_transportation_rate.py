from MathLib import pythagoras
from numpy import deg2rad, rad2deg
from GeoLib import earthCurvature
from math import tan
ve = 100 #km/h
vn = 100 #km/h^
v = pythagoras(ve,vn)
print("Mittlere Geschwindigkeit = ", v , "km/h")
ve *= 1000/3600
vn *= 1000/3600

Lat = 52.5 #deg
Lat_rad = deg2rad(Lat)
a = 6378137.0 #WGS84
f = 1./298.257223563
Rn, Re = earthCurvature(a,f,Lat_rad)
h = -30 #m

wtx = ve/(Re-h)
wty = -vn/(Rn-h)
wtz = (ve*tan(Lat_rad))/(Re-h)
print("Einfluss der Transportrate = ", wtx, wty, wtz, "rad/s")
print("Einfluss der Transportrate = ", rad2deg(wtx)*3600, rad2deg(wty)*3600, rad2deg(wtz)*3600, "deg/h")