# DataProcess/random_walks.py
import networkx as nx
import random
import os

def random_walk(graph, start_node, walk_length=10):
    """Perform a single random walk."""
    walk = [start_node]
    for _ in range(walk_length - 1):
        neighbors = list(graph.neighbors(walk[-1]))
        if not neighbors:
            break
        walk.append(random.choice(neighbors))
    return walk


def extract_paths(graph_file, save_path, num_walks=10, walk_length=10):
    """Perform multiple random walks on a graph and save as sequences."""
    G = nx.read_gpickle(graph_file)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    all_paths = []
    nodes = list(G.nodes())
    for _ in range(num_walks):
        start = random.choice(nodes)
        walk = random_walk(G, start, walk_length)
        all_paths.append(walk)

    with open(save_path, "w") as f:
        for path in all_paths:
            f.write(" ".join(path) + "\n")

    print(f"[+] Paths extracted and saved to {save_path}")
    return all_paths


if __name__ == "__main__":
    extract_paths("outputs/graphs/sample1.gpickle", "outputs/paths/sample1.txt")