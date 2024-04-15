import pandas as pd
import json

def visualize_graph(graph_data, filename, cycle_list):
    nodes = []
    links = []
    num_vertices = len(graph_data)

    node_ids = graph_data.columns

    # Create nodes
    for node_id in node_ids:
        nodes.append({"id": str(node_id)})

    graph_copy = graph_data.copy(deep=True)

    # Highlight cycle edges based on cycle_list indices
    if filename in ['rudrata_output', 'tsp_output'] and cycle_list:
        for i in range(len(cycle_list)):
            next_index = (i + 1) % len(cycle_list)
            from_index, to_index = cycle_list[i], cycle_list[next_index]
            graph_copy.iloc[from_index, to_index] = 2
            graph_copy.iloc[to_index, from_index] = 2  # Assuming undirected graph

    # Create links
    for i in range(num_vertices):
        for j in range(num_vertices):
            if graph_copy.iloc[i, j] >= 1:
                links.append({
                    "source": str(node_ids[i]), 
                    "target": str(node_ids[j]), 
                    "value": str(graph_copy.iloc[i, j])
                })

    # Create JSON object
    json_data = {"nodes": nodes, "links": links}

    return json_data