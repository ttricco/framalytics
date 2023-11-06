# framalytics/read_xfmv.py
from .xfmv_parser import parse_xfmv
from .visualize import visualize_network

def read_xfmv(filename):
    df_function, df_input, df_aspect = parse_xfmv(filename)
    # Additional processing if needed
    return df_function, df_input, df_aspect

def visualize(f):
    visualize_network(f)