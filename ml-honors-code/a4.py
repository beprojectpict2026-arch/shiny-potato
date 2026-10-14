"""Assignment 4 - Text classification for sentiment analysis using KNN (Twitter data).

Problem statement: classify tweets as positive / neutral / negative with the K-Nearest
Neighbours algorithm, choosing K by cross-validation.
Libraries: pandas (load CSV), scikit-learn (TfidfVectorizer, KNeighborsClassifier,
cross_val_score, metrics), re (text cleaning).
Driver: reads data/Tweets.csv (Kaggle "Twitter US Airline Sentiment"), prints accuracy
for several K, the final test report and predictions for a few new tweets.
"""

import re
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier

CSV_PATH = Path(__file__).parent / "data" / "Tweets.csv"
TEXT_COL, LABEL_COL = "text", "airline_sentiment"


def clean(text):
    """Lowercase, drop links, @mentions, '#' signs, digits and punctuation."""
    text = re.sub(r"http\S+|@\w+", " ", str(text).lower())
    return re.sub(r"[^a-z\s]", " ", text)


def main():
    if not CSV_PATH.exists():
        sys.exit(f"Dataset not found: {CSV_PATH}\nDownload it from Kaggle (see data/README.md).")

    data = pd.read_csv(CSV_PATH)[[TEXT_COL, LABEL_COL]].dropna()
    data[TEXT_COL] = data[TEXT_COL].map(clean)
    print(f"Tweets: {len(data)}")
    print(data[LABEL_COL].value_counts().to_string(), "\n")

    X_train, X_test, y_train, y_test = train_test_split(
        data[TEXT_COL], data[LABEL_COL], test_size=0.2, stratify=data[LABEL_COL], random_state=42)

    tfidf = TfidfVectorizer(stop_words="english", min_df=2, max_features=5000)
    X_train_vec = tfidf.fit_transform(X_train)          # words -> TF-IDF numbers
    X_test_vec = tfidf.transform(X_test)

    print("Choosing K with 3-fold cross-validation on the training set:")
    best_k, best_score = None, 0
    for k in (1, 3, 5, 7, 11, 15):
        knn = KNeighborsClassifier(n_neighbors=k, metric="cosine")
        score = cross_val_score(knn, X_train_vec, y_train, cv=3).mean()
        print(f"  K = {k:>2}: accuracy {score:.3f}")
        if score > best_score:
            best_k, best_score = k, score

    knn = KNeighborsClassifier(n_neighbors=best_k, metric="cosine").fit(X_train_vec, y_train)
    pred = knn.predict(X_test_vec)
    print(f"\nBest K = {best_k}. Test accuracy: {accuracy_score(y_test, pred):.3f}")
    print(classification_report(y_test, pred))

    samples = ["Great flight, the crew was lovely and friendly",
               "Worst airline ever, my bag was lost and the delay was awful",
               "What time does the flight to Delhi board"]
    for tweet, label in zip(samples, knn.predict(tfidf.transform([clean(t) for t in samples]))):
        print(f"{label:>9}  <-  {tweet}")


if __name__ == "__main__":
    main()
