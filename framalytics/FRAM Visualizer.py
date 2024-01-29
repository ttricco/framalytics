from read_xfmv import *
from xfmv_parser import *
import networkx as nx
import matplotlib.pyplot as plt
import textwrap

# Gets FRAM data in tuple form.
# Tuple[0] = Function Element Data
# Tuple[1] = Input Element Info for function connections
# Tuple[2] = Aspect Element Data
fram_data = read_xfmv("FRAM model-Stroke care system.xfmv")


# Scatter plot sample for FRAM replication

# X,Y coordinates of Nodes and the color and labels.
test_x = []
test_y = []
test_label = []
test_color = []


for index, row in fram_data[0].iterrows():
    test_x.append(float(row.x))
    test_y.append(float(row.y))
    test_label.append(row.IDName)

    #Converts node 32bit integer color to hexadecimal
    if type(row.color) == type(None):
        test_color.append("black")
    else:
        color = hex(int(row.color))
        color = color[2:]
        while(len(color)<6):
            color = "0"+color
        color = "#"+color
        test_color.append(color)




# Makes figure size
plt.figure(figsize=(30, 8))

#plt.figure(figsize(30,8)).canvas.manager.toolbar.pan()


# Plots nodes.
plt.scatter(test_x, test_y, label=test_label, marker='H', s=1000, facecolors='white', edgecolors=test_color, lw=5, zorder=2)


# Makes multi-line labels
for index, row in fram_data[0].iterrows():
    wrapped_label = textwrap.fill(row.IDName,width=13)
    plt.annotate(wrapped_label,(float(row.x),float(row.y)), ha='center', va='center', fontsize=5)


# Aspect creation
aspects_x = []
aspects_y = []
aspect_labels = []
aspects_per_function = [] #S tores aspect coordinates per function in order of FunctionID (Function IDNr).

# Iterates through x and y location of each node to get aspect locations and connections (plus labelling)
for x, y in zip(test_x,test_y):
    # T,C,I,O,P,R
    aspects_per_function.append([[x-20,y-20],[x+20,y-20],[x-40,y],[x+40,y],[x-20,y+20],[x+20,y+20]])

    # Top left (Note, y-axis is inverted) (T)
    aspects_x.append(x-20)
    aspects_y.append(y-20)
    aspect_labels.append("T")
    plt.plot([x-20,x],[y-20,y],color='black',zorder=1)  #Lower zorder prevents lines from going through nodes

    # Top right (C)
    aspects_x.append(x+20)
    aspects_y.append(y-20)
    aspect_labels.append("C")
    plt.plot([x+20, x], [y-20, y], color='black',zorder=1)

    # Mid left (I)
    aspects_x.append(x-40)
    aspects_y.append(y)
    aspect_labels.append("I")
    plt.plot([x-40, x], [y, y], color='black',zorder=1)

    # Mid right (O)
    aspects_x.append(x+40)
    aspects_y.append(y)
    aspect_labels.append("O")
    plt.plot([x+40, x], [y, y], color='black',zorder=1)

    # Bottom left (P)
    aspects_x.append(x-20)
    aspects_y.append(y+20)
    aspect_labels.append("P")
    plt.plot([x-20, x], [y+20, y], color='black',zorder=1)

    # Bottom right (R)
    aspects_x.append(x+20)
    aspects_y.append(y+20)
    aspect_labels.append("R")
    plt.plot([x+20, x], [y+20, y], color='black',zorder=1)

# Adds aspects to each node
plt.scatter(aspects_x, aspects_y, s=75, facecolors='white', edgecolors='black', lw=0.5,zorder=2)

# Applies proper labels to scatter plot
for label, x, y in zip(aspect_labels, aspects_x, aspects_y):
    wrapped_label = textwrap.fill(label, break_long_words=False)
    plt.annotate(wrapped_label, (x, y), ha='center', va='center', fontsize=5)


# Applies lines associated with each aspect connection. START OF NEW
# T,C,I,O,P,R

for index, row in fram_data[2].iterrows():
    # Breaks aspect connection into 4 parts (output function number,connection name,input function number,input aspect)
    connection = row.Name.split("|")

    # From function number
    from_function = int(connection[0])
    # To function number
    to_function = int(connection[2])

    # To function number aspect being connected
    to_aspect = connection[3]
    # Used to get proper index.
    aspect_letters = "TCIOPR"

    # Gets coordinates of aspect letter.
    to_aspect_index = aspect_letters.find(to_aspect)

    # Plots line from output aspect to input aspect between functions.
    plt.plot([aspects_per_function[from_function][3][0],aspects_per_function[to_function][to_aspect_index][0]], [aspects_per_function[from_function][3][1], aspects_per_function[to_function][to_aspect_index][1]],color='grey',zorder=1)


plt.gca().invert_yaxis()
plt.axis("off")

##Stretches axis to take up entire canvas
plt.tight_layout()


#Displays copied FRAM in python.
plt.show()


"""
#Output
print(fram_data[0][fram_data[0].IDNr == "72"].IDName)
print()

#Input
print(fram_data[0][fram_data[0].IDNr == "57"].IDName)
print()

#Gives the Aspect Curve
print(fram_data[1][fram_data[1].FunctionIDNr == "72"])
#print(fram_data[2].Curve)
print()
#test = fram_data[2].query('toFn == "72" and outputFn == "57"')
test = fram_data[2][(fram_data[2].toFn == "72") & (fram_data[2].outputFn == "57")]
curve = test.iat[0,8]
curve = curve.split("|")
for i in range(len(curve)):
    curve[i] = float(curve[i])
print(curve)
curve_x = [curve[0],curve[2],curve[4],curve[6],curve[8]]
curve_y = [curve[1],curve[3],curve[5],curve[7],curve[9]]
plt.scatter(curve_x,curve_y)
plt.show()
"""

