import xml.etree.ElementTree as ET
import pandas as pd


def parse_xfmv(filename: str) -> tuple[pd.DataFrame,
                                       pd.DataFrame, pd.DataFrame]:

    # Parse the XML file
    tree = ET.parse(filename)
    root = tree.getroot()

    # Extract data from Function elements
    function_data = []

    for function_elem in root.findall('.//Function'):
        element_data = {
            'IDNr': function_elem.findtext('IDNr'),
            'FunctionType': function_elem.findtext('FunctionType'),
            'IDName': function_elem.findtext('IDName'),
            'Description': function_elem.findtext('Description'),
            'x': function_elem.attrib.get('x', None),
            'y': function_elem.attrib.get('y', None),
            'style': function_elem.attrib.get('style', None),
            'color': function_elem.attrib.get('color', None),
            'fnStyle': function_elem.attrib.get('fnStyle', None)
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
    df_function['IDNr'] = df_function['IDNr'].astype(int)
    df_function['FunctionType'] = df_function['FunctionType'].astype(int)
    df_function['x'] = df_function['x'].astype(float)
    df_function['y'] = df_function['y'].astype(float)

    df_input = pd.DataFrame(input_data)

    df_aspect = pd.DataFrame(aspect_data)

    for index, row in df_aspect.iterrows():
        # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)
        name_split = row.Name.split("|")
        if row['outputFn'] is None:
            row['outputFn'] = name_split[0]
        if row['toFn'] is None:
            row['toFn'] = name_split[2]

    df_aspect['outputFn'] = df_aspect['outputFn'].astype(int)
    df_aspect['toFn'] = df_aspect['toFn'].astype(int)

    df_tmp = df_aspect['Name'].str.split('|', expand=True)
    df_aspect['parsed_name'] = df_tmp[1]
    df_aspect['toAspect'] = df_tmp[3]

    return df_function, df_input, df_aspect
