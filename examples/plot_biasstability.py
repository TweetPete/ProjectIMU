import matplotlib.pyplot as plt
from array import array

bx = [0.953018, 0.965222, 0.973485, 0.956202, 0.954734, 0.934733]
by = [-0.836894, -0.845056, -0.852844, -0.849721, -0.853087, -0.848449]
bz = [0.161931, 0.155903, 0.149976, 0.144025, 0.137360, 0.133043]

plt.subplot(311)
plt.plot(bx, 'r-')
plt.title('Zeitlicher Verlauf des Drehratenbias in deg/s')
plt.ylabel('X-Achse')
plt.subplot(312)
plt.plot(by, 'g-')
plt.ylabel('Y-Achse')
plt.subplot(313)
plt.plot(bz, 'b-')
plt.ylabel('Z-Achse')
plt.xlabel('Intervallnr.')
plt.show()