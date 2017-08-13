from MathLib import toVector, toValue
from math import pi, sin, cos
import matplotlib.pyplot as plt
from matplotlib.pyplot import title, xlabel, ylabel

g = 9.81
phi = 0 * pi / 180
theta = 1 * pi / 180
psi = 0 * pi / 180

# bw = toVector((theta), -(phi), 0)  # 5degree/s
bw = toVector(sin(phi) * sin(psi) + cos(phi) * sin(theta) * cos(psi),
            - sin(phi) * cos(psi) + cos(phi) * sin(theta) * sin(psi) ,
            1 - cos(phi) * cos(theta))

ba = toVector(10, 10, 10)  # mg
ba_ms = ba * g / 1000

for t in range(60):

    dr1 = (1 / 6) * g * (bw) * t ** 3
    
    dr2 = (1 / 2) * ba_ms * t ** 2
    
    x, y, z = toValue(dr1)
    
    red_dot, = plt.plot(t, x, "ro")
    blue_dot, = plt.plot(t, y, "bo")
    green_dot, = plt.plot(t, z, "go")


plt.legend([red_dot, blue_dot, green_dot], ["X-Pos", "Y-Pos", "Z-Pos"])
title('Positionsfehler durch Drehratenbias')

xlabel('Zeit in [sek]')
ylabel('Positionsfehler in [m]')
plt.show()

