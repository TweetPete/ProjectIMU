from numpy import deg2rad, rad2deg
from math import sin, cos

Lat = 52.5 #deg
Lat_rad = deg2rad(Lat)

Omega = 7.292115*10**(-5) #rad/s IERS - mittlere Winkelgeschwindigkeit der Erde

#Erddrehrate 
wex = Omega * cos(Lat_rad)
wey = 0
wez = - Omega *sin(Lat_rad)

print("Einfluss der Erddrehrate am 52.5 Breitengrad = ", wex, wey, wez , "rad/s")
print("Einfluss der Erddrehrate am 52.5 Breitengrad = ", rad2deg(wex), wey, rad2deg(wez) , "deg/h")

w_max = rad2deg(Omega)*1
print("Maximaler Drehrate der Erdrotation = ", w_max, "deg/s")