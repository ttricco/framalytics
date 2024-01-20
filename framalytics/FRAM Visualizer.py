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


# Makes figure size
plt.figure(figsize=(20, 8))


# Plots nodes.
plt.scatter(test_x, test_y,marker='H', s=2000,facecolors='white',edgecolors='black',lw=5,zorder=2)


# Makes multi-line labels
for index, row in fram_data[0].iterrows():
    wrapped_label = textwrap.fill(row.IDName,width=10)
    plt.annotate(wrapped_label,(float(row.x),float(row.y)), ha='center', va='center', fontsize=7)

##### NEW

# Aspect creation
aspects_x = []
aspects_y = []
aspect_labels = []

# Iterates through x and y location of each node to get aspect locations and connections (plus labelling)
for x, y in zip(test_x,test_y):
    # Top left (Note, y-axis is inverted) (T)
    aspects_x.append(x-25)
    aspects_y.append(y-25)
    aspect_labels.append("T")
    plt.plot([x-25,x],[y-25,y],color='black',zorder=1)  #Lower zorder prevents lines from going through nodes

    # Top right (C)
    aspects_x.append(x+25)
    aspects_y.append(y-25)
    aspect_labels.append("C")
    plt.plot([x+25, x], [y-25, y], color='black',zorder=1)

    # Mid left (I)
    aspects_x.append(x-60)
    aspects_y.append(y)
    aspect_labels.append("I")
    plt.plot([x-60, x], [y, y], color='black',zorder=1)

    # Mid right (O)
    aspects_x.append(x+60)
    aspects_y.append(y)
    aspect_labels.append("O")
    plt.plot([x+60, x], [y, y], color='black',zorder=1)

    # Bottom left (P)
    aspects_x.append(x-25)
    aspects_y.append(y+25)
    aspect_labels.append("P")
    plt.plot([x-25, x], [y+25, y], color='black',zorder=1)

    # Bottom right (R)
    aspects_x.append(x+25)
    aspects_y.append(y+25)
    aspect_labels.append("R")
    plt.plot([x+25, x], [y+25, y], color='black',zorder=1)

# Adds aspects to each node
plt.scatter(aspects_x, aspects_y, s=75, facecolors='white', edgecolors='black', lw=1)

# Applies proper labels to scatter plot
for label, x, y in zip(aspect_labels, aspects_x, aspects_y):
    wrapped_label = textwrap.fill(label)
    plt.annotate(wrapped_label, (x, y), ha='center', va='center', fontsize=5)



##### END OF NEW


plt.gca().invert_yaxis()
plt.axis("off")

##Stretches axis to take up entire canvas
plt.tight_layout()


plt.show()

#print(fram_data[0][fram_data[0].IDNr == "1"])
#print(fram_data[0][fram_data[0].IDNr == "0"].IDName)
#print(fram_data[1][fram_data[1].FunctionIDNr == "1"])
#print(fram_data[2].Curve)