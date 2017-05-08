from FileManager import FileManager
from PlotHelper import PlotHelper

filePath = "data\\arduino10DOF\\axes_sensitivity_minus_X_4.csv"
d = FileManager(filePath, columns=range(4,7), skip_header = 7)
v = d.values

x = v[:,0]

ph = PlotHelper()
ph.plot(range(0,d.length), x, 'ro')
ph.show()