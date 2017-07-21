from FileManager import CSVImporter
import matplotlib.pyplot as plt

filePath = "output_Strapdown_rectangle.csv"
d = CSVImporter(filePath, columns=[0,2,3,4,5,6,7,8,9,10 ], skip_header = 20, hasTime=False)
print(d.values)
plt.plot(d.values[:,0]-1500564695.788426, d.values[:,9],'r-')
plt.grid()
plt.show()