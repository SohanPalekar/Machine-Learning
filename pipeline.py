# pipeline.py
import os
from DataProcess.parse_traces import parse_trace
from DataProcess.graph_builder import build_graph
from DataProcess.random_walks import extract_paths
from train import train_doc2vec
from classify import train_classifier

def run_pipeline():
    print("=== API2Vec Data Processing Pipeline ===")

    # Step 1: Parse traces
    for category in ["black", "white"]:
        folder = f"dataset/{category}"
        for file in os.listdir(folder):
            if file.endswith(".json"):
                in_path = os.path.join(folder, file)
                out_path = f"outputs/parsed/{category}_{file.replace('.json', '.csv')}"
                parse_trace(in_path, out_path)

    # Step 2: Build graphs
    parsed_dir = "outputs/parsed"
    for file in os.listdir(parsed_dir):
        if file.endswith(".csv"):
            in_file = os.path.join(parsed_dir, file)
            out_file = f"outputs/graphs/{file.replace('.csv', '.gpickle')}"
            build_graph(in_file, out_file)

    # Step 3: Extract paths
    graphs_dir = "outputs/graphs"
    for file in os.listdir(graphs_dir):
        if file.endswith(".gpickle"):
            in_file = os.path.join(graphs_dir, file)
            out_file = f"outputs/paths/{file.replace('.gpickle', '.txt')}"
            extract_paths(in_file, out_file)

    # Step 4: Train embeddings
    train_doc2vec("outputs/paths", "models/api2vec.bin")

    # Step 5: Train and evaluate classifier
    train_classifier("models/api2vec.bin", "outputs/paths")

    print("=== Pipeline Complete ===")


if __name__ == "__main__":
    run_pipeline()