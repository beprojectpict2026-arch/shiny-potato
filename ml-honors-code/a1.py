"""Assignment 1 - Create and visualize a neural network for the given data.

Problem statement: train a small feed-forward neural network on a Kaggle tabular
dataset (Pima Indians Diabetes) and visualize both the network and its training.
Libraries: pandas (load CSV), scikit-learn (MLPClassifier, scaling, metrics),
matplotlib (loss curve + network diagram drawn with plain circles and lines).
Driver: reads data/diabetes.csv, trains, prints metrics, saves 2 PNGs in outputs/.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save figures to files, no window needed
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
CSV_PATH = HERE / "data" / "diabetes.csv"   # Kaggle: "Pima Indians Diabetes Database"
TARGET = "Outcome"                           # column to predict (0 / 1)
HIDDEN_LAYERS = (8, 4)                       # neurons in each hidden layer
OUT = HERE / "outputs"


def draw_network(model, n_inputs, path):
    """Draw the layers as circles; edge colour = weight sign, thickness = weight size."""
    sizes = [n_inputs, *model.hidden_layer_sizes, 1]
    ys = {i: [(n - 1) / 2 - j for j in range(n)] for i, n in enumerate(sizes)}
    biggest = max(abs(w).max() for w in model.coefs_)

    fig, ax = plt.subplots(figsize=(9, 6))
    for i, weights in enumerate(model.coefs_):          # edges first, nodes on top
        for a in range(weights.shape[0]):
            for b in range(weights.shape[1]):
                w = weights[a, b]
                ax.plot([i, i + 1], [ys[i][a], ys[i + 1][b]],
                        color="tab:blue" if w > 0 else "tab:red",
                        linewidth=0.2 + 2.5 * abs(w) / biggest, alpha=0.6, zorder=1)
    for i, n in enumerate(sizes):
        ax.scatter([i] * n, ys[i], s=350, color="white", edgecolor="black", zorder=2)
    names = ["Input"] + [f"Hidden {k + 1}" for k in range(len(sizes) - 2)] + ["Output"]
    for i, name in enumerate(names):
        ax.text(i, max(ys[0]) + 0.9, f"{name}\n({sizes[i]})", ha="center")
    ax.set_title("Neural network (blue = positive weight, red = negative weight)", pad=30)
    ax.axis("off")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def main():
    if not CSV_PATH.exists():
        sys.exit(f"Dataset not found: {CSV_PATH}\nDownload it from Kaggle (see data/README.md).")
    OUT.mkdir(exist_ok=True)

    data = pd.read_csv(CSV_PATH)
    X, y = data.drop(columns=[TARGET]), data[TARGET]
    print(f"Data: {X.shape[0]} rows, {X.shape[1]} features -> target '{TARGET}'")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    scaler = StandardScaler().fit(X_train)             # neural networks need scaled inputs
    X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

    model = MLPClassifier(hidden_layer_sizes=HIDDEN_LAYERS, activation="relu",
                          max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    print("\nLayer sizes:", [X.shape[1], *HIDDEN_LAYERS, 1])
    for i, w in enumerate(model.coefs_):
        print(f"  weights layer {i + 1}: {w.shape}")
    print(f"Training stopped after {model.n_iter_} iterations, final loss {model.loss_:.4f}")

    pred = model.predict(X_test)
    print(f"\nTest accuracy: {accuracy_score(y_test, pred):.3f}")
    print(classification_report(y_test, pred))

    plt.figure(figsize=(6, 4))
    plt.plot(model.loss_curve_)
    plt.xlabel("Iteration")
    plt.ylabel("Training loss")
    plt.title("Loss curve")
    plt.tight_layout()
    plt.savefig(OUT / "a1_loss_curve.png", dpi=120)
    plt.close()
    draw_network(model, X.shape[1], OUT / "a1_network.png")
    print("Saved outputs/a1_loss_curve.png and outputs/a1_network.png")


if __name__ == "__main__":
    main()
