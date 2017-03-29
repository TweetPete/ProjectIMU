from MathLib import toVector, toValue
from math import pi
g = 9.81

ba = toVector(10, 10, 10)  # mg
ba_ms = ba * g / 1000
bx, by, bz = toValue(ba_ms)

s_phi = -bx/g
print("Lagefehler phi = ", s_phi*180/pi, "deg")
s_theta = bz/g 
print("Lagefehler theta = ", s_theta*180/pi, "deg")