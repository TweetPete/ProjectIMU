from numpy import loadtxt

class FileManager(object):
    def readFile(self):
        filepath = r"C:\Users\Martin Zobel\Documents\Masterarbeit\Code\Eclipse\ProjectIMU\data\Sample9DoF_R_Session1_Shimmer_B663_Calibrated_SD.csv"
        return loadtxt(filepath, skiprows=3, delimiter = "\t", usecols = (1,2,3, 7,8,9, 10,11,12))
        
def main():
    testdata = FileManager()
    testarray = testdata.readFile()
    print(testarray[1,:])
    
if __name__ == "__main__":
    main() 