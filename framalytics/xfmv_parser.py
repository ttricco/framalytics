import xml.etree.ElementTree as ET
import pandas as pd
import math


def create_bezier_curve(from_x: float,
                        from_y: float,
                        from_aspect: str,
                        to_x: float,
                        to_y: float,
                        to_aspect: str,
                        curviness: float = 0.15) -> str:
    """
    Create a Bezier curve based on a Hobby-spline heuristic.

    Parameters
    ----------
    from_x : float
        x-coordinate of the first control point.
    from_y : float
        y-coordinate of the first control point.
    from_aspect : str
        The aspect (I, O, T, C, P, R) of the first control point.
    to_x : float
        x-coordinate of the last control point.
    to_y : float
        y-coordinate of the last control point.
    to_aspect : str
        The aspect (I, O, T, C, P, R) of the last control point.
    curviness : float, optional
        0 is straight. 0.5 is round. Defaults to 0.15 for a slight curve.

    Returns
    -------
    str
        A string describing the 5 control points of the curve.
    """

    if from_aspect not in ['I', 'O', 'T', 'C', 'P', 'R']:
        raise ValueError('Invalid to aspect')
    if to_aspect not in ['I', 'O', 'T', 'C', 'P', 'R']:
        raise ValueError('Invalid from aspect')

    aspect_offsets = {
        "I": (-44, 0),
        "O": (44, 0),
        "T": (-23, -35),
        "C": (23, -35),
        "P": (-23, 35),
        "R": (23, 35)
    }

    dx0, dy0 = aspect_offsets[from_aspect]
    dx1, dy1 = aspect_offsets[to_aspect]

    p0x = from_x + 48 + dx0
    p0y = from_y + 50 + dy0
    p4x = to_x + 48 + dx1
    p4y = to_y + 50 + dy1

    if p0x < p4x and p0y < p4y:
        quadrant = "ll"
    elif p0x >= p4x and p0y < p4y:
        quadrant = "lr"
    elif p0x < p4x and p0y >= p4y:
        quadrant = "ul"
    else:
        quadrant = "ur"

    flip = False
    if to_aspect in ['T', 'C'] and quadrant in ["ll", "lr"]:
        flip = True
    elif to_aspect in ['P', 'R'] and quadrant in ["ul", "ur"]:
        flip = True
    elif to_aspect == 'I' and quadrant in ["ll", "lr"]:
        flip = True

    s_curve = False
    if to_aspect == 'I':
        s_curve = True

    dx = p4x - p0x
    dy = p4y - p0y
    L = math.sqrt(dx**2 + dy**2)
    if L == 0:
        raise ValueError("Endpoints are identical")

    # 90 degree left normal
    nx = -dy / L
    ny = dx / L
    if flip:
        nx = -nx
        ny = -ny

    # handle distance along the chord and normal offset
    k = curviness * L

    # build middle three control points
    if s_curve:
        p1x = p0x + dx * 0.33 + nx * k
        p1y = p0y + dy * 0.33 + ny * k
        p2x = p0x + dx * 0.5
        p2y = p0y + dy * 0.5
        p3x = p0x + dx * 0.66 - nx * k
        p3y = p0y + dy * 0.66 - ny * k
    else:
        p1x = p0x + dx * 0.33 + nx * k
        p1y = p0y + dy * 0.33 + ny * k
        p2x = p0x + dx * 0.5 + nx * k
        p2y = p0y + dy * 0.5 + ny * k
        p3x = p0x + dx * 0.66 + nx * k
        p3y = p0y + dy * 0.66 + ny * k

    curve = f"{p0x:.2f}|{p0y:.2f}|{p4x:.2f}|{p4y:.2f}|"
    curve += f"{p3x:.2f}|{p3y:.2f}|{p1x:.2f}|{p1y:.2f}|{p2x:.2f}|{p2y:.2f}"

    return curve


def synthesize_connections(root: ET.Element,
                           df_function: pd.DataFrame) -> list:
    """
    Create connections based on Aspects data in an xfmv file.

    Parameters
    ----------
    root : ET.Element
        The xml element tree root.
    df_function : pd.DataFrame
        A DataFrame containing the function data.

    Returns
    -------
    list
        A list containing the synthesized connections.
    """
    aspect_tags = {
        'Input': 'I',
        'Output': 'O',
        'Control': 'C',
        'Precondition': 'P',
        'Time': 'T',
        'Resource': 'R'
    }

    # Parse dict of (IDName, [[fn_id, aspect], ...])
    connections: dict[str, list[tuple[int, str]]] = dict()

    for tag, char in aspect_tags.items():
        for elem in root.findall(f".//{tag}"):
            idname = elem.findtext("IDName")
            fn_id = elem.findtext("FunctionIDNr")
            if idname and fn_id:
                connections.setdefault(idname, []).append((int(fn_id), char))

    synthesized_connections = []
    for idname, refs in connections.items():
        outputs = [(fid, aspect) for fid, aspect in refs if aspect == 'O']
        targets = [(fid, aspect) for fid, aspect in refs if aspect != 'O']

        for output_fn, _ in outputs:
            for target_fn, to_aspect in targets:
                synthesized_connections.append({
                    "x": "0.000",
                    "y": "0.000",
                    "directionX": "from",
                    "directionY": "to",
                    "notGroup": "true",
                    "outputFn": output_fn,
                    "toFn": target_fn,
                    "Name": f"{output_fn}|{idname}|{target_fn}|{to_aspect}",
                    "Curve": "",
                })

    # make curves
    for aspect in synthesized_connections:
        from_fn = aspect['outputFn']
        to_fn = aspect['toFn']
        from_aspect = "O"  # always from output
        to_aspect = str(aspect['Name']).split("|")[3]  # target always at end

        x0 = df_function[df_function.IDNr == from_fn]['x'].iloc[0]
        y0 = df_function[df_function.IDNr == from_fn]['y'].iloc[0]
        x1 = df_function[df_function.IDNr == to_fn]['x'].iloc[0]
        y1 = df_function[df_function.IDNr == to_fn]['y'].iloc[0]

        aspect['Curve'] = create_bezier_curve(x0, y0, from_aspect,
                                              x1, y1, to_aspect)

    return synthesized_connections


def parse_xfmv(filename: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse an xfmv file into its function and connection data.

    Parameters
    ----------
    filename : str
        A .xfmv file to parse.

    Returns
    -------
    pd.DataFrame
        A dataframe containing the function data.
    pd.DataFrame
        A dataframe containing the connection data.
    """
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

    df_function = pd.DataFrame(function_data)
    df_function['IDNr'] = df_function['IDNr'].astype(int)
    df_function['FunctionType'] = df_function['FunctionType'].astype(int)
    df_function['x'] = df_function['x'].astype(float)
    df_function['y'] = df_function['y'].astype(float)

    # Extract data from Aspect elements
    connection_data = []

    for connection_elem in root.findall('.//Aspect'):
        connection_element_data = {
            'x': connection_elem.attrib.get('x', None),
            'y': connection_elem.attrib.get('y', None),
            'directionX': connection_elem.attrib.get('directionX', None),
            'directionY': connection_elem.attrib.get('directionY', None),
            'notGroup': connection_elem.attrib.get('notGroup', None),
            'outputFn': connection_elem.attrib.get('outputFn', None),
            'toFn': connection_elem.attrib.get('toFn', None),
            'Name': connection_elem.findtext('Name'),
            'Curve': connection_elem.findtext('Curve'),
        }
        connection_data.append(connection_element_data)

    if len(connection_data) == 0:
        connection_data = synthesize_connections(root, df_function)

    df_connection = pd.DataFrame(connection_data)

    for index, row in df_connection.iterrows():
        # 0 = OutputFn, 1 = Name, 2 = toFn, 3 = Aspect (R,C,I,O,T,P)
        name_split = row.Name.split("|")
        if row['outputFn'] is None:
            row['outputFn'] = name_split[0]
        if row['toFn'] is None:
            row['toFn'] = name_split[2]

    df_connection['outputFn'] = df_connection['outputFn'].astype(int)
    df_connection['toFn'] = df_connection['toFn'].astype(int)

    df_tmp = df_connection['Name'].str.split('|', expand=True)
    df_connection['parsed_name'] = df_tmp[1]
    df_connection['toAspect'] = df_tmp[3]

    return df_function, df_connection
