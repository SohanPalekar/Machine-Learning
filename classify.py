# classify.py
from gensim.models.doc2vec import Doc2Vec
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import glob
import os

def load_sample_vectors(model, paths_dir):
    X, y = [], []
    for file in glob.glob(os.path.join(paths_dir, "*.txt")):
        label = 1 if "black" in file else 0
        seq_vectors = []
        with open(file, "r") as f:
            for line in f:
                seq = line.strip().split()
                seq_vectors.append(model.infer_vector(seq))
        if len(seq_vectors) > 0:
            avg_vec = np.mean(seq_vectors, axis=0)
            X.append(avg_vec)
            y.append(label)
    return np.array(X), np.array(y)


def train_classifier(model_path="models/api2vec.bin", paths_dir="outputs/paths"):
    model = Doc2Vec.load(model_path)
    X, y = load_sample_vectors(model, paths_dir)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    print(f"[+] Classification accuracy: {acc:.4f}")


if __name__ == "__main__":
    train_classifier()