from read_xfmv import *
from xfmv_parser import *
import networkx as nx
import matplotlib
matplotlib.use('WebAgg')

import matplotlib.pyplot as plt
import textwrap

def function_nodes():
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


    # Plots nodes.
    plt.scatter(test_x, test_y, label=test_label, marker='H', s=1500, facecolors='white', edgecolors=test_color, lw=5, zorder=2)


    # Makes multi-line labels
    for index, row in fram_data[0].iterrows():
        wrapped_label = textwrap.fill(row.IDName,width=15)
        plt.annotate(wrapped_label,(float(row.x),float(row.y)), ha='center', va='center', fontsize=5)

    return [fram_data,test_x,test_y]


def aspects(fram_data,test_x,test_y):
    # Aspect creation
    aspects_x = []
    aspects_y = []
    aspect_labels = []
    aspects_per_function = [] #S tores aspect coordinates per function in order of FunctionID (Function IDNr).

    # Iterates through x and y location of each node to get aspect locations and connections (plus labelling)
    for x, y in zip(test_x,test_y):
        # T,C,I,O,P,R
        aspects_per_function.append([[x-25,y-35],[x+25,y-35],[x-44,y],[x+44,y],[x-25,y+35],[x+25,y+35]])

        # Top left (Note, y-axis is inverted) (T)
        aspects_x.append(x-25)
        aspects_y.append(y-35)
        aspect_labels.append("T")
        plt.plot([x-25,x],[y-35,y],color='black',zorder=1)  #Lower zorder prevents lines from going through nodes

        # Top right (C)
        aspects_x.append(x+25)
        aspects_y.append(y-35)
        aspect_labels.append("C")
        plt.plot([x+25, x], [y-35, y], color='black',zorder=1)

        # Mid left (I)
        aspects_x.append(x-44)
        aspects_y.append(y)
        aspect_labels.append("I")
        plt.plot([x-44, x], [y, y], color='black',zorder=1)

        # Mid right (O)
        aspects_x.append(x+44)
        aspects_y.append(y)
        aspect_labels.append("O")
        plt.plot([x+44, x], [y, y], color='black',zorder=1)

        # Bottom left (P)
        aspects_x.append(x-25)
        aspects_y.append(y+35)
        aspect_labels.append("P")
        plt.plot([x-25, x], [y+35, y], color='black',zorder=1)

        # Bottom right (R)
        aspects_x.append(x+25)
        aspects_y.append(y+35)
        aspect_labels.append("R")
        plt.plot([x+25, x], [y+35, y], color='black',zorder=1)

    # Adds aspects to each node
    plt.scatter(aspects_x, aspects_y, s=30, facecolors='white', edgecolors='black', lw=0.5,zorder=2)

    # Applies proper labels to scatter plot
    for label, x, y in zip(aspect_labels, aspects_x, aspects_y):
        wrapped_label = textwrap.fill(label, break_long_words=False,width=15)
        plt.annotate(wrapped_label, (x, y), ha='center', va='center', fontsize=5)

def bezier_curves(fram_data):
    #BEZIER CURVE

    import matplotlib.pyplot as plt
    from matplotlib.bezier import BezierSegment

    for i in fram_data[2].Curve:
        # Curve coordinates
        a = i.split("|")
        # Must be in this order!
        control_points = [(float(a[2]), float(a[3])), (float(a[4]), float(a[5])), (float(a[8]), float(a[9])), (float(a[6]), float(a[7])), (float(a[0]), float(a[1]))]
        bezier_segment = BezierSegment(control_points)

        x_pts = []
        y_pts = []
        for i in range(0, 101):
            x, y = bezier_segment.point_at_t(i / 100)
            x_pts.append(x)
            y_pts.append(y)

        for i in range(len(x_pts)):
            x_pts[i] = x_pts[i] - 48

        for i in range(len(y_pts)):
            y_pts[i] = y_pts[i] - 50

        plt.plot(x_pts, y_pts, zorder=1,color='silver')



def main():
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    plt.figure(figsize=(2433*px, 657*px))

    test = function_nodes()
    aspects(test[0],test[1],test[2])
    bezier_curves(test[0])

    plt.gca().invert_yaxis()
    plt.axis("off")

    ##Stretches axis to take up entire canvas
    #plt.tight_layout()

    # Displays copied FRAM in python.
    plt.show()
    exit()

if __name__ == "__main__":
    main()

