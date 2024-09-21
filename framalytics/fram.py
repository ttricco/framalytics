from .FRAM_Visualizer import *
from .xfmv_parser import parse_xfmv
import pandas as pd


class FRAM:

    def __init__(self, filename):
        """
        Initializer for the FRAM class. This focuses on reading and storing all data from a given .xfmv file.
        Additionally, it is also used to call methods and functions from the FRAM_Visualizer class.

        :param filename: The name of the .xfmv file being used.
        """
        self.filename = filename  # Name of ".xfmv" file.

        fram_data = parse_xfmv(filename)  # Gets all information from the .xfmv file

        self._function_data = fram_data[0]  # Function information (Hexagon nodes)
        self._aspect_data = fram_data[2]  # Aspect connection data (bezier curves)

        self.visualizer = Visualizer()

        self.given_data = None  # Given data from to user to run through the FRAM (Not implemented, pandas?)

        self.functions_by_id = {}  # Stores all functions in a dictionary. IDNr is the key, IDName is the value.
        self.functions_by_name = {}  # Stores all functions in a dictionary. IDName is the key, IDNr is the value.
        self.connections = {}  # Stores the connections between two aspects and the number of times it's traversed.

        self.connections_list = []  # Stores all connection names
        self.function_list = []  # Stores all function names

        for index, row in self._function_data.iterrows():
            self.functions_by_id.update({int(row.IDNr): row.IDName})
            self.functions_by_name.update({row.IDName: int(row.IDNr)})
            self.function_list.append(row.IDName)

        # Each list store the designated data of all connections. Each index stores the data of a particular connection.
        # For example, index 0 stores all the data of connection 1 over all 4 lists.
        all_fromFn = []
        all_toFn = []
        all_toAspect = []
        all_names = []

        for index, row in self._aspect_data.iterrows():
            self.connections.update({row.Name: 0})
            self.connections_list.append(row.Name)

            # Parses the data so that the desired data of each connection goes to the designated list.
            parsed_connection = row.Name.split("|")
            all_fromFn.append(int(parsed_connection[0]))
            all_names.append(parsed_connection[1])
            all_toFn.append(int(parsed_connection[2]))
            all_toAspect.append(parsed_connection[3])

        # Generates the connections dataframe using the parsed data.
        connection_dataframe = {'fromFn': all_fromFn, "toFn": all_toFn, "toAspect": all_toAspect, "Name": all_names}
        self.connection_dataframe = pd.DataFrame(data=connection_dataframe)



    def get_function_metadata(self):
        """
        Returns the function data of the FRAM file.

        :return: A list of function data. Each index is a different function
        """

        return self._function_data

    def get_aspect_data(self):
        """
        Returns the aspect connection data (Bezier curves) of the FRAM file

        :return: A list of aspect connection data. Each index is a different connection between two aspects.
        """

        return self._aspect_data

    def get_functions(self):
        """
        Returns the dictionary of functions in which the keys are the functionID's and the values
        are the function names.

        :return: A dictionary of functions (keys = ID, values = name).
        """
        return self.functions_by_id

    def get_connections(self):
        """
        Returns a pandas dataframe which consists of all the connections. Each instance/row is a connection and the
        data is broken down into 4 columns. (fromFn, toFn, toAspect, Name).

        :return: A pandas dataframe consisting of all connections.
        """

        return self.connection_dataframe

    def number_of_edges(self):
        """
        Returns the number of edges (connections) in a FRAM model.

        :return: The number of edges (connections/lines) in a FRAM model.
        """
        # Gets all the connection (key,value) pairs in the connections/edges dictionary as a list. Calls "len" to get
        # the total number of edges.
        number_of_edges = len(self.connections.items())

        return number_of_edges

    def number_of_functions(self):
        """
        Returns the number of functions (Hexagon nodes) in a FRAM model.

        :return: The total number of features in a FRAM model.
        """

        number_of_functions = len(self.functions_by_id.items())
        return number_of_functions

    def print_connections(self):
        """
        Prints the dictionary (key,value) items which are the connections of a FRAM model. The key is the name of a
        connection, while the value is the number of times that connection has been traversed if data was integrated.

        :return: None. Prints all connection names and associated traversal value (initially zero).
        """
        for connection in self.connections.items():
            print(connection)

    def print_functions(self):
        """
        Prints the dictionary (key,value) items which are the functions of a FRAM model. The key is the FunctionID of
        the corresponding function, while the value is the name of the function.

        :return: None. Prints all functions, row by row.
        """

        for function in self.functions_by_id.items():
            print(function)

    def get_function_id(self, name=None):
        """
        Given the functions name, returns the corresponding functions ID.

        :param name: The exact name of the function the user wants the ID for.

        :return: The FunctionID that corresponds to the given function name.
        """
        if isinstance(name, str) == False:
            raise Exception("Invalid input. A string value should be used.")

        function_id = self.functions_by_name.get(name)
        return function_id

    def get_function_name(self, id=None):
        """
        Given the functions ID, returns the corresponding functions name.

        :param id: The ID (integer) of the function we want the name of.

        :return: The name of the function for the corresponding given ID.
        """
        if isinstance(id, int) == False:
            raise Exception("Invalid input. A integer value should be used.")

        function_name = self.functions_by_id.get(id)
        return function_name

    def get_function_inputs(self, function=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as inputs to the input aspect
        of the desired function.

        :param function: The ID (integer) or name (string) of the desired function.
        :return: A dictionary consisting of the functions that serve as inputs to the input aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.
        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)

        # If the function value is an integer. We consider that the value is the function ID and use it accordingly.
        elif isinstance(function, int):
            id = function

        # Otherwise, all other value types are considered invalid and an error/exception is raised.
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_inputs = {}  # This will store all the functions inputs in a dictionary {key=id, value = name}

        # For every connection, we separate it into 4 parts. [output_function, name, to_function(input), aspect]
        for index, row in all_connections.iterrows():
            name = row.Name
            outputfn = int(row.fromFn)  # Stored ID and user given ID are integers.
            tofn = int(row.toFn)  # Stored ID and user given ID are integers.
            aspect = row.toAspect

        # If the connection links to the input aspect of the desired function, add the output_function id and name
        # to the dictionary of inputs.
            if (tofn == id) and (aspect == "I"):
                outputfn_name = self.get_function_name(outputfn)
                function_inputs.update({outputfn: outputfn_name})

        return function_inputs

    def get_function_outputs(self, function=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that use the output aspect of the desired
        function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that use the desired functions output aspect.
        """

        all_connections = self.get_connections()  # Gets all connections

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)

        # If the function value is an integer. We consider that the value is the function ID and use it accordingly.
        elif isinstance(function, int):
            id = function

        # Otherwise, all other value types are considered invalid and an error/exception is raised.
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        # This will store all the functions that use the desired function outputs aspect in a dictionary.
        # {key=id, value = name}
        function_outputs = {}

        # For every connection, we separate it into 4 parts. [output_function, name, to_function(input), aspect]
        for index, row in all_connections.iterrows():
            name = row.Name
            outputfn = int(row.fromFn)  # Stored ID and user given ID are integers.
            tofn = int(row.toFn)  # Stored ID and user given ID are integers.
            aspect = row.toAspect

            # If the connection uses the desired function as the output fn (means it uses it's output aspect), we
            # add it to the output_functions dictionary.
            if (outputfn == id):
                tofn_name = self.get_function_name(tofn)
                function_outputs.update({tofn: tofn_name})

        return function_outputs

    def get_function_preconditions(self, function=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as preconditions to the
        precondition aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as preconditions to
            the precondition aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)

        # If the function value is an integer. We consider that the value is the function ID and use it accordingly.
        elif isinstance(function, int):
            id = function

        # Otherwise, all other value types are considered invalid and an error/exception is raised.
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        # This will store all the functions preconditions in a dictionary {key=id, value = name}
        function_preconditions = {}

        for index, row in all_connections.iterrows():
            name = row.Name
            outputfn = int(row.fromFn)  # Stored ID and user given ID are integers.
            tofn = int(row.toFn)  # Stored ID and user given ID are integers.
            aspect = row.toAspect

            if (tofn == id) and (aspect == "P"):
                outputfn_name = self.get_function_name(outputfn)
                function_preconditions.update({outputfn: outputfn_name})

        return function_preconditions

    def get_function_resources(self, function=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as resources to the
        resource aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as resources to the resource aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)

        # If the function value is an integer. We consider that the value is the function ID and use it accordingly.
        elif isinstance(function, int):
            id = function

        # Otherwise, all other value types are considered invalid and an error/exception is raised.
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_resources = {}  # This will store all the functions resources in a dictionary {key=id, value = name}

        for index, row in all_connections.iterrows():
            name = row.Name
            outputfn = int(row.fromFn)  # Stored ID and user given ID are integers.
            tofn = int(row.toFn)  # Stored ID and user given ID are integers.
            aspect = row.toAspect

            if (tofn == id) and (aspect == "R"):
                outputfn_name = self.get_function_name(outputfn)
                function_resources.update({outputfn: outputfn_name})

        return function_resources

    def get_function_controls(self, function=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as controls to the
        time aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as controls to the control aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)

        # If the function value is an integer. We consider that the value is the function ID and use it accordingly.
        elif isinstance(function, int):
            id = function

        # Otherwise, all other value types are considered invalid and an error/exception is raised.
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_controls = {}  # This will store all the functions controls in a dictionary {key=id, value = name}

        for index, row in all_connections.iterrows():
            name = row.Name
            outputfn = int(row.fromFn)  # Stored ID and user given ID are integers.
            tofn = int(row.toFn)  # Stored ID and user given ID are integers.
            aspect = row.toAspect

            if (tofn == id) and (aspect == "C"):
                outputfn_name = self.get_function_name(outputfn)
                function_controls.update({outputfn: outputfn_name})

        return function_controls

    def get_function_times(self, function=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as times to the
        time aspect of the desired function.

        :param function: The ID (integer) or name (String) of the desired function.
        :return: A dictionary consisting of the functions that serve as times to the time aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # ID is used to get all functions that act as inputs for the given function ID or name, we use the functions ID.

        # If the function value given is a string. We consider the value is the function name and get the associated ID.
        if isinstance(function, str):
            id = self.get_function_id(function)

        # If the function value is an integer. We consider that the value is the function ID and use it accordingly.
        elif isinstance(function, int):
            id = function

        # Otherwise, all other value types are considered invalid and an error/exception is raised.
        else:
            raise Exception("Invalid input. A function ID (integer) or function name (string) is required")

        function_times = {}  # This will store all the functions times in a dictionary {key=id, value = name}

        for index, row in all_connections.iterrows():
            name = row.Name
            outputfn = int(row.fromFn)  # Stored ID and user given ID are integers.
            tofn = int(row.toFn)  # Stored ID and user given ID are integers.
            aspect = row.toAspect

            if (tofn == id) and (aspect == "T"):
                outputfn_name = self.get_function_name(outputfn)
                function_times.update({outputfn: outputfn_name})

        return function_times

    def visualize(self, ax=None):
        """
        Visualizes the model by calling to the Visualizer class of FRAM_Visualizer.py. This generates the default model.

        :param backend: The backend matplotlib will use to display the model through the Visualizer class.

        :return: None. Generates the FRAM model.
        """

        return self.visualizer.generate(self._function_data, self._aspect_data, ax=ax)

    def display(self):
        """
        Simply displays the current FRAM Model plot.

        :return: None. Displays the FRAM plot.
        """
        plt.show()

    def highlight_function_outputs(self, functionID):
        """
        Highlights the outputs of a function.

        :param functionID: Integer value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """
        if isinstance(functionID, int) == False:
            raise Exception("Invalid input. A integer value should be used.")

        self.visualizer.generate_function_output_paths(self._aspect_data, functionID)

    def highlight_full_path_from_function(self, functionID):
        """
        Highlights all the paths that are connected to a starting function.

        :param functionID: Integer value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """
        if isinstance(functionID, int) == False:
            raise Exception("Invalid input. A integer value should be used.")

        self.visualizer.generate_full_path_from_function(self._aspect_data, functionID)

    def highlight_data(self, data, column_type="functions", appearance="Pure"):
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
        plt.close(1)  # Closes and clears old figure

        # Makes new figure without the Bezier curves being produced.
        self.visualizer.generate(self._function_data, self._aspect_data, False)

        total_instances = len(data)  # Total number of rows / instances from the dataframe.

        column_type = column_type.lower()
        # If the dataframe uses function names for the column names.
        if column_type == "functions":

            for i in self.connections:
                # Stores current connection name
                connection_default = i

                # Splits connection to get information
                connection = i.split("|")

                # Get output and input function ID's
                outputFn = int(connection[0])
                toFn = int(connection[2])

                # Stores the names of the functions.
                outputFn_name = self.functions_by_id.get(outputFn)
                toFn_name = self.functions_by_id.get(toFn)

                # Finds all instances where both column values are 1 (this indicates the path/curve is traversed)
                connection_value = len(data[(data[outputFn_name] == 1) & (data[toFn_name] == 1)])

                # Updates the number of times this path is traversed.
                self.connections.update({connection_default: connection_value})

        # If the dataframe uses connection_names for the column names.
        elif column_type == "connections":
            for connection_name in self.connections:
                connection_value = len(data[(data[connection_name] == 1)])
                self.connections.update({connection_name: connection_value})

    # Begins updating the FRAM model so that connections are color coded based on the intensity of the connections use.
        for connection in self.connections:
            value = self.connections.get(connection)

            color = "grey"
            if (value == 0):
                color = "grey"

            elif (value <= int(total_instances * 0.25)):
                color = "green"

            elif (value <= int(total_instances * 0.5)):
                color = "yellow"

            elif (value <= int(total_instances * 0.75)):
                color = "orange"

            elif (value <= total_instances):
                color = "red"

            for index, row in self._aspect_data.iterrows():
                if (row.Name == connection):
                    self.visualizer.bezier_curve_single(row.Curve, color, appearance, (value / total_instances) * 4)

    def list_of_connections(self):
        """
        Prints a list in which all indexes are also a list of two values. These values are the function names
        of a connection. For example: [[OutputFn_name, toFn_name], OutputFn_name, toFn_name]].

        :return: None. Prints all connections, in which the values are function names.
        """
        all_connections = []
        for i in self.get_connections():
            # Stores current connection name
            connection_default = i

            # Splits connection to get information
            connection = i.split("|")

            # Get output and input function ID's
            outputFn = int(connection[0])
            toFn = int(connection[2])

            # Stores the names of the functions.
            outputFn_name = self.functions_by_id.get(outputFn)
            toFn_name = self.functions_by_id.get(toFn)

            all_connections.append([outputFn_name, toFn_name])

        print(all_connections)
