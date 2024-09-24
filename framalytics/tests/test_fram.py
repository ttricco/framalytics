from pathlib import Path

import pytest

import pandas as pd
import framalytics


@pytest.fixture
def simple_xfmv():
    file = Path(__file__).parent / 'resources/simple_fram.xfmv'
    return str(file)


@pytest.fixture
def fram(simple_xfmv):
    return framalytics.FRAM(simple_xfmv)


def test_number_of_connections(fram):
    assert fram.number_of_connections() == 8


def test_number_of_functions(fram):
    assert fram.number_of_functions() == 6


def test_get_functions(fram):
    functions = {0: 'Function A', 1: 'Function B', 2: 'Function C',
                 3: 'Function D', 4: 'Function E', 5: 'Function F'}

    assert fram.get_functions() == functions


def test_get_connections(fram):
    expected_names = ['Connection CB', 'Connection BA', 'Connection BD',
                      'Connection CD', 'Connection CE', 'Connection AB',
                      'Connection FE', 'Connection DE']

    expected_connections = pd.DataFrame({'fromFn': [2, 1, 1, 2, 2, 0, 5, 3],
                                         'toFn': [1, 0, 3, 3, 4, 1, 4, 4],
                                         'toAspect': ['C', 'I', 'I', 'T',
                                                      'P', 'I', 'R', 'P'],
                                         'Name': expected_names})

    connections = fram.get_connections()

    assert set(connections.Name) == set(expected_names)

    expected_fromFns = expected_connections[['Name', 'fromFn']]
    expected_fromFns = expected_fromFns.set_index('Name')['fromFn'].to_dict()
    fromFns = connections[['Name', 'fromFn']]
    fromFns = fromFns.set_index('Name')['fromFn'].to_dict()

    assert fromFns == expected_fromFns

    expected_toFns = expected_connections[['Name', 'toFn']]
    expected_toFns = expected_toFns.set_index('Name')['toFn'].to_dict()
    toFns = connections[['Name', 'toFn']]
    toFns = toFns.set_index('Name')['toFn'].to_dict()

    assert toFns == expected_toFns

    expected_aspects = expected_connections[['Name', 'toAspect']]
    expected_aspects = expected_aspects.set_index('Name')['toAspect'].to_dict()
    aspects = connections[['Name', 'toAspect']]
    aspects = aspects.set_index('Name')['toAspect'].to_dict()

    assert aspects == expected_aspects


def test_get_function_name(fram):
    assert fram.get_function_name(0) == 'Function A'
    assert fram.get_function_name(1) == 'Function B'
    assert fram.get_function_name(2) == 'Function C'
    assert fram.get_function_name(3) == 'Function D'
    assert fram.get_function_name(4) == 'Function E'
    assert fram.get_function_name(5) == 'Function F'


def test_get_function_id(fram):
    assert fram.get_function_id('Function A') == 0
    assert fram.get_function_id('Function B') == 1
    assert fram.get_function_id('Function C') == 2
    assert fram.get_function_id('Function D') == 3
    assert fram.get_function_id('Function E') == 4
    assert fram.get_function_id('Function F') == 5


@pytest.mark.parametrize("aspect, get_function",
                         [('I', 'get_function_inputs'),
                          ('O', 'get_function_outputs'),
                          ('T', 'get_function_times'),
                          ('C', 'get_function_controls'),
                          ('P', 'get_function_preconditions'),
                          ('R', 'get_function_resources')])
def test_get_connection_sources(fram, aspect, get_function):
    """
    get_function_* correctly return the functions connected to each aspect.

    The test gets the list of functions connected to each aspect. The test
    is parametrized so that it runs per aspect. The getattr() calls the
    associated get_function_* method.
    """

    functions = fram.get_functions()
    connections = fram.get_connections()

    # For every function, we gather inputs based on connection data.
    for IDNr, name in functions.items():
        fns = getattr(fram, get_function)(IDNr)

        expected_fns = connections[(connections.toAspect == aspect)
                                   & (connections.toFn == IDNr)]['fromFn']

        for expected_fn in expected_fns:
            assert fns.get(expected_fn) is not None
