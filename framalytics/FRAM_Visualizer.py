from read_xfmv import *
#from xfmv_parser import *
#import networkx as nx
import matplotlib
import textwrap
from matplotlib.bezier import BezierSegment

#matplotlib.use('WebAgg')
import matplotlib.pyplot as plt



class Visualizer:

    def __init__(self, file, figsize_x=1200, figsize_y=600, dpi=150, backend=None):
        self.file = file
        self.figsize_x = figsize_x  # Controls x-dimension of plot display
        self.figsize_y = figsize_y  # Controls y-dimension of plot display
        self.dpi = dpi  # Controls size of plot display.
        self.figure = None

        self.fram_data = None
        self.node_x_coords = []
        self.node_y_coords = []
        self.backend = backend  # Should be WebAgg or nbAgg (needs to be tested

        if self.backend != None:
            matplotlib.use(backend)

        # Sets visual dimensions for plot. (Hard coded currently).
        #px = 1 / plt.rcParams['figure.dpi']  # pixel in inches

        # plt.figure(figsize=(2433 * px, 657 * px), dpi=150)

        # Creates the figure dimensions and size.
        #plt.figure(figsize=(self.figsize_x * px, self.figsize_y * px), dpi=self.dpi)
        #plt.gca().invert_yaxis()
        #plt.axis("off")

    def function_nodes(self):
        # Gets FRAM data in tuple form.
        self.fram_data = read_xfmv(self.file)

        # X,Y coordinates of Nodes and the color and labels.
        self.node_x_coords = []
        self.node_y_coords = []

        # Gets the labels, colors, face colors and line width of each node
        node_labels = []
        node_colors = []
        node_facecolors = []  # Array of face colors
        node_lw = []  # Array of line widths (borders)

        # Will store true or false values for each feature (numbered by index) to determine if
        # they have inputs and/or outputs. Will determine if the facecolor is 'white" or very light grey '#F3F3F3'
        node_toFn = []
        node_outputFn = []

        # For loop that determines each node's x and y coordinates, label, and colors.
        for index, row in self.fram_data[0].iterrows():
            self.node_x_coords.append(float(row.x))
            self.node_y_coords.append(float(row.y))
            node_labels.append(row.IDName)

            # Converts node 32bit integer color to hexadecimal
            if type(row.color) == type(None):
                node_colors.append("black")
                node_lw.append(0.5)

            else:
                color = hex(int(row.color))
                color = color[2:]
                while len(color) < 6:
                    color = "0"+color
                color = "#"+color
                node_colors.append(color)
                node_lw.append(3)

            node_toFn.append(False)
            node_outputFn.append(False)

        # Determines which nodes (ordered by the functions IDNr = index) have outputs and/or inputs.
        for i in self.fram_data[2].toFn:
            if i != None:
                node_toFn[int(i)] = True

        for i in self.fram_data[2].outputFn:
            if i != None:
                node_outputFn[int(i)] = True

        for i in range(len(node_toFn)):
            # If a function/node has both an input and output, the face color is white.
            if (node_toFn[i]) and (node_outputFn[i]):
                node_facecolors.append('white')

            # If a function/node does not have both an input and output, the face color is very light grey.
            else:
                node_facecolors.append('#F3F3F3')



        plot_x_border = (max(self.node_x_coords) - min(self.node_x_coords) + 100)/100
        plot_y_border = (max(self.node_y_coords) - min(self.node_y_coords) + 100)/100

        #px = 1   # For FnStyle = 1
        px = 1.18  # For FnStyle = 0

        # Creates the figure dimensions and size.
        self.figure = plt.figure(figsize=(plot_x_border*px, plot_y_border*px), dpi=self.dpi)
        plt.gca().invert_yaxis()
        plt.axis("off")


        # Plots nodes.
        plt.scatter(self.node_x_coords, self.node_y_coords, label=node_labels, marker='H', s=1500, facecolors=node_facecolors, edgecolors=node_colors, lw=node_lw, zorder=3)

        # Makes multi-line labels
        for index, row in self.fram_data[0].iterrows():
            wrapped_label = textwrap.fill(row.IDName, width=13)
            plt.annotate(wrapped_label, (float(row.x), float(row.y)), ha='center', va='center', fontsize=4)

    def aspects(self):
        # Aspect creation
        aspects_x = []
        aspects_y = []
        aspect_labels = []
        aspects_per_function = []  # Stores aspect coordinates per function in order of FunctionID (Function IDNr).

        # Iterates through x and y location of each node to get aspect locations and connections (plus labelling)
        for x, y in zip(self.node_x_coords, self.node_y_coords):
            # T,C,I,O,P,R  coordinate ordering
            aspects_per_function.append([[x-23, y-35], [x+23, y-35], [x-44, y], [x+44, y], [x-23, y+35], [x+23, y+35]])

            # EACH ASPECT IS INDIVIDUALLY PLOTTED TO GENERATE A LINE BETWEEN ITSELF AND ITS ASSOCIATED FUNCTION NODE.

            # Top left (Note, y-axis is inverted) (T)
            aspects_x.append(x-23)
            aspects_y.append(y-35)
            aspect_labels.append("T")
            # Lower z-order prevents lines from going through nodes
            plt.plot([x-23, x], [y-35, y], color='black', zorder=2, lw=0.5)

            # Top right (C)
            aspects_x.append(x+23)
            aspects_y.append(y-35)
            aspect_labels.append("C")
            plt.plot([x+23, x], [y-35, y], color='black', zorder=2, lw=0.5)

            # Mid left (I)
            aspects_x.append(x-44)
            aspects_y.append(y)
            aspect_labels.append("I")
            plt.plot([x-44, x], [y, y], color='black', zorder=2, lw=0.5)

            # Mid right (O)
            aspects_x.append(x+44)
            aspects_y.append(y)
            aspect_labels.append("O")
            plt.plot([x+44, x], [y, y], color='black', zorder=2, lw=0.5)

            # Bottom left (P)
            aspects_x.append(x-23)
            aspects_y.append(y+35)
            aspect_labels.append("P")
            plt.plot([x-23, x], [y+35, y], color='black', zorder=2, lw=0.5)

            # Bottom right (R)
            aspects_x.append(x+23)
            aspects_y.append(y+35)
            aspect_labels.append("R")
            plt.plot([x+23, x], [y+35, y], color='black', zorder=2, lw=0.5)

        # Adds aspects to each node
        plt.scatter(aspects_x, aspects_y, s=30, facecolors='white', edgecolors='black', lw=0.5, zorder=3)

        # Applies proper labels to scatter plot
        for label, x, y in zip(aspect_labels, aspects_x, aspects_y):
            wrapped_label = textwrap.fill(label, break_long_words=False, width=1)
            plt.annotate(wrapped_label, (x, y), ha='center', va='center', fontsize=3.5)






    def bezier_curves(self):

        for i in self.fram_data[2].Curve:
            # Curve coordinates
            a = i.split("|")

            # Must be in this order!
            control_points = [(float(a[2]), float(a[3])), (float(a[4]), float(a[5])), (float(a[8]), float(a[9])), (float(a[6]), float(a[7])), (float(a[0]), float(a[1]))]
            bezier_segment = BezierSegment(control_points)

            x_pts = []
            y_pts = []
            for j in range(0, 101):
                x, y = bezier_segment.point_at_t(j/100)
                x_pts.append(x)
                y_pts.append(y)

            for j in range(len(x_pts)):
                x_pts[j] = x_pts[j] - 48

            for j in range(len(y_pts)):
                y_pts[j] = y_pts[j] - 50

            plt.plot(x_pts, y_pts, zorder=1, color='#999999', lw=1)




    def generate(self):
        self.function_nodes()
        self.aspects()
        self.bezier_curves()

    def display(self):
        plt.show()


    def generate_function_output_paths(self, output_function, input_function=None):
        """

        :param output_function: Output functionID number
        :param input_function: Input functionID number (Optional)
        :return:
        """
        #fram_data[0] = Function data
        #fram_data[1] = Function inputs?
        #fram_data[2] = Aspect connections (lines)


        if(input_function == None):
            for index, row in self.fram_data[2].iterrows():

                if ((row.outputFn == None) and (row.toFn == None)):
                    name_split = row.Name.split("|")  # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)

                    if (name_split[0] == output_function):
                        self.bezier_curve_single(row.Curve)
                else:
                    if (row.outputFn == output_function):
                        self.bezier_curve_single(row.Curve)

        else:
            for index, row in self.fram_data[2].iterrows():
                if ((row.outputFn == None) and (row.toFn == None)):
                    name_split = row.Name.split("|")  # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)

                    if ((name_split[0] == output_function) and (name_split[2] == input_function)):
                        self.bezier_curve_single(row.Curve)
                else:
                    if((row.outputFn == output_function) and (row.toFn == input_function)):
                        self.bezier_curve_single(row.Curve)



    def generate_full_path_from_function(self,output_function):
        """
        Generates the full path of a starting function from itself, to the end.
        This shows all the connections a function impacts.

        :param output_function: The string value IDNr for the starting function.

        :return: None. Results are displayed in a plot when called.
        """
        functions_in_path = []
        already_pathed = []
        current_function = output_function

        for index, row in self.fram_data[2].iterrows():

            # In the case the instance does not store the output and toFn Values, they seem to be stored in the name.
            if((row.outputFn == None) and (row.toFn == None)):
                name_split = row.Name.split("|") # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)
                if(name_split[0] == current_function):
                    functions_in_path.append(name_split[2])
                    self.bezier_curve_single(row.Curve)

            # For our Stroke Care System, this is used.
            else:
                if (row.outputFn == current_function):
                    functions_in_path.append(row.toFn)
                    self.bezier_curve_single(row.Curve)

        # Add this function to the path link, so that we don't repeat paths.
        already_pathed.append(current_function)

        #While all paths have not been searched
        while(len(functions_in_path) != 0):
            print(len(functions_in_path))
            current_function = functions_in_path.pop()
            if(current_function in already_pathed):
                continue

            for index, row in self.fram_data[2].iterrows():
                if ((row.outputFn == None) and (row.toFn == None)):
                    name_split = row.Name.split("|")  # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)
                    if (name_split[0] == current_function):
                        functions_in_path.append(name_split[2])
                        self.bezier_curve_single(row.Curve)

                    # For our Stroke Care System, this is used.
                else:
                    if (row.outputFn == current_function):
                        functions_in_path.append(row.toFn)
                        self.bezier_curve_single(row.Curve)

            already_pathed.append(current_function)

    def bezier_curve_single(self,curve):
        """
        :param curve: The curve string between two aspects which is given by the parser.

        :return: None. It plots the bezier curve of the given curve string.
        """
        # Curve coordinates
        a = curve.split("|")

        # Must be in this order!
        control_points = [(float(a[2]), float(a[3])), (float(a[4]), float(a[5])), (float(a[8]), float(a[9])),
                          (float(a[6]), float(a[7])), (float(a[0]), float(a[1]))]

        bezier_segment = BezierSegment(control_points)

        x_pts = []
        y_pts = []

        for j in range(0, 101):
            x, y = bezier_segment.point_at_t(j / 100)
            x_pts.append(x)
            y_pts.append(y)

        for j in range(len(x_pts)):
            x_pts[j] = x_pts[j] - 48

        for j in range(len(y_pts)):
            y_pts[j] = y_pts[j] - 50

        plt.plot(x_pts, y_pts, zorder=2, color='green', lw=1)




def main():
    test = Visualizer("FRAM model-Stroke care system.xfmv", backend='WebAgg', dpi=175)
    #test = Visualizer("FRAM model-Stroke care system.xfmv")
    #test = Visualizer("Cup Noodles.xfmv",backend="WebAgg")
    #test = Visualizer("prepare_work_example.xfmv",backend="WebAgg")
    #test = Visualizer("leave_harbor_example.xfmv",backend="WebAgg")

    # Does all the work to produce the FRAM visual, and displays it.
    test.generate()  # Generates the default model without modifications from the user.
    test.generate_function_output_paths("1","14")  # Highlights the output paths of a specific function given its Function#.
    #test.generate_full_path_from_function("1")
    test.display()  # Displays the graph


if __name__ == "__main__":
    main()


