from FRAM_Visualizer import *

class FRAM:

    def __init__(self, filename):
        """
        Initializer for the FRAM class. This focuses on reading and storing all data from a given .xfmv file.
        Additionally, it is also used to call methods and functions from the FRAM_Visualizer class.

        :param filename: The name of the .xfmv file being used.
        """
        self.filename = filename  # Name of ".xfmv" file.
        self.backend = None

        fram_data = parse_xfmv(filename)  # Gets all information from the .xfmv file

        self._function_data = fram_data[0]  # Function information (Hexagon nodes)
        self._input_data = fram_data[1]  # Input information for input aspect of a function
        self._aspect_data = fram_data[2]  # Aspect connection data (bezier curves)

        self.fram_model = None  # Stores the default FRAM model for alterations before displaying.

        self.given_data = None  # Given data from to user to run through the FRAM (Not implemented, pandas?)

        self.functions_by_id = {}  # Stores all functions in a dictionary. IDNr is the key, IDName is the value.
        self.functions_by_name = {}  # Stores all functions in a dictionary. IDName is the key, IDNr is the value.
        self.connections = {}  # Stores the connections between two aspects and the number of times it's traversed.

        self.connections_list = []  # Stores all connection names
        self.function_list = []  # Stores all function names

        for index, row in self._function_data.iterrows():
            self.functions_by_id.update({row.IDNr: row.IDName})
            self.functions_by_name.update({row.IDName: row.IDNr})
            self.function_list.append(row.IDName)

        for index, row in self._aspect_data.iterrows():
            self.connections.update({row.Name: 0})
            self.connections_list.append(row.Name)


    def get_function_metadata(self):
        """
        Returns the function data of the FRAM file.

        :return: A list of function data. Each index is a different function
        """

        return self._function_data

    def get_input_data(self):
        """
        Returns the input data of a function (input aspect) of the FRAM file.

        :return: A list of input data. Each index is a different functions input.
        """

        return self._input_data

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
        Returns a list of all connections and the number of times that connection has been traversed.

        :return: Dictionary of aspect connections (bezier curves).
        """

        return self.connections

    def number_of_edges(self):
        """
        Prints and returns the number of edges (connections) in a FRAM model.

        :return: The number of edges (connections/lines) in a FRAM model.
        """
        # Gets all the connection (key,value) pairs in the connections/edges dictionary as a list. Calls "len" to get
        # the total number of edges.
        number_of_edges = len(self.connections.items())

        print(number_of_edges)
        return number_of_edges

    def number_of_functions(self):
        """
        Prints and returns the number of functions (Hexagon nodes) in a FRAM model.

        :return: The total number of features in a FRAM model.
        """

        number_of_functions = len(self.functions_by_id.items())
        print(number_of_functions)
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

        function_id = self.functions_by_name.get(name)
        #print(name, ": ", function_id)
        return function_id

    def get_function_name(self, id=None):
        """
        Given the functions ID, returns the corresponding functions name.

        :param id: The ID of the function we want the name of.

        :return: The name of the function for the corresponding given ID.
        """

        function_name = self.functions_by_id.get(id)
        #print(id, ": ", function_name)
        return function_name

    def get_function_inputs(self, name=None, id=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as inputs to the input aspect
        of the desired function.

        :param name: The name of the desired function we want the inputs for. (Used to find the function ID)
        :param id: The id of the desired function we want the inputs for.
        :return: A dictionary consisting of the functions that serve as inputs to the input aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # If the id was not given for the function, find it using the name.
        if id == None:
            id = self.get_function_id(name)

        function_inputs = {}  # This will store all the functions inputs in a dictionary {key=id, value = name}

        # For every connection, we separate it into 4 parts. [output_function, name, to_function(input), aspect]

        for connection in all_connections.keys():
            seperated_connection = connection.split("|")
            outputfn = seperated_connection[0]
            tofn = seperated_connection[2]
            aspect = seperated_connection[3]

        # If the connection links to the input aspect of the desired function, add the output_function id and name
        # to the dictionary of inputs.
            if((tofn == id) and (aspect == "I")):
                outputfn_name = self.get_function_name(outputfn)
                function_inputs.update({outputfn:outputfn_name})

        return function_inputs

    def get_function_outputs(self, name=None, id=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that use the output aspect of the desired
        function.

        :param name: The name of the desired function we want the outputs for. (Used to find the function ID)
        :param id: The id of the desired function we want the outputs for.
        :return: A dictionary consisting of the functions that use the desired functions output aspect.
        """

        all_connections = self.get_connections()  # Gets all connections

        # If the id was not given for the function, find it using the name.
        if id == None:
            id = self.get_function_id(name)

        # This will store all the functions that use the desired function outputs aspect in a dictionary.
        # {key=id, value = name}
        function_outputs = {}

        # For every connection, we separate it into 4 parts. [output_function, name, to_function(input), aspect]
        for connection in all_connections.keys():
            seperated_connection = connection.split("|")
            outputfn = seperated_connection[0]
            tofn = seperated_connection[2]
            aspect = seperated_connection[3]

            # If the connection uses the desired function as the output fn (means it uses it's output aspect), we
            # add it to the output_functions dictionary.
            if (outputfn == id):
                tofn_name = self.get_function_name(tofn)
                function_outputs.update({tofn: tofn_name})

        return function_outputs

    def get_function_preconditions(self, name=None, id=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as preconditions to the
        precondition aspect of the desired function.

        :param name: The name of the desired function we want the preconditions for. (Used to find the function ID)
        :param id: The id of the desired function we want the preconditions for.
        :return: A dictionary consisting of the functions that serve as preconditions to the precondition aspect of the
        function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # If the id was not given for the function, find it using the name.
        if id == None:
            id = self.get_function_id(name)

        # This will store all the functions preconditions in a dictionary {key=id, value = name}
        function_preconditions = {}

        for connection in all_connections.keys():
            seperated_connection = connection.split("|")
            outputfn = seperated_connection[0]
            tofn = seperated_connection[2]
            aspect = seperated_connection[3]

            if((tofn == id) and (aspect == "P")):
                outputfn_name = self.get_function_name(outputfn)
                function_preconditions.update({outputfn:outputfn_name})

        return function_preconditions

    def get_function_resources(self, name=None, id=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as resources to the
        resource aspect of the desired function.

        :param name: The name of the desired function we want the resources for. (Used to find the function ID)
        :param id: The id of the desired function we want the resources for.
        :return: A dictionary consisting of the functions that serve as resources to the resource aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # If the id was not given for the function, find it using the name.
        if id == None:
            id = self.get_function_id(name)

        function_resources = {}  # This will store all the functions resources in a dictionary {key=id, value = name}
        for connection in all_connections.keys():
            seperated_connection = connection.split("|")
            outputfn = seperated_connection[0]
            tofn = seperated_connection[2]
            aspect = seperated_connection[3]

            if((tofn == id) and (aspect == "R")):
                outputfn_name = self.get_function_name(outputfn)
                function_resources.update({outputfn:outputfn_name})

        return function_resources

    def get_function_controls(self, name=None, id=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as controls to the
        time aspect of the desired function.

        :param name: The name of the desired function we want the controls for. (Used to find the function ID)
        :param id: The id of the desired function we want the controls for.
        :return: A dictionary consisting of the functions that serve as controls to the control aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # If the id was not given for the function, find it using the name.
        if id == None:
            id = self.get_function_id(name)

        function_controls = {}  # This will store all the functions controls in a dictionary {key=id, value = name}
        for connection in all_connections.keys():
            seperated_connection = connection.split("|")
            outputfn = seperated_connection[0]
            tofn = seperated_connection[2]
            aspect = seperated_connection[3]

            if((tofn == id) and (aspect == "C")):
                outputfn_name = self.get_function_name(outputfn)
                function_controls.update({outputfn:outputfn_name})

        return function_controls

    def get_function_times(self, name=None, id=None):
        """
        Gets a dictionary of key/value pairs that consist of the functions that serve as times to the
        time aspect of the desired function.

        :param name: The name of the desired function we want the times for. (Used to find the function ID)
        :param id: The id of the desired function we want the times for.
        :return: A dictionary consisting of the functions that serve as times to the time aspect of the function.
        """

        all_connections = self.get_connections()  # Gets all connections

        # If the id was not given for the function, find it using the name.
        if id == None:
            id = self.get_function_id(name)

        function_times = {}  # This will store all the functions times in a dictionary {key=id, value = name}
        for connection in all_connections.keys():
            seperated_connection = connection.split("|")
            outputfn = seperated_connection[0]
            tofn = seperated_connection[2]
            aspect = seperated_connection[3]

            if((tofn == id) and (aspect == "T")):
                outputfn_name = self.get_function_name(outputfn)
                function_times.update({outputfn:outputfn_name})

        return function_times

    def visualize(self,backend=None):
        """
        Visualizes the model by calling to the Visualizer class of FRAM_Visualizer.py. This generates the default model.

        :return: None. Generates the FRAM model.
        """

        self.backend = backend
        self.fram_model = Visualizer(backend=backend, dpi=150)
        self.fram_model.generate(self._function_data, self._input_data, self._aspect_data)

    def display(self):
        """
        Simply displays the current FRAM Model plot.

        :return: None. Displays the FRAM plot.
        """
        plt.show()

    def highlight_function_outputs(self, functionID):
        """
        Highlights the outputs of a function.

        :param functionID: String value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """

        self.fram_model.generate_function_output_paths(self._aspect_data, functionID)

    def highlight_full_path_from_function(self, functionID):
        """
        Highlights all the paths that are connected to a starting function.

        :param functionID: String value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """

        self.fram_model.generate_full_path_from_function(self._aspect_data, functionID)

    def highlight_data(self, data, column_type= "functions", appearance="Pure"):
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
        plt.close(1) # Closes and clears old figure

        # Makes new figure without the Bezier curves being produced.
        self.fram_model.generate(self._function_data, self._input_data, self._aspect_data, False)

        total_instances = len(data)  # Total number of rows / instances from the dataframe.

        column_type = column_type.lower()
        # If the dataframe uses function names for the column names.
        if column_type == "functions":
            for i in self.get_connections():
                # Stores current connection name
                connection_default = i

                # Splits connection to get information
                connection = i.split("|")

                # Get output and input function ID's
                outputFn = connection[0]
                toFn = connection[2]

                # Stores the names of the functions.
                outputFn_name = self.functions_by_id.get(outputFn)
                toFn_name = self.functions_by_id.get(toFn)

                # Finds all instances where both column values are 1 (this indicates the path/curve is traversed)
                connection_value = len(data[(data[outputFn_name] == 1) & (data[toFn_name] == 1)])

                # Updates the number of times this path is traversed.
                self.connections.update({connection_default: connection_value})

        # If the dataframe uses connection_names for the column names.
        elif column_type == "connections":
            for connection_name in self.get_connections():
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
                    self.fram_model.bezier_curve_single(row.Curve, color, appearance, (value/total_instances)*4)

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
            outputFn = connection[0]
            toFn = connection[2]

            # Stores the names of the functions.
            outputFn_name = self.functions_by_id.get(outputFn)
            toFn_name = self.functions_by_id.get(toFn)

            all_connections.append([outputFn_name, toFn_name])

        print(all_connections)


def main():
    # Initializes the Fram model by giving the associated ".xfmv" file.

    test = FRAM("FRAM model-Stroke care system.xfmv")
    #test = FRAM("Cup Noodles.xfmv")
    #test = FRAM("prepare_work_example.xfmv")
    #test = FRAM("leave_harbor_example.xfmv")

    # Shows this is a FRAM object as desired
    # print(test)

    # Shows that the fram.py displays the FRAM model by calling the functions of the FRAM_Visualizer.py

    test.visualize("WebAgg")  # Displays the default FRAM model as desired.

    # test.highlight_function_outputs("57")  # Shows the output connections of a specific function based on the function IDNr.
    # test.highlight_full_path_from_function("57")  # Shows the entire path associated with a starting function (using IDNr).
    # print(test.get_connections())  # Shows all connections between aspects and the number of times it's been traversed.

    # Calls for testing functions

    # test.get_functions()  #Prints and returns a dictionary of all functions (key=FunctionID,value=Function Name)

    # test.number_of_edges()  #Prints and returns the total number of edges/connections/lines/bezier curves.
    # test.number_of_functions()  #Prints and returns the total number of functions.

    # test.print_connections()  #Prints all connections neatly, row by row.
    # test.print_functions()  #Prints all functions neatly, row by row.

    # test.get_function_id(name="Activate a code stroke") #Prints and returns the functionID of a given function name.
    # test.get_function_name(id="57") #Prints and returns the name of a function for the given function ID.

    # print(test.get_function_inputs(name="Do stroke assessment by a care paramedic"))
    # print(test.get_function_outputs(name="Do stroke assessment by a care paramedic"))
    # print(test.get_function_preconditions(name="Receive a call through the dispatch system"))
    # print(test.get_function_resources(name="Receive a call through the dispatch system"))
    # print(test.get_function_controls(name="Transport the patient by ambulance"))
    # print(test.get_function_times(name="To wait until tender"))

    # print(test.get_function_metadata())
    # print(test.get_input_data())
    # print(test.get_aspect_data())

    # print(test.function_list)  # Prints a list of all function names
    # print(test.connections_list)  # Prints a list of all connection names


    #data = pd.read_csv("Insert dataframe.csv or directory to .csv file")
    #test.highlight_data(data,"Functions","Traced")
    #test.display()




if __name__ == "__main__":
    main()


