import matplotlib.pyplot as plt
from MathLib import toVector, toValue
from mpl_toolkits.mplot3d import Axes3D
from numpy import rad2deg

def plotVector(x, vector):
    if not vector.any(): raise ValueError( "Vector is not valid" )
    y1, y2, y3 = toValue(vector)
    symbol = 'ro'
    plt.subplot(311)
    plt.plot(x,y1,symbol)
    plt.subplot(312)
    plt.plot(x,y2,symbol)
    plt.subplot(313)
    plt.plot(x,y3,symbol)
    
def plot3DFrame(q,ax):
#     c = toVector(0,0,0)
    xn = toVector(0,1,0)
    yn = toVector(1,0,0)
    zn = toVector(0,0,-1)
    
    xb = q.vecTransformation(xn)
    yb = q.vecTransformation(yn)
    zb = q.vecTransformation(zn)
    
    x1, x2, x3 = toValue(xb)
    y1, y2, y3 = toValue(yb)
    z1, z2, z3 = toValue(zb)
    xb = [x1,x2,x3]
    yb = [y1,y2,y3]
    zb = [z1,z2,z3]
    
    for i in range(3):
        ax.plot([0,xb[i]], [0,yb[i]], zs = [0,zb[i]])
        
    ax.auto_scale_xyz([-1,1],[-1,1],[-1,1])
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    ax.set_zlabel('Down')
    
    phi, theta, psi = q.getEulerAngles()
    s = ' Roll: %f\n Pitch: %f\n Yaw: %f' % (rad2deg(phi),rad2deg(theta),rad2deg(psi))
    plt.figtext(0, 0, s)
    
def main():
    vec = toVector(1.,2.,0.)
    plotVector(1,vec)
    plt.show()
    
if __name__ == "__main__":
    main()