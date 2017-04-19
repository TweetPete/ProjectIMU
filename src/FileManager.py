from numpy import loadtxt
from os.path import dirname, join, abspath
from os import getcwd

class FileManager(object):
    def readFile(self,fileStr):
        projectPath = dirname(abspath(getcwd()))
        filePath = join(projectPath,fileStr)
        #filepath = r"C:\Users\Martin Zobel\Documents\Masterarbeit\Code\Eclipse\ProjectIMU\data\Sample9DoF_R_Session1_Shimmer_B663_Calibrated_SD.csv"
        return loadtxt(filePath, skiprows=3, delimiter = "\t", usecols = (1,2,3, 7,8,9, 10,11,12))
        
def main():
    testdata = FileManager()
    fileStr = "data\Sample9DoF_R_Session1_Shimmer_B663_Calibrated_SD.csv"
    testarray = testdata.readFile(fileStr)
    print(testarray[1,:])
    
if __name__ == "__main__":
    main() 