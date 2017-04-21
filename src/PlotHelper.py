import matplotlib.pyplot as plt 

class PlotHelper(object): 
    def __init__(self):
        self.figure = plt.Figure()
        
    def plot(self,x,y,symbol):
        handle, = plt.plot(x,y,symbol) 
        return handle
        
    def subplot(self,x,y,symbol,shape):
        plt.subplot(shape)
        return self.plot(x, y, symbol)
        
    def show(self, xlabel='', ylabel='', title='', handle=(), label=()):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.gcf().legend(handle, label)
        plt.show()
        
def main():
    ph = PlotHelper()
    handle1 = ph.plot((1,2,3), (2,3,2), 'ro')
    handle2 = ph.plot((11,12,13),(12,13,12),'go')
    ph.show(handle= (handle1, handle2), label = ('label1', 'label2'))
    
if __name__ == "__main__":
    main()