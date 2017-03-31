from numpy import cross, matrix, dot
from math import pi, sqrt
from MathLib import pythagoras

#omega = toVector(1.,1.,1.)
#rx = toVector(0.05,0.05,0.05)
omega = matrix([1.,0.,0.])
rx = matrix([5.,0,0])/100.
l = sqrt(25+25+25)

O = matrix([[ 0.,-1., 1.],
            [ 1., 0.,-1.],
            [-1., 1., 0.]])
print(O)
a = O*rx.transpose()
print(a)
b = O*a
print(b)
print(b.transpose()*matrix([1.,1.,1.]).transpose())

az = ((1)**2)*0.05 #m/s2
azg = az*1000/9.80665 #mg
print(az)
print(azg)
t = 1
print("V_Fehler = ", az*t, "m/s")
print("Pos_Fehler = ", 0.5*az*t**2, "m")