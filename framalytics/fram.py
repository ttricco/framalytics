from FRAM_Visualizer import *

class FRAM:

    def __init__(self, filename):
        self.filename = filename  # Name of ".xfmv" file.

        fram_data = parse_xfmv(filename)  # Gets all information from .xfmv file

        self.function_data = fram_data[0]  # Function information (Hexagon nodes)
        self.input_data = fram_data[1]  # Input information for input aspect of a function
        self.aspect_data = fram_data[2]  # Aspect connection data (bezier curves)

        self.fram_model = None  # Stores the default FRAM model for alterations before displaying.

        self.given_data = None  # Given data from to user to run through the FRAM (Not implemented)

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
        print(self.functions)
        return self.functions

    def find_function(self, id=None, name=None):
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


if __name__ == "__main__":
    main()


