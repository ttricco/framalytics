import pandas as pd
from pathlib import Path

import pytest

from framalytics.xfmv_parser import parse_xfmv


@pytest.fixture
def simple_xfmv() -> str:
    file = Path(__file__).parent / 'resources/simple_fram.xfmv'
    return str(file)


@pytest.fixture
def colored_xfmv() -> str:
    file = Path(__file__).parent / 'resources/colored_fram.xfmv'
    return str(file)


@pytest.fixture()
def parsed_xfmv(simple_xfmv: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    return parse_xfmv(simple_xfmv)


def test_return_types(parsed_xfmv: tuple[pd.DataFrame, pd.DataFrame]) -> None:
    """ Parsing xfmv should return 3 DataFrames. """

    functions, connections = parsed_xfmv

    assert isinstance(functions, pd.DataFrame)
    assert isinstance(connections, pd.DataFrame)


def test_function_data(parsed_xfmv: tuple[pd.DataFrame, pd.DataFrame]) -> None:
    """ Test that function names, ids and types were parsed correctly. """

    functions, connections = parsed_xfmv

    expected_names = ['Function A', 'Function B', 'Function C',
                      'Function D', 'Function E', 'Function F']
    expected_types = {'Function A': 0, 'Function B': 0, 'Function C': 2,
                      'Function D': 0, 'Function E': 0, 'Function F': 2}
    expected_ids = {'Function A': 0, 'Function B': 1, 'Function C': 2,
                    'Function D': 3, 'Function E': 4, 'Function F': 5}

    assert len(functions) == 6
    assert set(functions.IDName.unique()) == set(expected_names)

    tmp = functions[['IDName', 'IDNr']]
    ids = tmp.set_index('IDName')['IDNr'].to_dict()

    assert ids == expected_ids

    tmp = functions[['IDName', 'FunctionType']]
    types = tmp.set_index('IDName')['FunctionType'].to_dict()

    assert types == expected_types


def test_function_positions(parsed_xfmv: tuple[pd.DataFrame,
                                               pd.DataFrame]) -> None:
    """ Test that function positions were parsed correctly. """

    functions, connections = parsed_xfmv

    x, y = functions[functions.IDName == 'Function A'][['x', 'y']].values[0]
    assert x == pytest.approx(88.67, abs=1e-2)
    assert y == pytest.approx(364.67, abs=1e-2)

    x, y = functions[functions.IDName == 'Function B'][['x', 'y']].values[0]
    assert x == pytest.approx(91.33, abs=1e-2)
    assert y == pytest.approx(203.33, abs=1e-2)

    x, y = functions[functions.IDName == 'Function C'][['x', 'y']].values[0]
    assert x == pytest.approx(92.00, abs=1e-2)
    assert y == pytest.approx(25.33, abs=1e-2)

    x, y = functions[functions.IDName == 'Function D'][['x', 'y']].values[0]
    assert x == pytest.approx(290.67, abs=1e-2)
    assert y == pytest.approx(172.00, abs=1e-2)

    x, y = functions[functions.IDName == 'Function E'][['x', 'y']].values[0]
    assert x == pytest.approx(423.33, abs=1e-2)
    assert y == pytest.approx(37.33, abs=1e-2)

    x, y = functions[functions.IDName == 'Function F'][['x', 'y']].values[0]
    assert x == pytest.approx(444.66, abs=1e-2)
    assert y == pytest.approx(186.66, abs=1e-2)


def test_connection_raw_name(parsed_xfmv: tuple[pd.DataFrame,
                                                pd.DataFrame]) -> None:
    """ Test that the raw connection name was parsed correctly. """

    functions, connections = parsed_xfmv

    connection_raw_names = ['2|Connection CB|1|C', '1|Connection BA|0|I',
                            '1|Connection BD|3|I', '2|Connection CD|3|T',
                            '2|Connection CE|4|P', '0|Connection AB|1|I',
                            '5|Connection FE|4|R', '3|Connection DE|4|P']

    assert len(connections) == 8
    assert set(connections['Name'].unique()) == set(connection_raw_names)


def test_connection_names(parsed_xfmv: tuple[pd.DataFrame,
                                             pd.DataFrame]) -> None:
    """ Test that connection data was parsed correctly. """

    functions, connections = parsed_xfmv

    connection_raw_names = ['2|Connection CB|1|C', '1|Connection BA|0|I',
                            '1|Connection BD|3|I', '2|Connection CD|3|T',
                            '2|Connection CE|4|P', '0|Connection AB|1|I',
                            '5|Connection FE|4|R', '3|Connection DE|4|P']
    connection_names = ['Connection CB', 'Connection BA', 'Connection BD',
                        'Connection CD', 'Connection CE', 'Connection AB',
                        'Connection FE', 'Connection DE']
    connection_aspects = ['C', 'I', 'I', 'T', 'P', 'I', 'R', 'P']
    connection_outputFns = [2, 1, 1, 2, 2, 0, 5, 3]
    connection_toFns = [1, 0, 3, 3, 4, 1, 4, 4]

    connection_data = pd.DataFrame({'Name': connection_raw_names,
                                    'parsed_name': connection_names,
                                    'toAspect': connection_aspects,
                                    'outputFn': connection_outputFns,
                                    'toFn': connection_toFns})

    tmp = connection_data[['Name', 'parsed_name']]
    expected_names = tmp.set_index('Name')['parsed_name'].to_dict()
    tmp = connections[['Name', 'parsed_name']]
    names = tmp.set_index('Name')['parsed_name'].to_dict()

    assert names == expected_names

    tmp = connection_data[['Name', 'toAspect']]
    expected_aspects = tmp.set_index('Name')['toAspect'].to_dict()
    tmp = connections[['Name', 'toAspect']]
    aspects = tmp.set_index('Name')['toAspect'].to_dict()

    assert aspects == expected_aspects

    tmp = connection_data[['Name', 'outputFn']]
    expected_outputs = tmp.set_index('Name')['outputFn'].to_dict()
    tmp = connections[['Name', 'outputFn']]
    outputs = tmp.set_index('Name')['outputFn'].to_dict()

    assert outputs == expected_outputs

    tmp = connection_data[['Name', 'toFn']]
    expected_toFns = tmp.set_index('Name')['toFn'].to_dict()
    tmp = connections[['Name', 'toFn']]
    toFns = tmp.set_index('Name')['toFn'].to_dict()

    assert toFns == expected_toFns


def test_function_description(colored_xfmv: str) -> None:
    """Test that function descriptions are parsed correctly."""

    functions, connections = parse_xfmv(colored_xfmv)

    # Check that Description column exists
    assert 'Description' in functions.columns

    # Check that function with IDNr 0 has the correct description
    function_0 = functions[functions['IDNr'] == 0]
    assert len(function_0) == 1
    assert function_0['Description'].values[0] == "Description of B4"

    # Verify the function name is correct
    assert function_0['IDName'].values[0] == "B4"
