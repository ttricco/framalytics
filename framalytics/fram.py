import pandas as pd
from matplotlib.axes import Axes

from .FRAM_Visualizer import Visualizer
from .xfmv_parser import parse_xfmv


class FRAM:
    """
    FRAM objects hold FRAM models.

    FRAM objects can render FRAM models and act as a general interface for
    FRAM models. They can be created by reading FRAM models specified by an
    .xfmv file created by the FRAM Model Visualizer.
    """

    def __init__(self,
                 filename: str):
        """
        Initialize a FRAM object from an .xfmv file.

        Parameters
        ----------
        filename : str
            The name of the .xfmv file to read.

        Examples
        --------
        >>> import framalytics
        >>>
        >>> fram = framalytics.FRAM('my-fram-model.xfmv')
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

    def _get_function_metadata(self) -> pd.DataFrame:
        """
        Returns the function data of the FRAM model.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the raw function data from the .xfmv
            file. Each row is one function.
        """

        return self._function_data

    def _get_connection_data(self) -> pd.DataFrame:
        """
        Returns the aspect connection data of the FRAM model.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the raw connection data from the
            .xfmv file. Each row is one connection between two aspects.
        """

        return self._connection_data

    def get_functions(self) -> dict:
        """
        Returns the dictionary of functions.

        The keys of the dictionary are the function IDs and the values are the
        function names.

        Returns
        -------
        dict
            A dictionary of functions, with (key, value) pairs the (ID, name)
            of each function.
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

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame of all the connections.
        """

        columns = ['outputFn', 'toFn', 'toAspect', 'parsed_name']
        rename = {'outputFn': 'fromFn', 'parsed_name': 'Name'}
        return self._connection_data[columns].rename(columns=rename)

    def number_of_edges(self) -> int:
        """
        Returns the number of connections (edges) in the FRAM model.

        Returns
        -------
        int
            The number of connections (edges) in the FRAM model.
        """

        return len(self._connection_data)

    def number_of_connections(self) -> int:
        """
        Returns the number of connections (edges) in the FRAM model.

        Returns
        -------
        int
            The number of connections (edges) in the FRAM model.
        """

        return self.number_of_edges()

    def number_of_functions(self) -> int:
        """
        Returns the number of functions in the FRAM model.

        Returns
        -------
        int
            The number of functions in the FRAM model.
        """

        number_of_functions = len(self.functions_by_id.items())
        return number_of_functions

    def get_function_id(self,
                        name: str) -> int:
        """
        Return the corresponding function ID given a function name.

        Parameters
        ----------
        name : str
            The exact name of a function.

        Returns
        -------
        int
            The function ID that corresponds to the given function name.
        """
        if not isinstance(name, str):
            raise ValueError("The string function name should be used.")

        function_id = self.functions_by_name.get(name)

        if function_id is None:
            raise Exception("No such function name exists.")

        return function_id

    def get_function_name(self,
                          id: int) -> str:
        """
        Return the corresponding function name given a function ID.

        Parameters
        ----------
        id : int
            The ID (integer) of a function.

        Returns
        -------
        str
            The function name that corresponds to the given function ID.
        """
        if not isinstance(id, int):
            raise ValueError("The integer function ID should be used.")

        function_name = self.functions_by_id.get(id)

        if function_name is None:
            raise ValueError("No such function ID exists.")

        return function_name

    def get_function_inputs(self,
                            function: str | int) -> dict:
        """
        Get all functions connected to the given function's input aspect.

        A dictionary is returned where the keys/values are function IDs/names
        of all functions that connect to the input aspect of the given
        function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.

        Returns
        -------
        dict
            A dictionary consisting of the functions that connect to the input
            aspect of the specified function.
        """

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise ValueError("A function ID or name is required.")

        function_inputs = {}  # {key=id, value=name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "I":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_inputs.update({row['outputFn']: outputfn_name})

        return function_inputs

    def get_function_outputs(self,
                             function: str | int) -> dict:
        """
        Get all functions connected to the given function's output aspect.

        A dictionary is returned where the keys/values are function IDs/names
        of all functions that connect to the output aspect of the given
        function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.

        Returns
        -------
        dict
            A dictionary consisting of the functions that connect to the output
            aspect of the specified function.
        """

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise ValueError("A function ID or name is required.")

        function_outputs = {}  # {key=id, value=name}

        for index, row in self._connection_data.iterrows():
            if row['outputFn'] == id:
                tofn_name = self.get_function_name(row['toFn'])
                function_outputs.update({row['toFn']: tofn_name})

        return function_outputs

    def get_function_preconditions(self,
                                   function: str | int) -> dict:
        """
        Get all functions connected to the given function's precondition
        aspect.

        A dictionary is returned where the keys/values are function IDs/names
        of all functions that connect to the precondition aspect of the given
        function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.

        Returns
        -------
        dict
            A dictionary consisting of the functions that connect to the
            precondition aspect of the specified function.
        """

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise ValueError("A function ID or name is required.")

        function_preconditions = {}  # {key=id, value=name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "P":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_preconditions.update({row['outputFn']: outputfn_name})

        return function_preconditions

    def get_function_resources(self,
                               function: str | int) -> dict:
        """
        Get all functions connected to the given function's resource aspect.

        A dictionary is returned where the keys/values are function IDs/names
        of all functions that connect to the resource aspect of the given
        function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.

        Returns
        -------
        dict
            A dictionary consisting of the functions that connect to the
            resource aspect of the specified function.
        """

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise ValueError("A function ID or name is required.")

        function_resources = {}  # {key=id, value=name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "R":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_resources.update({row['outputFn']: outputfn_name})

        return function_resources

    def get_function_controls(self,
                              function: str | int) -> dict:
        """
        Get all functions connected to the given function's controls aspect.

        A dictionary is returned where the keys/values are function IDs/names
        of all functions that connect to the control aspect of the given
        function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.

        Returns
        -------
        dict
            A dictionary consisting of the functions that connect to the
            control aspect of the specified function.
        """

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise ValueError("A function ID or name is required.")

        function_controls = {}  # {key=id, value=name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "C":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_controls.update({row['outputFn']: outputfn_name})

        return function_controls

    def get_function_times(self,
                           function: str | int) -> dict:
        """
        Get all functions connected to the given function's time aspect.

        A dictionary is returned where the keys/values are function IDs/names
        of all functions that connect to the time aspect of the given function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.

        Returns
        -------
        dict
            A dictionary consisting of the functions that connect to the
            time aspect of the specified function.
        """

        if isinstance(function, str):
            id = self.get_function_id(function)
        elif isinstance(function, int):
            id = function
        else:
            raise ValueError("A function ID or name is required.")

        function_times = {}  # {key=id, value=name}

        for index, row in self._connection_data.iterrows():
            if row['toFn'] == id and row['toAspect'] == "T":
                outputfn_name = self.get_function_name(row['outputFn'])
                function_times.update({row['outputFn']: outputfn_name})

        return function_times

    def visualize(self,
                  ax: Axes | None = None) -> Axes:
        """
        Visualize the FRAM model.

        This uses Matplotlib to display the model. Colours are chosen based on
        the colours specified in the .xfmv file. Connections between functions
        use the Bezier curves specified in the .xfmv file.

        Parameters
        ----------
        ax : Axes, optional
            The Matplotlib Axes on which to render the FRAM model. If None,
            then a new Matplotlib Axes will be created. Defaults to None.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.

        Examples
        --------
        >>> import framalytics
        >>>
        >>> fram = framalytics.FRAM('my-fram-model.xfmv')
        >>> fram.visualize()
        """

        return self.visualizer.render(self._function_data,
                                      self._connection_data, ax=ax)

    def highlight_function_outputs(self,
                                   function: str | int,
                                   ax: Axes | None = None) -> Axes:
        """
        Visualize the FRAM model, with the output connections of a function
        highlighted.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.
        ax : Axes, optional
            The Matplotlib Axes on which to render the FRAM model. If None,
            then a new Matplotlib Axes will be created. Defaults to None.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.
        """
        if isinstance(function, str):
            functionID = self.get_function_id(function)
        elif isinstance(function, int):
            functionID = function
        else:
            raise ValueError("A function ID or name is required.")

        return self.visualizer.render_output_paths(self._function_data,
                                                   self._connection_data,
                                                   functionID, ax=ax)

    def highlight_full_path_from_function(self,
                                          function: str | int,
                                          ax: Axes | None = None) -> Axes:
        """
        Visualize the FRAM model, highlighting all functions downstream of the
        specified function.

        Parameters
        ----------
        function : str | int
            The ID (int) or name (str) of the desired function.
        ax : Axes, optional
            The Matplotlib Axes on which to render the FRAM model. If None,
            then a new Matplotlib Axes will be created. Defaults to None.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.
        """
        if isinstance(function, str):
            functionID = self.get_function_id(function)
        elif isinstance(function, int):
            functionID = function
        else:
            raise ValueError("A function ID name (string) is required.")

        return self.visualizer.render_path_from_function(self._function_data,
                                                         self._connection_data,
                                                         functionID,
                                                         ax=ax)

    def _count_data_connections(self,
                                data: pd.DataFrame,
                                column_type: str = "functions") -> dict:
        """
        Count the number of connections in the given DataFrame.

        The DataFrame is a set of observations. Each row is a single
        observation of "real" data for the system specified by the FRAM model,
        which specifies either the functions or the connections that are
        present for each observation. The columns are either the set of
        functions or the set of connections, selected by the "column_type"
        parameter.

        Paramters
        ---------
        data : pd.DataFrame
            The DataFrame containing the data to be counted.
        column_type : {'functions', 'connections'}
            Whether the columns of the data represent functions or connections.

        Returns
        -------
        dict
            The number of times each connection is present in the data.
        """
        connections = {}

        for index, row in self._connection_data.iterrows():
            connections.update({row.Name: 0.0})

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

                # Finds all instances where both column values are 1
                connection_value = len(data[(data[outputFn_name] == 1) &
                                            (data[toFn_name] == 1)])

                # Updates the number of times this path is traversed.
                connections.update({connection_default: connection_value})

        # If the dataframe uses connection_names for the column names.
        elif column_type == "connections":
            for connection_name in connections:
                connection_value = len(data[(data[connection_name] == 1)])
                connections.update({connection_name: connection_value})

        # Normalize connections
        for key, value in connections.items():
            connections[key] = value / len(data)

        return connections

    def highlight_data(self,
                       data: pd.DataFrame,
                       column_type: str = "functions",
                       appearance: str = "pure",
                       ax: Axes | None = None) -> Axes:
        """
        Visualize the FRAM model, highlighting connections based on a set of
        observations.

        The observations are "real" data of the system modeled by the FRAM.
        Each row is a single observation that specifies either the functions
        or the connections that are present. The columns of the DataFrame are
        either the set of functions or the set of connections, which must be
        specified in the "column_type" parameter.

        Connections are highlighted based on their occurrence rate in the data.
        They are coloured green if less than 25% of the observations contain
        the connection, yellow if 25-50% of the data contains the connection,
        orange if 50-75% of the data, and red if the connection is in more than
        75% of the observations.

        This colour scheme is the "pure" default style. The "traced" style
        adds a black outline to each connection, and "expand" changes the
        thickness of the connection based on how frequently the connection
        appears in the data.

        Paramters
        ---------
        data : pd.DataFrame
            A DataFrame containing the observations.
        column_type : {'functions', 'connections'}
            Whether the columns of the data represent functions or connections.
            Defaults to 'functions'.
        appearance : {'pure', 'traced', 'expand'}
            Select the visual representation of the connection highlight.
            Defaults to 'pure'.
        ax : Axes, optional
            The Matplotlib Axes on which to render the FRAM model. If None,
            then a new Matplotlib Axes will be created. Defaults to None.

        Returns
        -------
        Axes
            Returns the Matplotlib Axes the FRAM model was rendered onto.

        Examples
        --------

        The set of functions are:

        >>> fram.get_functions()
        {0: 'Step A',
         1: 'Step B',
         2: 'Step C',
         3: 'Last Step'}

         >>> data
                Step A  Step B  Step C  Last Step
            0 	0 	    0 	    1 	    1
            1 	0 	    0 	    0 	    1
            2 	1 	    1 	    1 	    0
            3 	0 	    1 	    1 	    1
            4 	1 	    0 	    0 	    1

        >>> fram.highlight_data(data, column_type='functions')

        """

        # Makes new figure without the Bezier curves being produced.

        connections = self._count_data_connections(data=data,
                                                   column_type=column_type)

        return self.visualizer.render(self._function_data,
                                      self._connection_data,
                                      real_connections=connections,
                                      appearance=appearance,
                                      ax=ax)
