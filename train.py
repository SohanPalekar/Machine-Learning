# train.py
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import glob
import os

def train_doc2vec(paths_dir, model_path="models/api2vec.bin"):
    documents = []
    for file in glob.glob(os.path.join(paths_dir, "*.txt")):
        with open(file, "r") as f:
            for i, line in enumerate(f):
                tokens = line.strip().split()
                tag = f"{os.path.basename(file)}_{i}"
                documents.append(TaggedDocument(words=tokens, tags=[tag]))

    print(f"[+] Training on {len(documents)} path sequences...")
    model = Doc2Vec(documents, vector_size=128, window=5, min_count=1, workers=4, epochs=20)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    print(f"[+] Model trained and saved at {model_path}")


if __name__ == "__main__":
    train_doc2vec("outputs/paths", "models/api2vec.bin")