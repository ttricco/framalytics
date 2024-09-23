from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes

from .FRAM_Visualizer import *
from .xfmv_parser import parse_xfmv


class FRAM:
    """
    FRAM objects hold FRAM models.

    FRAM objects can render FRAM models and act as a general interface for
    FRAM models. They can be created by reading FRAM models specified by an
    .xfmv file created by the FRAM Model Visualizer.
    """
    def __init__(self, filename):
        """
        Initialize a FRAM object from an .xfmv file.

        :param filename: The name of the .xfmv file being used.
        """
        self.filename = filename

        fram_data = parse_xfmv(filename)
        self._function_data = fram_data[0]
        self._connection_data = fram_data[2]

        self.visualizer = Visualizer()
        self.functions_by_id = {}
        self.functions_by_name = {}

        for index, row in self._function_data.iterrows():
            self.functions_by_id.update({int(row.IDNr): row.IDName})
            self.functions_by_name.update({row.IDName: int(row.IDNr)})


    def get_function_metadata(self) -> pd.DataFrame:
        """
        Returns the function data of the FRAM model.

        :return: A list of function data. Each index is a different function
        """

        return self._function_data

    def get_connection_data(self) -> pd.DataFrame:
        """
        Returns the aspect connection data of the FRAM model.

        :return: A list of aspect connection data. Each index is a different
        connection between two aspects.
        """

        return self._connection_data

    def get_functions(self) -> dict:
        """
        Returns the dictionary of functions.

        The keys of the dictionary are the function IDs and the values are the
        function names.

        :return: A dictionary of functions (keys = ID, values = name).
        """
        return self.functions_by_id

    def get_connections(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame of all the connections.

        Each row of the DataFrame is a connection. Connections all start from
        the output aspect of one function and connect to an aspect of another
        function. Each row has the source function (fromFn), the destination
        function (toFn), the aspect on the destination function (toAspect),
        and the name of the function (toName).

        :return: A pandas DataFrame consisting of all connections.
        """

        columns = ['outputFn', 'toFn', 'toAspect', 'parsed_name']
        rename = {'outputFn' : 'fromFn', 'parsed_name': 'Name'}
        return self._connection_data[columns].rename(columns=rename)

    def number_of_edges(self) -> int:
        """
        Returns the number of connections (edges) in the FRAM model.

        :return: The number of connections (edges/lines) in the FRAM model.
        """

        return len(self._connection_data)

    def number_of_functions(self) -> int:
        """
        Returns the number of functions in the FRAM model.

        :return: The total number of functions in a FRAM model.
        """

        number_of_functions = len(self.functions_by_id.items())
        return number_of_functions

    def get_function_id(self,
                        name: str) -> int:
        """
        Return the corresponding function ID given a function name.

        :param name: The exact name of a function.

        :return: The FunctionID that corresponds to the given function name.
        """
        if not isinstance(name, str):
            raise Exception("Invalid input. A string value should be used.")

        function_id = self.functions_by_name.get(name)
        return function_id

    def get_function_name(self,
                          id: int) -> str:
        """
        Return the corresponding function name given a function ID.

        :param id: The ID (integer) of a function.

        :return: The name of the function for the corresponding given ID.
        """
        if not isinstance(id, int):
            raise Exception("Invalid input. A integer value should be used.")

        function_name = self.functions_by_id.get(id)
        return function_name

    def get_function_inputs(self,
                            function: str | int) -> dict:
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as inputs to the input aspect
        of the desired function.

        :param function: The ID (integer) or name (string) of the desired function.
        :return: A dictionary consisting of the functions that serve as inputs to the input aspect of the function.
        """

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.
        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_inputs = {}  # This will store all the functions inputs in a dictionary {key=id, value = name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "I":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_inputs.update({row['outputFn']: outputfn_name})

        return function_inputs

    def get_function_outputs(self,
                             function: str | int) -> dict:
        """
        Gets a dictionary of key/value pairs that consist of the functions that use the output aspect of the desired
        function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that use the desired functions output aspect.
        """

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_outputs = {}

        for index, row in self._connection_data.iterrows():
            if row['outputFn'] == id:
                tofn_name = self.get_function_name(row['toFn'])
                function_outputs.update({row['toFn']: tofn_name})

        return function_outputs

    def get_function_preconditions(self,
                                   function: str | int) -> dict:
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as preconditions to the
        precondition aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as preconditions to
            the precondition aspect of the function.
        """

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        # This will store all the functions preconditions in a dictionary {key=id, value = name}
        function_preconditions = {}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "P":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_preconditions.update({row['outputFn']: outputfn_name})

        return function_preconditions

    def get_function_resources(self,
                               function: str | int) -> dict:
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as resources to the
        resource aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as resources to the resource aspect of the function.
        """

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_resources = {}  # This will store all the functions resources in a dictionary {key=id, value = name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "R":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_resources.update({row['outputFn']: outputfn_name})

        return function_resources

    def get_function_controls(self,
                              function: str | int) -> dict:
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as controls to the
        time aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as controls to the control aspect of the function.
        """

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_controls = {}  # This will store all the functions controls in a dictionary {key=id, value = name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "C":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_controls.update({row['outputFn']: outputfn_name})

        return function_controls

    def get_function_times(self,
                           function: str | int) -> dict:
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as times to the
        time aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as times to the time aspect of the function.
        """

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_times = {}  # This will store all the functions times in a dictionary {key=id, value = name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "T":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_times.update({row['outputFn']: outputfn_name})

        return function_times

    def visualize(self,
                  ax: Axes | None = None) -> Axes:
        """
        Visualizes the model by calling to the Visualizer class of FRAM_Visualizer.py. This generates the default model.

        :param backend: The backend matplotlib will use to display the model through the Visualizer class.

        :return: None. Generates the FRAM model.
        """

        return self.visualizer.generate(self._function_data, self._connection_data, ax=ax)

    def display(self):
        """
        Simply displays the current FRAM Model plot.

        :return: None. Displays the FRAM plot.
        """
        plt.show()

    def highlight_function_outputs(self,
                                   function: str | int,
                                   ax: Axes | None = None) -> Axes:
        """
        Highlights the outputs of a function.

        :param functionID: Integer value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """
        if isinstance(function, str):
            functionID = self.get_function_id(function)
        elif isinstance(function, int):
            functionID = function
        else:
            raise ValueError("Invalid input. A function ID (integer) or function name (string) is required.")

        return self.visualizer.generate_function_output_paths(self._function_data,
                                                       self._connection_data, functionID, ax=ax)

    def highlight_full_path_from_function(self,
                                          function: str | int,
                                          ax: Axes | None = None) -> Axes:
        """
        Highlights all the paths that are connected to a starting function.

        :param functionID: Integer value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """
        if isinstance(function, str):
            functionID = self.get_function_id(function)
        elif isinstance(function, int):
            functionID = function
        else:
            raise ValueError("Invalid input. A function ID (integer) or function name (string) is required.")

        return self.visualizer.generate_full_path_from_function(self._function_data,
                                                         self._connection_data, functionID, ax=ax)

    def _count_real_data_connections(self,
                                     real_data: pd.DataFrame,
                                     column_type: str = "functions") -> dict:

        connections = {}  # Stores the connections between two aspects and the number of times it's traversed.
        for index, row in self._connection_data.iterrows():
            connections.update({row.Name: 0})

        column_type = column_type.lower()
        # If the dataframe uses function names for the column names.
        if column_type == "functions":
            for connection_default in connections:
                # Splits connection to get information
                connection = connection_default.split("|")

                # Get output and input function ID's
                outputFn = int(connection[0])
                toFn = int(connection[2])

                # Stores the names of the functions.
                outputFn_name = self.functions_by_id.get(outputFn)
                toFn_name = self.functions_by_id.get(toFn)

                # Finds all instances where both column values are 1 (this indicates the path/curve is traversed)
                connection_value = len(real_data[(real_data[outputFn_name] == 1) & (real_data[toFn_name] == 1)])

                # Updates the number of times this path is traversed.
                connections.update({connection_default: connection_value})

        # If the dataframe uses connection_names for the column names.
        elif column_type == "connections":
            for connection_name in connections:
                connection_value = len(real_data[(real_data[connection_name] == 1)])
                connections.update({connection_name: connection_value})

        return connections

    def highlight_data(self,
                       data: pd.DataFrame,
                       column_type: str = "functions",
                       ax: Axes | None = None) -> Axes:
        """
        Highlights the connections of all bezier curves which data instances traverse.
        The color of the connection indicates the intensity of its usage.

        :param data: A pandas dataframe where the columns are function names and rows are instances.
            The values of each column should be 0 (absent) or 1 (present)

        :param column_type: Lets the program know if the user is using the function names, or connection names as the
            column names in the given dataframe.

        :param appearance: Determines the appearance the paths will take on when highlighted. "Pure" is for pure
            color. "Traced" is similar to pure color, but traced in a black outline. "Expand" will have a black line,
            but the outline of this black line will be the highlighted color, and will be wider or narrower depending on
            how much that path is traversed.

        :return: None. A highlighted FRAM model.
        """

        # Makes new figure without the Bezier curves being produced.

        connections = self._count_real_data_connections(real_data=data, column_type=column_type)

        return self.visualizer.generate(self._function_data, self._connection_data, real_connections=connections, ax=ax)

