from FileManager import CSVImporter
from GeoLib import ell2xyz
from numpy import deg2rad, std
from Position import EllipsoidPosition
from MathLib import toVector

filePath = "data\\UltimateGPS\\20min_sample.csv"
col_pos = range(0,7)
d = CSVImporter(filePath, columns=col_pos, skip_header = 1, hasTime=True)
v = d.values
posArray = v[:,1:4]
velArray = v[:,4:7]

lat_list = []
lon_list = []
h_list = []

for i,position in enumerate(posArray):
    lat, lon = deg2rad(position[0:2])
    h = position[2]
    lat, lon, h = (ell2xyz(EllipsoidPosition(toVector(lat,lon,h))))
    lat_list.append(lat)
    lon_list.append(lon)
    h_list.append(h)
    
print(std(lat_list), std(lon_list), std(h_list))
print(std(velArray[:,0]),std(velArray[:,1]),std(velArray[:,2]))
