from framalytics import fram

def test_get_function_metadata():
    """
    Tests to see if the returned function metadata (dataframe) is as expected. The function data is indexed from
    top to bottom in the .xfmv file. So the first function will be index 0. We test the expected outputs with respect
    to that knowledge.
    """

    # Select and generate the FRAM model data.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")
    function_metadata = test.get_function_metadata()

    # Each function has a unique IDNr. index 0 has a IDNr of 0, index 1 has a IDNr of 1, and so on.
    # For the .xfmv file we are using, all functions have a fnStyle of 0.
    index = 0
    for index, row in function_metadata.iterrows():
        assert row.IDNr == str(index)
        assert row.fnStyle == '0'
        index += 1

    # The rest are the expected outputs for the first function (index 0 in the dataframe).
    assert function_metadata.iloc[0].FunctionType == '0'
    assert function_metadata.iloc[0].IDName == 'Do stroke assessment by a care paramedic'
    assert function_metadata.iloc[0].x == '197.89999389648438'
    assert function_metadata.iloc[0].y == '143.59999084472656'
    assert function_metadata.iloc[0].style == 'green'
    assert function_metadata.iloc[0].color == '1555713'


def test_get_aspect_data():
    """
    Tests to see if the returned aspect metadata (dataframe) is as expected.
    """
    # Generate the aspect data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")
    aspect_data = test.get_connection_data()

    # Each row is a single aspect connection. The name consist of "outputFn|Name|toFn|Aspect". We confirm the dataframe
    # stores the proper toFn and outputFn data that is associated with the name. The columns, x and y should be 0.
    # Additionally, for this .xfmv file, directionX and directionY are 'from' and 'to' respectively while
    # notGroup = True for all aspects.
    for index, row in aspect_data.iterrows():
        split_name = row.Name.split("|")
        assert row.outputFn == split_name[0]
        assert row.toFn == split_name[2]
        assert row.x == '0'
        assert row.y == '0'
        assert row.directionX == 'from'
        assert row.directionY == 'to'
        assert row.notGroup == 'true'

def test_get_functions():
    """
    This test method tests 3 functions. These are "get_functions","get_function_id", and "get_function_name".
    "get_functions" returns a dictionary of key,value pairs which are {IDNr: Function Name} in terms of a function.
    "get_function_id" will return the associated id when given a function EXACT name. "get_function_name" does the
    exact opposite. So, by iterating thought the dictionary of "get_functions", we can call and test the other two
    functions to see if their returned value match the given id/name associated with a function.
    """

    # Generate the data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")
    functions = test.get_functions()

    # Call and iterate through the function {ID: Name} key,value pairs.

    for function_id, function_name in functions.items():

        # Each returned id should match the name and vice versa depending on the function called.
        assert test.get_function_id(function_name) == function_id
        assert test.get_function_name(function_id) == function_name

def test_number_of_edges_and_functions():
    """
    Tests to confirm that the number of edges and functions returned matches the expected values.
    """
    # Generates data from the .xfmv file and calls for the sum values of edges and functions.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")
    number_of_edges = test.number_of_edges()
    number_of_functions = test.number_of_functions()

    assert number_of_edges == 195
    assert number_of_functions == 73

    # Repeats this with another .xfmv file.
    test = fram.FRAM("Cup Noodles.xfmv")
    test.visualize("WebAgg")
    number_of_edges = test.number_of_edges()
    number_of_functions = test.number_of_functions()

    assert number_of_edges == 12
    assert number_of_functions == 10

def test_get_function_inputs():
    """
    Tests to see if the functions used as inputs returned for the specified function match.
    """
    # Generates data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")

    functions = test.get_functions()
    all_connections = test.get_connections()

    # For every function, we gather inputs based on connection data.
    for IDNr, name in functions.items():
        function_inputs = test.get_function_inputs(IDNr)
        inputs = []

        # If a connection has a toFn that matches the current functions IDNr and goes to it's Input aspect
        # Add it to the inputs.
        for index, row in all_connections.iterrows():
            if ((row.toFn == IDNr) and (row.toAspect == "I")):
                inputs.append(row.fromFn)

        # If all the inputs are returned by the function, when we perform (function_inputs.get(id)), the value should
        # never be none. It should always return the fromFn function name. Otherwise, there is an error!
        for id in inputs:
            assert function_inputs.get(id) != None


def test_get_function_outputs():
    """
    Tests to see if the functions that use the specified function as output inputs returned is accurate.
    """
    # Generates data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")

    functions = test.get_functions()
    all_connections = test.get_connections()

    # For every function, we gather inputs based on connection data.
    for IDNr, name in functions.items():
        function_outputs = test.get_function_outputs(IDNr)
        outputs = []

        # If a connection has a fromFn that matches the current functions IDNr, add it to the outputs.
        for index, row in all_connections.iterrows():
            if (row.fromFn == IDNr):
                outputs.append(row.toFn)

        # If all the outputs are returned by the function, when we perform (function_outputs.get(id)), the value should
        # never be "None". It should always return the toFn function name. Otherwise, there is an error!
        for id in outputs:
            assert function_outputs.get(id) != None

def test_get_function_preconditions():
    """
    Tests to see if the functions used as preconditions returned for the specified function match.
    """
    # Generates data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")

    functions = test.get_functions()
    all_connections = test.get_connections()

    # For every function, we gather preconditions based on connection data.
    for IDNr, name in functions.items():
        function_preconditions = test.get_function_preconditions(IDNr)
        preconditions = []

        # If a connection has a toFn that matches the current functions IDNr and goes to it's preconditions aspect
        # Add it to the inputs.
        for index, row in all_connections.iterrows():
            if ((row.toFn == IDNr) and (row.toAspect == "P")):
                preconditions.append(row.fromFn)

        # If all the preconditions are returned by the function, when we perform (function_preconditions.get(id)), the
        # value should never be "None". It should always return the fromFn function name. Otherwise, there is an error!

        for id in preconditions:
            assert function_preconditions.get(id) != None

def test_get_function_resources():
    """
    Tests to see if the functions used as resources returned for the specified function match.
    """
    # Generates data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")

    functions = test.get_functions()
    all_connections = test.get_connections()

    # For every function, we gather resources based on connection data.
    for IDNr, name in functions.items():
        function_resources = test.get_function_resources(IDNr)
        resources = []

        # If a connection has a toFn that matches the current functions IDNr and goes to it's resources aspect
        # Add it to the resources.
        for index, row in all_connections.iterrows():
            if ((row.toFn == IDNr) and (row.toAspect == "R")):
                resources.append(row.fromFn)

        # If all the resources are returned by the function, when we perform (function_resources.get(id)), the
        # value should never be "None". It should always return the fromFn function name. Otherwise, there is an error!

        for id in resources:
            assert function_resources.get(id) != None


def test_get_function_controls():
    """
    Tests to see if the functions used as controls returned for the specified function match.
    """
    # Generates data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")

    functions = test.get_functions()
    all_connections = test.get_connections()

    # For every function, we gather controls based on connection data.
    for IDNr, name in functions.items():
        function_controls = test.get_function_controls(IDNr)
        controls = []

        # If a connection has a toFn that matches the current functions IDNr and goes to it's controls aspect
        # Add it to the controls.
        for index, row in all_connections.iterrows():
            if ((row.toFn == IDNr) and (row.toAspect == "C")):
                controls.append(row.fromFn)

        # If all the controls are returned by the function, when we perform (function_controls.get(id)), the
        # value should never be "None". It should always return the fromFn function name. Otherwise, there is an error!

        for id in controls:
            assert function_controls.get(id) != None


def test_get_function_times():
    """
    Tests to see if the functions used as times returned for the specified function match.
    """
    # Generates data from the .xfmv file.
    test = fram.FRAM("FRAM model-Stroke care system.xfmv")
    test.visualize("WebAgg")

    functions = test.get_functions()
    all_connections = test.get_connections()

    # For every function, we gather times based on connection data.
    for IDNr, name in functions.items():
        function_times = test.get_function_times(IDNr)
        times = []

        # If a connection has a toFn that matches the current functions IDNr and goes to it's times aspect
        # Add it to the times.
        for index, row in all_connections.iterrows():
            if ((row.toFn == IDNr) and (row.toAspect == "T")):
                times.append(row.fromFn)

        # If all the times are returned by the function, when we perform (function_times.get(id)), the
        # value should never be "None". It should always return the fromFn function name. Otherwise, there is an error!

        for id in times:
            assert function_times.get(id) != None

def main():
    test = test_get_function_metadata()
    test = test_get_aspect_data()
    test = test_get_functions()
    test = test_number_of_edges_and_functions()
    test = test_get_function_inputs()
    test = test_get_function_outputs()
    test = test_get_function_preconditions()
    test = test_get_function_resources()
    test = test_get_function_controls()
    test = test_get_function_times()



if __name__ == "__main__":
    main()