import xml.etree.ElementTree as ET
import pandas as pd
def parse_xfmv(filename):
    # Parse the XML file
    tree = ET.parse(filename)
    root = tree.getroot()

    # Extract data from Function elements
    function_data = []

    for function_elem in root.findall('.//Function'):
        element_data = {'IDNr': function_elem.findtext('IDNr'),
        'FunctionType': function_elem.findtext('FunctionType'),
        'IDName': function_elem.findtext('IDName'),
        'Description': function_elem.findtext('Description'),
        'x': function_elem.attrib.get('x', None),
        'y': function_elem.attrib.get('y', None),
        'style': function_elem.attrib.get('style', None),
        'color': function_elem.attrib.get('color', None),
        }
        function_data.append(element_data)

    # Extract data from Input elements
    input_data = []

    for input_elem in root.findall('.//Input'):
        input_element_data = {
            'IDNr': input_elem.findtext('IDNr'),
            'IDName': input_elem.findtext('IDName'),
            'FunctionIDNr': input_elem.findtext('FunctionIDNr'),
        }
        input_data.append(input_element_data)

    # Extract data from Aspect elements
    aspect_data = []

    for aspect_elem in root.findall('.//Aspect'):
        aspect_element_data = {
            'x': aspect_elem.attrib.get('x', None),
            'y': aspect_elem.attrib.get('y', None),
            'directionX': aspect_elem.attrib.get('directionX', None),
            'directionY': aspect_elem.attrib.get('directionY', None),
            'notGroup': aspect_elem.attrib.get('notGroup', None),
            'outputFn': aspect_elem.attrib.get('outputFn', None),
            'toFn': aspect_elem.attrib.get('toFn', None),
            'Name': aspect_elem.findtext('Name'),
            'Curve': aspect_elem.findtext('Curve'),
        }
        aspect_data.append(aspect_element_data)

    # Create Pandas DataFrames
    df_function = pd.DataFrame(function_data)
    df_input = pd.DataFrame(input_data)
    df_aspect = pd.DataFrame(aspect_data)
    return df_function, df_input, df_aspect

"""
# Display the DataFrames
print("Function DataFrame:")
print(df_function)

print("\nInput DataFrame:")
print(df_input)

print("\nAspect DataFrame:")
print(df_aspect)
"""
