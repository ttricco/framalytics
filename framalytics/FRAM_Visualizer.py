import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matplotlib.bezier import BezierSegment
import matplotlib.pyplot as plt
import textwrap


class Visualizer:

    def _create_figure(self,
                       function_data: pd.DataFrame) -> tuple[Figure, Axes]:
        """ Create a figure and axes of appropriate dimensions. """

        style = function_data.iloc[0]["fnStyle"]

        px = 1.18  # Default; fnStyle = 0
        if style == "1":
            px = 1.0  # fnStyle = 1

        dx = max(function_data['x']) - min(function_data['x'])
        dy = max(function_data['y']) - min(function_data['y'])
        figsize_x = px * (dx + 100)/100
        figsize_y = px * (dy + 100)/100

        fig, ax = plt.subplots(figsize=(figsize_x, figsize_y), dpi=150)
        return fig, ax

    def _hex_to_color(self,
                      hex_value: str) -> tuple[str, float]:
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

    def _draw_function_nodes(self,
                             function_data: pd.DataFrame,
                             connection_data: pd.DataFrame,
                             ax: Axes):
        """
        Draw FRAM functions onto a Matplotlib axes.

        Parameters
        ----------
        function_data : pd.DataFrame
            The function data from the FRAM model.
        connection_data : pd.DataFrame
            The connection data from the FRAM model.
        ax : Axes
            The Matplotlib axes.
        """

        # Gets the labels, colors, face colors and line width of each node
        node_colors = []
        node_lw = []  # Array of line widths (borders)

        # For loop that determines each node's x and y coordinates, label,
        # and colors.
        for index, row in function_data.iterrows():
            color, lw = self._hex_to_color(row.color)
            node_colors.append(color)
            node_lw.append(lw)

        node_labels = function_data['IDName'].tolist()

        # Will store true or false values for each feature (numbered by index)
        # to determine if they have inputs and/or outputs. Will determine if
        # the facecolor is 'white" or very light grey '#F3F3F3'
        node_toFn = [False] * len(function_data)
        node_outputFn = [False] * len(function_data)

        # Determines which nodes (ordered by the functions IDNr = index)
        # have outputs and/or inputs.
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

        # Plots function (Hexagon) nodes.
        # (The second plot provides the black outline around the nodes).
        ax.scatter(function_data['x'], function_data['y'],
                   label=node_labels, marker='H', s=1500,
                   facecolors=node_facecolors, edgecolors=node_colors,
                   lw=node_lw, zorder=3)
        ax.scatter(function_data['x'], function_data['y'],
                   label=node_labels, marker='H', s=1600,
                   facecolors=node_facecolors, edgecolors='black',
                   lw=node_lw, zorder=2)

        # Makes multi-line labels
        for index, row in function_data.iterrows():
            wrapped_label = textwrap.fill(row.IDName, width=13)
            plt.annotate(wrapped_label, (row.x, row.y), ha='center',
                         va='center', fontsize=4)

    def _draw_aspects(self,
                      node_x_coords: pd.Series | list,
                      node_y_coords: pd.Series | list,
                      ax: Axes):
        """
        Draw the six aspects around each function.

        Parameters
        ----------
        node_x_coords : pd.Series
            The x-coordinates of each function
        node_y_coords : pd.Series
            The y-coordinates of each function.
        ax : Axes
            The Matplotlib axes.
        """
        # Aspect creation
        aspects_x = []
        aspects_y = []
        aspect_labels = []
        aspects_per_function = []

        # Iterates through x and y location of each node to get aspect
        # locations and connections (plus labelling)
        for x, y in zip(node_x_coords, node_y_coords):
            # T,C,I,O,P,R  coordinate ordering
            aspects_per_function.append([[x-23, y-35],
                                         [x+23, y-35],
                                         [x-44, y],
                                         [x+44, y],
                                         [x-23, y+35],
                                         [x+23, y+35]])

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
        ax.scatter(aspects_x, aspects_y, s=30, facecolors='white',
                   edgecolors='black', lw=0.5, zorder=3)

        # Applies proper labels to scatter plot
        for label, x, y in zip(aspect_labels, aspects_x, aspects_y):
            wrapped_label = textwrap.fill(label, break_long_words=False,
                                          width=1)
            ax.annotate(wrapped_label, (x, y), ha='center', va='center',
                        fontsize=3.5)

    def _get_bezier_points(self,
                           curve: str) -> tuple[list, list]:
        """ Return a set (x, y) positions along each Bezier curve. """

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

    def _draw_bezier_curves(self,
                            connection_data: pd.DataFrame,
                            ax: Axes,
                            real_connections: dict | None = None,
                            appearance: str | None = None):
        """
        Draw connections between functions.

        Parameters
        ----------
        connection_data : pd.DataFrame
            The connection data from the FRAM model.
        ax : Axes
            The Matplotlib axes.
        real_connections : dict, optional
            A dictionary with the weighting of each connection. The keys
            of the dictionary are the raw string representing the connection.
        appearance : {'pure', 'traced', 'expand'}, optional
            The visual appearance of highlighted data. Defaults to 'pure'.
        """

        if isinstance(appearance, str):
            appearance = appearance.lower()

        if appearance not in [None, 'pure', 'traced', 'expand']:
            raise ValueError("Invalid highlighting appearance.")

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
                elif value <= 0.25:
                    color = "green"
                elif value <= 0.5:
                    color = "yellow"
                elif value <= 0.75:
                    color = "orange"
                elif value <= total_instances:
                    color = "red"

                if color == 'grey':
                    ax.plot(x_pts, y_pts, zorder=0, color=color,
                            lw=1, ls='--')

                # Paths are purely color, no outline.
                elif appearance == "pure":
                    ax.plot(x_pts, y_pts, zorder=2, color=color, lw=1)
                # Similar to pure color, but with a black outline.
                elif appearance == "traced":
                    ax.plot(x_pts, y_pts, zorder=2, color=color, lw=1)
                    ax.plot(x_pts, y_pts, zorder=1, color='black', lw=2)
                # A black line, but with the highlighted color being the
                # outline. This outline expands or contracts depending on the
                # value of "expand_value". This is usually between 0 - > 1.0
                # and is automated by the fram.py.
                elif appearance == "expand":
                    ax.plot(x_pts, y_pts, zorder=2, color='black', lw=1)
                    ax.plot(x_pts, y_pts, zorder=1, color=color, lw=2)

    def render(self,
               function_data: pd.DataFrame,
               connection_data: pd.DataFrame,
               real_connections: dict | None = None,
               appearance: str | None = None,
               ax: Axes | None = None) -> Axes:
        """
        Draw the FRAM model onto a Matplotlib axes.

        Parameters
        ----------
        function_data : pd.DataFrame
            The function data from the FRAM model.
        connection_data : pd.DataFrame
            The connection data from the FRAM model.
        real_connections : dict, optional
            A dictionary with the weighting of each connection. Used for
            highlighting connections based on a set of observations. The keys
            of the dictionary are the raw string representing the connection.
        appearance : {'pure', 'traced', 'expand'}, optional
            The visual appearance of highlighted data. Defaults to 'pure'.
        ax : Axes, optional
            The Matplotlib axes. If None, then a new Axes is created.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.
        """

        if ax is None:
            fig, ax = self._create_figure(function_data)

        self._draw_function_nodes(function_data, connection_data, ax=ax)
        self._draw_aspects(function_data['x'],
                           function_data['y'],
                           ax=ax)
        self._draw_bezier_curves(connection_data,
                                 real_connections=real_connections,
                                 appearance=appearance, ax=ax)

        return ax

    def render_output_paths(self,
                            function_data: pd.DataFrame,
                            connection_data: pd.DataFrame,
                            output_function: int,
                            input_function: int | None = None,
                            ax: Axes | None = None) -> Axes:
        """
        Highlights the output connections of a given function ID.

        Parameters
        ----------
        function_data : pd.DataFrame
            The function data from the FRAM model.
        connection_data : pd.DataFrame
            The connection data from the FRAM model.
        output_function : int
            The output function ID.
        input_function : int, optional
            The input function ID.
        ax : Axes, optional
            The Matplotlib axes. If None, then a new Axes is created.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.
        """

        connections = dict.fromkeys(connection_data['Name'].unique(), 0.0)

        if input_function is None:
            for index, row in connection_data.iterrows():
                if row.outputFn == output_function:
                    connections[row.Name] = 0.1
        else:
            for index, row in connection_data.iterrows():
                if (row.outputFn == output_function
                        and row.toFn == input_function):
                    connections[row.Name] = 0.1

        return self.render(function_data, connection_data,
                           real_connections=connections,
                           appearance="pure", ax=ax)

    def render_path_from_function(self,
                                  function_data: pd.DataFrame,
                                  connection_data: pd.DataFrame,
                                  output_function: int,
                                  ax: Axes | None = None) -> Axes:
        """
        Highlight all functions downstream of the specified function.

        Parameters
        ----------
        function_data : pd.DataFrame
            The function data from the FRAM model.
        connection_data : pd.DataFrame
            The connection data from the FRAM model.
        output_function : int
            The output function ID.
        ax : Axes, optional
            The Matplotlib axes. If None, then a new Axes is created.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.
        """

        function_stack = []
        already_pathed = [output_function]
        connections = dict.fromkeys(connection_data['Name'].unique(), 0.0)

        # Add all functions this function outputs to
        for index, row in connection_data.iterrows():
            if row.outputFn == output_function:
                function_stack.append(row.toFn)
                connections[row.Name] = 0.1

        # While all paths have not been searched
        while len(function_stack) != 0:
            current_function = function_stack.pop()

            if current_function in already_pathed:
                continue

            for index, row in connection_data.iterrows():
                if row.outputFn == current_function:
                    function_stack.append(row.toFn)
                    connections[row.Name] = 0.1

            already_pathed.append(current_function)

        return self.render(function_data, connection_data,
                           real_connections=connections,
                           appearance="pure", ax=ax)
