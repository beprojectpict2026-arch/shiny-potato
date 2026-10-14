"""Assignment 2 - Recognize optical characters (handwritten digits) using an ANN.

Problem statement: train a neural network to read 8x8 pixel images of handwritten
digits 0-9 (a small OCR task) and test how well it recognizes unseen images.
Libraries: scikit-learn (built-in digits dataset, MLPClassifier, metrics), matplotlib.
Driver: trains on 80% of 1797 images, prints accuracy and confusion matrix, saves
outputs/a2_predictions.png. No download needed, the dataset ships with scikit-learn.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

OUT = Path(__file__).parent / "outputs"


def main():
    OUT.mkdir(exist_ok=True)
    digits = load_digits()                              # each image is 8x8 = 64 pixel values (0-16)
    X = digits.data / 16.0                              # scale pixels to 0-1
    y = digits.target
    print(f"Images: {len(X)}, pixels per image: {X.shape[1]}, classes: {sorted(set(map(int, y)))}")

    X_train, X_test, y_train, y_test, img_train, img_test = train_test_split(
        X, y, digits.images, test_size=0.2, stratify=y, random_state=42)

    model = MLPClassifier(hidden_layer_sizes=(64,), max_iter=500, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print(f"\nTest accuracy: {accuracy_score(y_test, pred):.3f}")
    print("\nConfusion matrix (rows = true digit, columns = predicted digit):")
    print(confusion_matrix(y_test, pred))
    print()
    print(classification_report(y_test, pred))

    fig, axes = plt.subplots(2, 8, figsize=(12, 4))     # first 16 test images with their prediction
    for ax, image, true, guess in zip(axes.ravel(), img_test, y_test, pred):
        ax.imshow(image, cmap="gray_r")
        ax.set_title(f"pred {guess}" if guess == true else f"pred {guess} (true {true})",
                     color="green" if guess == true else "red", fontsize=9)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(OUT / "a2_predictions.png", dpi=120)
    plt.close()
    print("Saved outputs/a2_predictions.png")


if __name__ == "__main__":
    main()
