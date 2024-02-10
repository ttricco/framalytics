# framalytics/read_xfmv.py
from xfmv_parser import parse_xfmv
from visualize import visualize_network
import pandas as pd

def read_xfmv(filename):
    df_function, df_input, df_aspect = parse_xfmv(filename)
    # Additional processing if needed
    return df_function, df_input, df_aspect

def preprocess_data(df_function, filtered_df):
    # Assume filtered_df is a DataFrame that has been read in and filtered elsewhere

    # Drop unnecessary columns
    filtered_df.drop(columns=['x', 'y', 'directionX', 'directionY', 'notGroup','Curve'], inplace=True)

    # Rename columns to unify naming conventions
    filtered_df.rename(columns={"outputFn": "exporter", "toFn": "importer"}, inplace=True)

    # Convert positions to numeric
    filtered_df['x'] = pd.to_numeric(filtered_df['x'], errors='coerce')
    filtered_df['y'] = pd.to_numeric(filtered_df['y'], errors='coerce')

    # Merge the DataFrame with df_function for both exporters and importers
    merged_df_exporter = pd.merge(df_function, filtered_df, left_on="IDNr", right_on="exporter")
    merged_df_importer = pd.merge(df_function, filtered_df, left_on="IDNr", right_on="importer")

    # Drop columns from merged dataframes
    merged_df_exporter.drop(['FunctionType', 'IDNr'], axis=1, inplace=True)
    merged_df_importer.drop(['FunctionType', 'IDNr'], axis=1, inplace=True)

    return merged_df_exporter, merged_df_importer


def visualize(f):
    visualize_network(f)
