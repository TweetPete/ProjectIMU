from Quaternion import Quaternion
from numpy import matrix, rad2deg, deg2rad
from Strapdown import Strapdown
import math 
from MathLib import toValue, toVector
from Bearing import Bearing
from Velocity import Velocity

phi = 1
theta = 1 
psi = 0

wx = 0.001
wy = 0.001
wz = 0

print("Ausgangslage = ", phi, theta, psi)
q = Quaternion(toVector(phi, theta, psi))
# print("zweites Quaternionenelement ", q.q0)
print("R\n" ,q.getRotationMatrix())
print("Drehrate = ", wx, wy, wz)
q.update(matrix([wx,wy,wz]))
# print("geupdatetes Quaternion ", q.q0)

s = Strapdown()
b = Bearing()
# print(b.bearing, s.velocity)
b.initBearing(matrix([0.1,0.2,10.0]), matrix([100,200,5]))
print(b.bearing)

print("Eulerwinkel aus Quaternion", q.getEulerAngles()) #Test Euler --> Quat --> update --> Euler ?
neu = b.update(toVector(wx,wy,wz))
print("Eulerwinkelaendeurng aus Eulerwinkeln", neu)

a,b,c = toValue(matrix([3,2,1]))
print(a,b,c)
vector = toVector(a,b,c)
print(vector)

acc = matrix([3,0.1,2])
vel = Velocity()
print(vel.velocity)
vel.update(acc, q)
print(vel.velocity)
