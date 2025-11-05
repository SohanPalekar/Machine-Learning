# DataProcess/graph_builder.py
import networkx as nx
import csv
import os

def build_graph(csv_file, save_path):
    """
    Build a directed API graph from parsed CSV trace.
    Nodes: API calls
    Edges: Temporal connections between consecutive calls
    """
    G = nx.DiGraph()
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        prev_api = None
        for row in reader:
            api = row["api_call"]
            G.add_node(api)
            if prev_api:
                G.add_edge(prev_api, api)
            prev_api = api

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    nx.write_gpickle(G, save_path)
    print(f"[+] Graph saved to {save_path}")
    return G


if __name__ == "__main__":
    build_graph("outputs/parsed/sample1.csv", "outputs/graphs/sample1.gpickle")