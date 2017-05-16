import matplotlib.pyplot as plt
from MathLib import toVector, toValue

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
        
def main():
    vec = toVector(1.,2.,0.)
    plotVector(1,vec)
    plt.show()
    
if __name__ == "__main__":
    main()