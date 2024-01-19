from read_xfmv import *
from xfmv_parser import *
import networkx as nx
import matplotlib.pyplot as plt
import textwrap

# Gets FRAM data in tuple form.
# Tuple[0] = Function Element Data
# Tuple[1] = Input Element Info
# Tuple[2] = Aspect Element Data
fram_data = read_xfmv("FRAM model-Stroke care system.xfmv")


"""
# Networkx sample of FRAM replication

print("FRAM tuple 0:")
print(fram_data[0])
print()
print("FRAM tuple 1:")
print(fram_data[1])
print()
print("FRAM tuple 2:")
print(fram_data[2])
print()
"""



# Scatter plot sample for FRAM replication

# X and Y coordinates of Nodes
test_x = []
test_y = []
test_label = []

for index, row in fram_data[0].iterrows():
    test_x.append(float(row.x))
    test_y.append(float(row.y))
    test_label.append(row.IDName)

# Plots Nodes
plot = plt.subplot()
plot.scatter(test_x, test_y,marker='H', s=2000,facecolors='white',edgecolors='black',lw=5)

#Makes multi-line labels
for index, row in fram_data[0].iterrows():
    wrapped_label = textwrap.fill(row.IDName,width=10)
    plot.annotate(wrapped_label,(float(row.x),float(row.y)), ha='center', va='center', fontsize=7)




plot.invert_yaxis()
plot.axis("off")
#plt.text FOR STRING WRAPPING

#print(fram_data[0][fram_data[0].IDNr == "1"])
#print(fram_data[0][fram_data[0].IDNr == "0"].IDName)
#print(fram_data[1][fram_data[1].FunctionIDNr == "1"])
#print(fram_data[2].Curve)

plt.show()
