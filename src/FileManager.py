from numpy import genfromtxt
from os.path import dirname, join, abspath
from os import getcwd
from Settings import DT
from math import isclose

class FileManager(object):
    
    def __init__(self, fileStr, delimiter = ',', columns = (0, 2,3,4, 6,7,8, 10,11,12)):
        """ reads txt-file in project directory 
            skips lines with inconsistent columns 
            returns array of values
        """
        projectPath = dirname(abspath(getcwd()))
        filePath = join(projectPath,fileStr)
        
        self.path = filePath
        self.values = genfromtxt(filePath, delimiter = ',', invalid_raise = False, usecols = columns)
        self.sampleRate = self.getSampleRate() 
        self.length = len(self.values)
        if not isclose(self.sampleRate,DT) : 
            raise Warning("Files Sample Rate doesn't fit to Settings Sample Rate", self.sampleRate, DT)
    
    def getSampleRate(self):
        numTime = self.values[:,0]
        timeSpan = numTime[-1]-numTime[0]
        return timeSpan/len(numTime)
        
def main():
    fileStr = "data\mystream_realFrame_fast.csv"
    testdata = FileManager(fileStr)
    print(testdata.values[0])
    print(testdata.path)
    print(testdata.sampleRate)
    print(testdata.length)
    
if __name__ == "__main__":
    main() 