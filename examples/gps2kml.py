import simplekml
from FileManager import CSVImporter

kml = simplekml.Kml()

filePath = "data\\UltimateGPS\\linie_dach_gps.csv"
col_pos = range(0,7)
d = CSVImporter(filePath, columns=col_pos, skip_header = 1, hasTime=True)
v = d.values
posArray = v[:,1:4]

for i,position in enumerate(posArray):
    kml.newpoint(name=str(i), coords=[(position[1],position[0],position[2])])
    
kml.save("kml\linie_gps_v3.kml")
