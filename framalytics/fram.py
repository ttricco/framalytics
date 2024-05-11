from FRAM_Visualizer import *

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
        self.aspect_data = fram_data[2]  # Aspect connection data (bezier curves)

        self.fram_model = None  # Stores the default FRAM model for alterations before displaying.

        self.given_data = None  # Given data from to user to run through the FRAM (Not implemented, pandas?)

        self.functions_by_id = {}  # Stores all functions in a dictionary. IDNr is the key, IDName is the value.
        self.functions_by_name = {}  # Stores all functions in a dictionary. IDName is the key, IDNr is the value.

        for index, row in self.function_data.iterrows():
            self.functions_by_id.update({row.IDNr: row.IDName})
            self.functions_by_name.update({row.IDName: row.IDNr})


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

        return self.aspect_data

    def get_functions(self):
        """
        Prints and returns the dictionary of functions inwhich the keys are the functionID's and the values
        are the function names.

        :return: A dictionary of functions (keys = ID, values = name).
        """
        print(self.functions_by_id)
        return self.functions_by_id

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
        self.fram_model.generate(self.function_data, self.input_data, self.aspect_data)

    def display(self):
        plt.show()


    def show_function_outputs(self, functionID):
        """
        Highlights the outputs of a function.

        :param functionID: String value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """

        self.fram_model.generate_function_output_paths(self.aspect_data, functionID)

    def show_full_path_from_function(self, functionID):
        """
        Highlights all the paths that are connected to a starting function.

        :param functionID: String value of the FunctionID to be used as the starting point.

        :return: None. Highlights paths when the model is displayed.
        """

        self.fram_model.generate_full_path_from_function(self.aspect_data, functionID)



def main():
    test = FRAM("FRAM model-Stroke care system.xfmv")
    #test = FRAM("Cup Noodles.xfmv")
    #test = FRAM("prepare_work_example.xfmv")
    #test = FRAM("leave_harbor_example.xfmv")

    # Does all the work to produce the FRAM visual, and displays it.
    #test.visualize("WebAgg")
    #test.show_function_outputs("1")
    #test.show_full_path_from_function("1")
    #test.display()  # Displays the graph

    # Testing functions

    # test.get_functions()
    # test.find_function(id="1")
    # test.find_function(name="Transport the patient by ambulance")
    # print(test.get_function_data())
    # print(test.get_input_data())
    # print(test.get_aspect_data())


if __name__ == "__main__":
    main()


