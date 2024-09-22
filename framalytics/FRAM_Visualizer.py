import matplotlib
import textwrap
from matplotlib.bezier import BezierSegment
import matplotlib.pyplot as plt


class Visualizer:

    def _create_figure(self, function_data):
        """ Create a figure / axis of appropriate dimensions. """

        style = function_data.iloc[0]["fnStyle"]

        px = 1.18  # Default; fnStyle = 0
        if style == "1":
            px = 1.0  # fnStyle = 1

        figsize_x = px * (max(function_data['x']) - min(function_data['x']) + 100)/100
        figsize_y = px * (max(function_data['y']) - min(function_data['y']) + 100)/100

        fig, ax = plt.subplots(figsize=(figsize_x, figsize_y), dpi=150)
        return fig, ax

    def _hex_to_color(self, hex_value):
        """ Converts node 32bit integer color to hexadecimal. """

        color = "black"
        lw = 0.5

        if hex_value is not None:
            color = hex(int(hex_value))
            color = color[2:]
            while len(color) < 6:
                color = "0" + color
            color = "#" + color
            lw = 3

        return color, lw

    def _draw_function_nodes(self, function_data, connection_data, ax):
        """
        Generates the Function Nodes based on the data given from the FRAM class.

        :param function_data: Function data from FRAM class
        :param connection_data:  Aspect data from FRAM class

        :return: None. Used to plot Function nodes on scatterplot.
        """

        # Gets the labels, colors, face colors and line width of each node
        node_colors = []
        node_lw = []  # Array of line widths (borders)

        # For loop that determines each node's x and y coordinates, label, and colors.
        for index, row in function_data.iterrows():
            color, lw = self._hex_to_color(row.color)
            node_colors.append(color)
            node_lw.append(lw)

        node_labels = function_data['IDName'].tolist()

        # Will store true or false values for each feature (numbered by index) to determine if
        # they have inputs and/or outputs. Will determine if the facecolor is 'white" or very light grey '#F3F3F3'
        node_toFn = [False] * len(function_data)
        node_outputFn = [False] * len(function_data)

        # Determines which nodes (ordered by the functions IDNr = index) have outputs and/or inputs.
        for i in connection_data.toFn:
            if i is not None:
                node_toFn[i] = True

        for i in connection_data.outputFn:
            if i is not None:
                node_outputFn[i] = True

        node_facecolors = []  # Array of face colors
        # If the function type is 0, the facecolor is white
        for index, row in function_data.iterrows():
            if row.FunctionType == 0:
                node_facecolors.append('white')
            else:
                node_facecolors.append('#F3F3F3')

        # Creates the figure dimensions and size.
        ax.invert_yaxis()
        ax.axis("off")

        # Plots function (Hexagon) nodes. (The second plot provides the black outline around the nodes).
        ax.scatter(function_data['x'], function_data['y'],
                   label=node_labels, marker='H', s=1500, facecolors=node_facecolors, edgecolors=node_colors, lw=node_lw, zorder=3)
        ax.scatter(function_data['x'], function_data['y'],
                   label=node_labels, marker='H', s=1600, facecolors=node_facecolors, edgecolors='black', lw=node_lw, zorder=2)

        # Makes multi-line labels
        for index, row in function_data.iterrows():
            wrapped_label = textwrap.fill(row.IDName, width=13)
            plt.annotate(wrapped_label, (row.x, row.y), ha='center', va='center', fontsize=4)

    def _draw_aspects(self, node_x_coords, node_y_coords, ax):
        """
        Generates the Aspects of each Function Node.

        :return: None. Adds the aspects of function nodes to the plot.
        """
        # Aspect creation
        aspects_x = []
        aspects_y = []
        aspect_labels = []
        aspects_per_function = []  # Stores aspect coordinates per function in order of FunctionID (Function IDNr).

        # Iterates through x and y location of each node to get aspect locations and connections (plus labelling)
        for x, y in zip(node_x_coords, node_y_coords):
            # T,C,I,O,P,R  coordinate ordering
            aspects_per_function.append([[x-23, y-35], [x+23, y-35], [x-44, y], [x+44, y], [x-23, y+35], [x+23, y+35]])

            # EACH ASPECT IS INDIVIDUALLY PLOTTED TO GENERATE A LINE BETWEEN ITSELF AND ITS ASSOCIATED FUNCTION NODE.

            # Top left (Note, y-axis is inverted) (T)
            aspects_x.append(x-23)
            aspects_y.append(y-35)
            aspect_labels.append("T")
            # Lower z-order prevents lines from going through nodes
            ax.plot([x-23, x], [y-35, y], color='black', zorder=2, lw=0.5)

            # Top right (C)
            aspects_x.append(x+23)
            aspects_y.append(y-35)
            aspect_labels.append("C")
            ax.plot([x+23, x], [y-35, y], color='black', zorder=2, lw=0.5)

            # Mid left (I)
            aspects_x.append(x-44)
            aspects_y.append(y)
            aspect_labels.append("I")
            ax.plot([x-44, x], [y, y], color='black', zorder=2, lw=0.5)

            # Mid right (O)
            aspects_x.append(x+44)
            aspects_y.append(y)
            aspect_labels.append("O")
            ax.plot([x+44, x], [y, y], color='black', zorder=2, lw=0.5)

            # Bottom left (P)
            aspects_x.append(x-23)
            aspects_y.append(y+35)
            aspect_labels.append("P")
            ax.plot([x-23, x], [y+35, y], color='black', zorder=2, lw=0.5)

            # Bottom right (R)
            aspects_x.append(x+23)
            aspects_y.append(y+35)
            aspect_labels.append("R")
            ax.plot([x+23, x], [y+35, y], color='black', zorder=2, lw=0.5)

        # Adds aspects to each node
        ax.scatter(aspects_x, aspects_y, s=30, facecolors='white', edgecolors='black', lw=0.5, zorder=3)

        # Applies proper labels to scatter plot
        for label, x, y in zip(aspect_labels, aspects_x, aspects_y):
            wrapped_label = textwrap.fill(label, break_long_words=False, width=1)
            ax.annotate(wrapped_label, (x, y), ha='center', va='center', fontsize=3.5)

    def _get_bezier_points(self, curve):

        # Curve coordinates
        a = curve.split("|")

        # Must be in this order!
        control_points = [(float(a[2]), float(a[3])),
                          (float(a[4]), float(a[5])),
                          (float(a[8]), float(a[9])),
                          (float(a[6]), float(a[7])),
                          (float(a[0]), float(a[1]))]
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

        return x_pts, y_pts

    def _draw_bezier_curves(self, connection_data, ax, real_connections=None, appearance=None):
        """
        Generates the bezier curves (lines) between two aspects using the aspect data given
        from the FRAM class.

        :param connection_data: Aspect data given from FRAM class (Automatically given by the class).

        :return: None. Adds the line connections between two aspects to the plot.
        """

        if isinstance(appearance, str):
            appearance = appearance.lower()

        if appearance not in [None, 'pure', 'traced', 'expand']:
            raise ValueError("Invalid highlighting appearance for connections.")

        if appearance is None and real_connections is not None:
            appearance = 'pure'

        for index, row in connection_data[['Name', 'Curve']].iterrows():
            curve = row['Curve']
            name = row['Name']

            x_pts, y_pts = self._get_bezier_points(curve)

            if real_connections is None:
                ax.plot(x_pts, y_pts, zorder=1, color='#999999', lw=1)
            else:

                value = real_connections[name]
                total_instances = len(real_connections)

                color = "grey"
                if value == 0:
                    color = "grey"
                elif value <= int(total_instances * 0.25):
                    color = "green"
                elif value <= int(total_instances * 0.5):
                    color = "yellow"
                elif value <= int(total_instances * 0.75):
                    color = "orange"
                elif value <= total_instances:
                    color = "red"

                # Paths are purely color, no outline.
                if appearance == "pure":
                    if color == 'grey':
                        ax.plot(x_pts, y_pts, zorder=0, color=color, lw=1, linestyle='--')
                    else:
                        ax.plot(x_pts, y_pts, zorder=2, color=color, lw=1)

                # Similar to pure color, but with a black outline.
                elif appearance == "traced":
                    if color == "grey":
                        ax.plot(x_pts, y_pts, zorder=0, color=color, lw=1, linestyle='--')
                    else:
                        ax.plot(x_pts, y_pts, zorder=2, color=color, lw=1)
                        ax.plot(x_pts, y_pts, zorder=1, color='black', lw=2)

                # A black line, but with the highlighted color being the outline.
                # This outline expands or contracts depending on the value of "expand_value".
                # This is usually between 0 - > 1.0 and is automated by the fram.py.
                elif appearance == "expand":
                    if color == "grey":
                        ax.plot(x_pts, y_pts, zorder=0, color=color, lw=1, linestyle='--')
                    else:
                        ax.plot(x_pts, y_pts, zorder=2, color='black', lw=1)
                        ax.plot(x_pts, y_pts, zorder=1, color= color, lw=2)

    def generate(self,
                 function_data,
                 connection_data,
                 real_connections=None,
                 appearance=None,
                 ax=None):
        """
        Generates the default FRAM model using the data given from the FRAM class

        :param function_data: Function Data given by FRAM class (automatic).
        :param connection_data: Aspect Data given by FRAM class (automatic).
        :param curves: Determines if the bezier curves are drawn or not.

        :return: None. Plots the default FRAM model which is displayed when called by "display()".
        """

        if ax is None:
            fig, ax = self._create_figure(function_data)

        self._draw_function_nodes(function_data, connection_data, ax=ax)
        self._draw_aspects(function_data['x'],
                           function_data['y'],
                           ax=ax)
        self._draw_bezier_curves(connection_data, real_connections=real_connections,
                                 appearance=appearance, ax=ax)

        return ax

    def generate_function_output_paths(self, function_data, connection_data,
                                       output_function, input_function=None, ax=None):
        """
        Highlights the output paths of a function based on the given FunctionID.

        :param output_function: Output functionID number. (Integer).
        :param input_function: Input functionID number (Optional) (Integer).

        :return: None. Highlights a functions outputs on the model.
        """

        connections = dict.fromkeys(connection_data.Name.unique(), 0)

        if input_function is None:
            for index, row in connection_data.iterrows():
                if int(row.outputFn) == output_function:
                    connections[row.Name] = 1
                    # self.bezier_curve_single(row.Curve)
        else:
            for index, row in connection_data.iterrows():
                if (int(row.outputFn) == output_function) and (int(row.toFn) == input_function):
                    connections[row.Name] = 1
                    # self.bezier_curve_single(row.Curve)

        return self.generate(function_data, connection_data, real_connections=connections,
                             appearance="pure", ax=ax)

    def generate_full_path_from_function(self, function_data, connection_data,
                                         output_function, ax=None):
        """
        Generates the full path of a starting function from itself, to the end.
        This shows all the connections a function impacts.

        :param output_function: The integer value IDNr for the starting function.

        :return: None. Results are displayed in a plot when called.
        """

        function_stack = []
        already_pathed = [int(output_function)]
        connections = dict.fromkeys(connection_data.Name.unique(), 0)

        # Add all functions this function outputs to
        for index, row in connection_data.iterrows():
            if int(row.outputFn) == output_function:
                function_stack.append(int(row.toFn))
                connections[row.Name] = 1

        #While all paths have not been searched
        while len(function_stack) != 0:
            current_function = function_stack.pop()

            if current_function in already_pathed:
                continue

            for index, row in connection_data.iterrows():
                if int(row.outputFn) == current_function:
                    function_stack.append(int(row.toFn))
                    connections[row.Name] = 1

            already_pathed.append(current_function)

        return self.generate(function_data, connection_data, real_connections=connections,
                             appearance="pure", ax=ax)


