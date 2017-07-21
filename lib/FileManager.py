from numpy import genfromtxt, deg2rad, append, diag, std
from os.path import dirname, join, abspath
from os import getcwd
import pynmea2
from Position import EllipsoidPosition
from MathLib import toVector
from GeoLib import ell2xyz
from Kalman import KalmanPVO
from math import sqrt

class CSVImporter(object):
    
    def __init__(self, fileStr, delimiter = ',', columns = (0, 2,3,4, 6,7,8, 10,11,12), hasTime = False, skip_header = 0):
        """ reads txt-file in project directory 
            skips lines with inconsistent columns 
            returns array of values
        """
        projectPath = dirname(abspath(getcwd()))
        filePath = join(projectPath,fileStr)
        
        self.path = filePath
        self.values = genfromtxt(filePath, delimiter = ',', invalid_raise = False,
                                  usecols = columns, skip_header = skip_header)
        if hasTime:
            self.sampleRate = self.getSampleRate() 
        else:
            self.sampleRate = None
        self.length = len(self.values)
    
    def getSampleRate(self):
        numTime = self.values[:,0]
        timeSpan = numTime[-1]-numTime[0]
        return timeSpan/len(numTime)
        
        
class NMEAImporter(object):
    def __init__(self, fileStr):
        """ reads NMEA string and converts them to a List of cartesian Positions and a list of the 
            related time in seconds
            using pynmea2 package
        """
        projectPath = dirname(abspath(getcwd()))
        filePath = join(projectPath,fileStr)
        
        self.path = filePath
        
        self.P = []
        self.t = []
        
        with open(filePath,'r') as fread:
            fileLen = getNumberOfLines(filePath)
            streamreader = pynmea2.NMEAStreamReader(fread, 'ignore')
            for _ in range(fileLen):
                for msg in streamreader.next():
                    if msg.sentence_type == 'GGA':
                        he = float(msg.altitude) + float(msg.geo_sep) #m
                        lat = deg2rad(msg.latitude)
                        lon = deg2rad(msg.longitude)
                        p_geo = EllipsoidPosition(toVector(lat,lon,he))
                        p_cart = ell2xyz(p_geo)
                        t = msg.timestamp #datetime.time()
                        t_sec = (t.hour*3600 + t.minute*60 + t.second)                    
                        self.P.append(p_cart)
                        self.t.append(t_sec)
                        
        self.length = len(self.t)
        self.sampleRate = (self.t[-1]-self.t[0])/self.length
        
def getNumberOfLines(fname):
    return sum(1 for line in open(fname))

def export(fileStr, sampleName, K, phi_list, theta_list):
    projectPath = dirname(abspath(getcwd()))
    filePath = join(projectPath,fileStr)
    with open(filePath, 'w') as file: 
        file.write('Samplefile used: ' + sampleName + '\n')
        file.write('\n Analyse der Lage: \n' )
        file.write('Phi: RMS ' + str(std(phi_list)) + '\t MAX ' + str(max(phi_list)) + '\t MIN ' + str(min(phi_list)) + ' deg \n')
        file.write('Theta: RMS ' + str(std(theta_list)) + '\t MAX ' + str(max(theta_list)) + '\t MIN ' + str(min(theta_list)) + ' deg \n')

        file.write('\n VKM des Systemrauschens: \n')
        file.write(str(K.Q))
        file.write('\n VKM des Messrauschen: \n')
        file.write(str(K.R))
    
def main():
    K = KalmanPVO()
    phi_list = [0,1,2,3,2,5,6,7]
    theta_list = [0,1,2,3,2,5,6,7]
    fileStr = "data\\test_NMEA_output.csv"
    export('root_test.txt', fileStr, K, phi_list, theta_list)   
    

if __name__ == "__main__":
    main() 