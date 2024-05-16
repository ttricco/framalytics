from FRAM_Visualizer import *
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

        self.function_data = fram_data[0]  # Function information (Hexagon nodes)
        self.input_data = fram_data[1]  # Input information for input aspect of a function
        self._aspect_data = fram_data[2]  # Aspect connection data (bezier curves)

        self.fram_model = None  # Stores the default FRAM model for alterations before displaying.

        self.given_data = None  # Given data from to user to run through the FRAM (Not implemented, pandas?)

        self.functions_by_id = {}  # Stores all functions in a dictionary. IDNr is the key, IDName is the value.
        self.functions_by_name = {}  # Stores all functions in a dictionary. IDName is the key, IDNr is the value.
        self.connections = {}  # Stores the connections between two aspects and the number of times it's traversed.

        for index, row in self.function_data.iterrows():
            self.functions_by_id.update({row.IDNr: row.IDName})
            self.functions_by_name.update({row.IDName: row.IDNr})

        for index, row in self._aspect_data.iterrows():
            self.connections.update({row.Name: 0})


    def get_function_data(self):
        """
        Returns the function data of the FRAM file.

        :return: A list of function data. Each index is a different function
        """

        return self.function_data

    def get_input_data(self):
        """
        Returns the input data of a function (input aspect) of the FRAM file.

        :return: A list of input data. Each index is a different functions input.
        """

        return self.input_data

    def get_aspect_data(self):
        """
        Returns the aspect connection data (Bezier curves) of the FRAM file

        :return: A list of aspect connection data. Each index is a different connection between two aspects.
        """

        return self._aspect_data

    def get_functions(self):
        """
        Prints and returns the dictionary of functions inwhich the keys are the functionID's and the values
        are the function names.

        :return: A dictionary of functions (keys = ID, values = name).
        """
        print(self.functions_by_id)
        return self.functions_by_id

    def get_connections(self):
        """
        Returns a list of all connections and the number of times that connection has been traversed.

        :return: Dictionary of aspect connections (bezier curves).
        """
        for connection in self.connections.items():
            print(connection)
        return self.connections


    def find_function(self, id=None, name=None):
        """
        Returns a functionID or name depending on the parameter given.

        If the id of a function is given, the name is returned.
        If the name of a function is given, the id is returned.

        Only one of two parameters should be given, if both are given, the function returns nothing.

        :param id: The IDNr of a function
        :param name: The name of a function.

        :return: The IDNr or Name of a function depending on which parameter is given.

        """
        if ((id != None) and (name != None)):
            print("Only one of two parameters should be used.")
            return None

        if ((id == None) and (name == None)):
            print("One parameter needs to be used.")
            return None

        if (id != None):
            function_name = self.functions_by_id.get(id)
            print(id,": ",function_name)
            return function_name

        if (name != None):
            functionID = self.functions_by_name.get(name)
            print(name,": ",functionID)
            return functionID



    def visualize(self,backend=None):
        """Visualizes the model"""
        self.fram_model = Visualizer(backend=backend, dpi=150)
        self.fram_model.generate(self.function_data, self.input_data, self._aspect_data)

    def display(self):
        plt.show()


    def show_function_outputs(self, functionID):
        """
        Highlights the outputs of a function.

        :param functionID: String value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """

        self.fram_model.generate_function_output_paths(self._aspect_data, functionID)

    def show_full_path_from_function(self, functionID):
        """
        Highlights all the paths that are connected to a starting function.

        :param functionID: String value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """

        self.fram_model.generate_full_path_from_function(self._aspect_data, functionID)


    def generate_connection_traversal_count(self, output_function):
        """
        Generates the number of times each connection is traversed.

        :param output_function: FunctionID of starting function

        :return: None.
        """

        functions_in_path = []
        already_pathed = []
        current_function = output_function

        for index, row in self._aspect_data.iterrows():
            # In the case the instance does not store the output and toFn Values, they seem to be stored in the name.
            if ((row.outputFn == None) and (row.toFn == None)):
                name_split = row.Name.split("|")  # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)
                if (name_split[0] == current_function):
                    functions_in_path.append(name_split[2])

                    connection_count = self.connections.get(row.Name)
                    connection_count += 1
                    self.connections.update({row.Name: connection_count})


            # For our Stroke Care System, this is used.
            else:
                if (row.outputFn == current_function):
                    functions_in_path.append(row.toFn)

                    connection_count = self.connections.get(row.Name)
                    connection_count += 1
                    self.connections.update({row.Name: connection_count})

        # Add this function to the path link, so that we don't repeat paths.
        already_pathed.append(current_function)

        # While all paths have not been searched
        while (len(functions_in_path) != 0):
            current_function = functions_in_path.pop()
            if (current_function in already_pathed):
                continue

            for index, row in self._aspect_data.iterrows():
                if ((row.outputFn == None) and (row.toFn == None)):
                    name_split = row.Name.split("|")  # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)
                    if (name_split[0] == current_function):
                        functions_in_path.append(name_split[2])

                        connection_count = self.connections.get(row.Name)
                        connection_count += 1
                        self.connections.update({row.Name: connection_count})

                    # For our Stroke Care System, this is used.
                else:
                    if (row.outputFn == current_function):
                        functions_in_path.append(row.toFn)

                        connection_count = self.connections.get(row.Name)
                        connection_count += 1
                        self.connections.update({row.Name: connection_count})

            already_pathed.append(current_function)

            self.connections = dict(sorted(self.connections.items(), key=lambda item: item[1]))



    def highlight_data(self, data):
        """
        Highlights the connections of all bezier curves which data instances traverse.
        The color of the connection indicates the intensity of its usage.

        :param data: A dataframe where the columns are function names, and rows are instances.
        The values of each column should be 0 (absent) or 1 (present)

        :return: None. A highlighted FRAM model.
        """
        total_instances = len(data)  # Total number of rows / instances from the dataframe.

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

            # Begins iterating through the dataframe to find the number of times a path is traversed
            # This is based on if both functions in an instance have a value of 1.
            for row in range(len(data[outputFn_name])):
                outputFn_data_value = data[outputFn_name][row]
                toFn_data_value = data[toFn_name][row]

                if ((outputFn_data_value == 1) and (toFn_data_value == 1)):
                    connection_value = self.connections.get(connection_default)
                    connection_value += 1
                    self.connections.update({connection_default: connection_value})

        # Begins updating the FRAM model so that connections are color coded based on the intensity of the connections use.
        for connection in self.connections:
            value = self.connections.get(connection)

            color = "grey"
            if(value == 0):
                color = "grey"

            elif(value <= int(total_instances*0.25)):
                color = "green"

            elif(value <= int(total_instances*0.5)):
                color = "yellow"

            elif(value <= int(total_instances*0.75)):
                color = "orange"

            elif(value <= total_instances):
                color = "red"

            for index, row in self._aspect_data.iterrows():
                if (row.Name == connection):
                    self.fram_model.bezier_curve_single(row.Curve,color)




def main():
    # Initializes the Fram model by giving the associated ".xfmv" file.

    #test = FRAM("FRAM model-Stroke care system.xfmv")
    test = FRAM("Cup Noodles.xfmv")
    #test = FRAM("prepare_work_example.xfmv")
    #test = FRAM("leave_harbor_example.xfmv")

    # Shows this is a FRAM object as desired
    # print(test)

    # Shows that the fram.py displays the FRAM model by calling the functions of the FRAM_Visualizer.py

    test.visualize("WebAgg")  # Displays the default FRAM model as desired.

    #test.show_function_outputs("0")  # Shows the output connections of a specific function based on the function IDNr.
    test.show_full_path_from_function("1")  # Shows the entire path associated with a starting function (using IDNr).
    #test.get_connections()  # Shows all connections between aspects and the number of times it's been traversed.

    #print("\n\n\n\n")

    #test.generate_connection_traversal_count("1") # Shows how many times a connection is traversed.
    #test.get_connections()
    test.display()  # Displays the model.

    # Calls for testing functions

    #test.get_functions()
    # test.find_function(id="1")
    # test.find_function(name="Transport the patient by ambulance")
    # print(test.get_function_data())
    # print(test.get_input_data())
    # print(test.get_aspect_data())

    #test.highlight_data(data)
    #test.display()


if __name__ == "__main__":
    main()


