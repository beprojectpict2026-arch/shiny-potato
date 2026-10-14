"""Assignment 5 - Exploratory analysis on Twitter text data.

Problem statement: explore a tweet dataset, pre-process the text, check Zipf's law
(word frequency vs rank) and Heaps' law (vocabulary size vs number of words) and
identify topics.
Libraries: pandas (CSV, counts), numpy (log-log line fit), matplotlib (plots),
scikit-learn (stop-word list, CountVectorizer, LatentDirichletAllocation for topics).
Driver: reads data/Tweets.csv (Kaggle "Twitter US Airline Sentiment"), prints the
statistics and topics, saves outputs/a5_zipf.png and outputs/a5_heaps.png.
"""

import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer

HERE = Path(__file__).parent
CSV_PATH = HERE / "data" / "Tweets.csv"
TEXT_COL, LABEL_COL = "text", "airline_sentiment"
OUT = HERE / "outputs"
N_TOPICS = 5


def preprocess(text):
    """Lowercase, remove links/@mentions/punctuation/digits, return a list of words."""
    text = re.sub(r"http\S+|@\w+", " ", str(text).lower())
    return re.sub(r"[^a-z\s]", " ", text).split()


def zipf_law(words):
    """Rank-frequency table; Zipf's law says frequency ~ 1 / rank (slope ~ -1 on log-log)."""
    freqs = np.array(sorted(Counter(words).values(), reverse=True))
    ranks = np.arange(1, len(freqs) + 1)
    slope, intercept = np.polyfit(np.log(ranks), np.log(freqs), 1)
    plt.figure(figsize=(6, 4))
    plt.loglog(ranks, freqs, label="data")
    plt.loglog(ranks, np.exp(intercept) * ranks ** slope, "--", label=f"fit, slope = {slope:.2f}")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.title("Zipf's law")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "a5_zipf.png", dpi=120)
    plt.close()
    return slope


def heaps_law(words):
    """Vocabulary growth; Heaps' law says V = K * n^beta with beta usually 0.4 to 0.7."""
    seen, vocab_size = set(), []
    for word in words:
        seen.add(word)
        vocab_size.append(len(seen))
    n = np.arange(1, len(words) + 1)
    beta, log_k = np.polyfit(np.log(n), np.log(vocab_size), 1)
    plt.figure(figsize=(6, 4))
    plt.plot(n, vocab_size, label="data")
    plt.plot(n, np.exp(log_k) * n ** beta, "--", label=f"fit, K = {np.exp(log_k):.1f}, beta = {beta:.2f}")
    plt.xlabel("Words read (n)")
    plt.ylabel("Vocabulary size (V)")
    plt.title("Heaps' law")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "a5_heaps.png", dpi=120)
    plt.close()
    return np.exp(log_k), beta


def main():
    if not CSV_PATH.exists():
        sys.exit(f"Dataset not found: {CSV_PATH}\nDownload it from Kaggle (see data/README.md).")
    OUT.mkdir(exist_ok=True)

    data = pd.read_csv(CSV_PATH)
    tweets = data[TEXT_COL].dropna()

    print("== 1. Basic exploration ==")
    print(f"Tweets: {len(tweets)}, columns: {list(data.columns)[:6]}...")
    if LABEL_COL in data:
        print(data[LABEL_COL].value_counts().to_string())
    print(f"Average length: {tweets.str.len().mean():.0f} characters, "
          f"{tweets.str.split().str.len().mean():.1f} words")

    print("\n== 2. Pre-processing ==")
    print("Original :", tweets.iloc[0])
    tokens = [preprocess(t) for t in tweets]
    print("Cleaned  :", " ".join(tokens[0]))
    all_words = [w for t in tokens for w in t]
    no_stop = [w for w in all_words if w not in ENGLISH_STOP_WORDS and len(w) > 2]
    print(f"Words: {len(all_words)} -> {len(no_stop)} after removing stop words and 1-2 letter words")
    print("Top 10 words:", Counter(no_stop).most_common(10))

    print("\n== 3. Zipf's law ==")
    print(f"Log-log slope = {zipf_law(all_words):.2f} (close to -1 means Zipf's law holds)")

    print("\n== 4. Heaps' law ==")
    k, beta = heaps_law(all_words)
    print(f"V = K * n^beta with K = {k:.1f}, beta = {beta:.2f}")

    print("\n== 5. Topics (LDA) ==")
    vectorizer = CountVectorizer(stop_words="english", min_df=5, max_df=0.5,
                                 token_pattern=r"[a-z]{3,}")
    counts = vectorizer.fit_transform(" ".join(t) for t in tokens)
    lda = LatentDirichletAllocation(n_components=N_TOPICS, random_state=42).fit(counts)
    vocab = vectorizer.get_feature_names_out()
    for i, weights in enumerate(lda.components_):
        print(f"Topic {i + 1}: {', '.join(vocab[weights.argsort()[::-1][:8]])}")
    print("\nSaved outputs/a5_zipf.png and outputs/a5_heaps.png")


if __name__ == "__main__":
    main()
