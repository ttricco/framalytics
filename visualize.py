import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def visualize_network(framalytics_obj):
    # Create a directed graph
    G = nx.DiGraph()

    # Access data from the framalytics_obj assuming it has 'df_exporter_info' and 'df_importer_info' attributes
    df_exporter_info = framalytics_obj.df_exporter_info
    df_importer_info = framalytics_obj.df_importer_info

    # Add exporter nodes with color attribute
    for _, row in df_exporter_info.iterrows():
        exporter_node = row['exporter']
        G.add_node(exporter_node, label=f"Exporter {row['IDName']}", pos=(row['x'], row['y']), type='exporter', style=row['style'])

    # Add importer nodes with color attribute
    for _, row in df_importer_info.iterrows():
        importer_node = row['importer']
        G.add_node(importer_node, label=f"Importer {row['IDName']}", pos=(row['x'], row['y']), type='importer', style=row['style'])

    # Create connections dataframe from exporter to importer
    connections_data = {
        'exporter': df_exporter_info['exporter'],
        'importer': df_importer_info['importer']
    }
    connections_df = pd.DataFrame(connections_data)

    # Add edges to the graph
    for _, row in connections_df.iterrows():
        exporter_node = row['exporter']
        importer_node = row['importer']
        G.add_edge(exporter_node, importer_node)

    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')

    # Use fillna to replace NaN values with a default color
    default_color = 'green'
    exporter_colors = [df_exporter_info[df_exporter_info['exporter'] == node]['style'].fillna(default_color).iloc[0] for node in G.nodes if G.nodes[node]['type'] == 'exporter']
    importer_colors = [df_importer_info[df_importer_info['importer'] == node]['style'].fillna(default_color).iloc[0] for node in G.nodes if G.nodes[node]['type'] == 'importer']

    # Draw the graph
    fig, ax = plt.subplots(figsize=(15, 15))  # Adjusted to a more reasonable figure size

    # Draw exporter nodes with specified colors and larger node_size
    exporter_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'exporter']
    nx.draw_networkx_nodes(G, pos, nodelist=exporter_nodes, node_size=500, node_color=exporter_colors)  # Adjusted size to a reasonable value

    # Draw importer nodes with specified colors and larger node_size
    importer_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'importer']
    nx.draw_networkx_nodes(G, pos, nodelist=importer_nodes, node_size=500, node_color=importer_colors)  # Adjusted size to a reasonable value

    # Draw curved edges with thicker arrows and larger arrowheads
    for edge in G.edges():
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='gray', width=2, arrowstyle='-|>', arrowsize=10, connectionstyle="arc3,rad=0.1")

    # Draw node labels with IDName and adjust font size
    node_labels = {node: data['label'] for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)  # Adjusted font size to a reasonable value

    plt.title('Functional Resource Analysis Map')
    plt.axis('off')  # Hide axes
    return plt.show()
