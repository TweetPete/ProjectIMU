import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MathLib import toVector, toValue
from Quaternion import Quaternion
from Euler import Euler
from numpy import deg2rad
from matplotlib.pyplot import xlabel, ylabel

VecStart_x = toVector(0,0,0)
VecStart_y = toVector(0,0,0)
VecStart_z = toVector(0,0,0)
VecEnd_x = toVector(0,1,0)
VecEnd_y = toVector(1,0,0)
VecEnd_z  = toVector(0,0,-1)

e = Euler(VecEnd_z,VecEnd_x)
e.values = toVector(deg2rad(0.),deg2rad(0.),deg2rad(45.))
q = Quaternion(e.values)
q_conj = q.getConjugatedQuaternion()

x = q_conj.vecTransformation(VecEnd_x)
y = q_conj.vecTransformation(VecEnd_y)
z = q_conj.vecTransformation(VecEnd_z)
x1, x2, x3 = toValue(x)
y1, y2, y3 = toValue(y)
z1, z2, z3 = toValue(z)
x_list = [x1,x2,x3]
y_list = [y1,y2,y3]
z_list = [z1,z2,z3]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(3):
    ax.plot([VecStart_x[i], x_list[i]], [VecStart_y[i],y_list[i]],zs=[VecStart_z[i],z_list[i]])

ax.auto_scale_xyz([-1,1],[-1,1],[-1,1])
ax.set_xlabel('East')
ax.set_ylabel('North')
ax.set_zlabel('Down')
plt.show()
# Axes3D.plot()