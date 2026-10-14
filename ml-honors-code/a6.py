"""Assignment 6 - Recognize whether a document is positive or negative using polarity words.

Problem statement: classify documents as positive or negative from their polarity
words. Method: Multinomial Naive Bayes on word counts, which learns how strongly each
word points to a class; compared with a simple hand-made polarity word list.
Libraries: pandas (CSV), scikit-learn (CountVectorizer, MultinomialNB, metrics), re.
Driver: reads data/Tweets.csv (Kaggle "Twitter US Airline Sentiment", neutral rows
dropped), prints both accuracies, the strongest learned polarity words and examples.
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

CSV_PATH = Path(__file__).parent / "data" / "Tweets.csv"
TEXT_COL, LABEL_COL = "text", "airline_sentiment"

POSITIVE_WORDS = {"good", "great", "best", "love", "thanks", "thank", "awesome", "excellent",
                  "amazing", "happy", "friendly", "smooth", "helpful", "wonderful", "perfect"}
NEGATIVE_WORDS = {"bad", "worst", "late", "delayed", "delay", "lost", "cancelled", "rude",
                  "terrible", "awful", "horrible", "angry", "never", "broken", "waiting"}


def clean(text):
    text = re.sub(r"http\S+|@\w+", " ", str(text).lower())
    return re.sub(r"[^a-z\s]", " ", text)


def lexicon_label(text):
    """Baseline: count positive and negative words from the lists above."""
    words = text.split()
    score = sum(w in POSITIVE_WORDS for w in words) - sum(w in NEGATIVE_WORDS for w in words)
    return "positive" if score > 0 else "negative"   # ties go to negative (the majority class)


def main():
    if not CSV_PATH.exists():
        sys.exit(f"Dataset not found: {CSV_PATH}\nDownload it from Kaggle (see data/README.md).")

    data = pd.read_csv(CSV_PATH)[[TEXT_COL, LABEL_COL]].dropna()
    data = data[data[LABEL_COL].isin(["positive", "negative"])]
    data[TEXT_COL] = data[TEXT_COL].map(clean)
    print(f"Documents: {len(data)}")
    print(data[LABEL_COL].value_counts().to_string(), "\n")

    X_train, X_test, y_train, y_test = train_test_split(
        data[TEXT_COL], data[LABEL_COL], test_size=0.2, stratify=data[LABEL_COL], random_state=42)

    baseline = X_test.map(lexicon_label)
    print(f"Word-list baseline accuracy : {accuracy_score(y_test, baseline):.3f}")

    vectorizer = CountVectorizer(stop_words="english", min_df=2, binary=True)
    model = MultinomialNB().fit(vectorizer.fit_transform(X_train), y_train)
    pred = model.predict(vectorizer.transform(X_test))
    print(f"Naive Bayes accuracy        : {accuracy_score(y_test, pred):.3f}\n")
    print(classification_report(y_test, pred))

    # polarity of a word = how much more likely it is in positive than in negative documents
    vocab = vectorizer.get_feature_names_out()
    polarity = model.feature_log_prob_[list(model.classes_).index("positive")] \
        - model.feature_log_prob_[list(model.classes_).index("negative")]
    order = np.argsort(polarity)
    print("Most negative words:", ", ".join(vocab[order[:10]]))
    print("Most positive words:", ", ".join(vocab[order[::-1][:10]]))

    print()
    for doc in ["The crew was friendly and the flight was perfect, thank you",
                "Terrible service, delayed for hours and my bag was lost"]:
        label = model.predict(vectorizer.transform([clean(doc)]))[0]
        print(f"{label:>8}  <-  {doc}")


if __name__ == "__main__":
    main()
