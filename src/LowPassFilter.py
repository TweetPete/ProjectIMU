class LowPassFilter(object): 
    def __init__(self):
        self.n = 1
    
    def mean(self, value, new):
        K = 1/self.n
        value += K*(new - value)
        self.n += 1
        return value 