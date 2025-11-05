# DataProcess/parse_traces.py
import json
import csv
import os

def parse_trace(input_path, output_path):
    """
    Convert sandbox logs or JSON traces into CSV format.
    Columns: process_id, timestamp, api_call, parent_pid
    """
    traces = []
    with open(input_path, "r") as f:
        for line in f:
            data = json.loads(line)
            traces.append({
                "process_id": data.get("pid", ""),
                "timestamp": data.get("time", ""),
                "api_call": data.get("api", ""),
                "parent_pid": data.get("ppid", "")
            })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["process_id", "timestamp", "api_call", "parent_pid"])
        writer.writeheader()
        writer.writerows(traces)
    print(f"[+] Parsed trace saved to {output_path}")


if __name__ == "__main__":
    # Example usage
    parse_trace("dataset/black/sample1.json", "outputs/parsed/sample1.csv")