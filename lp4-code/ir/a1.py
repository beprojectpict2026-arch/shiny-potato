"""IR Assignment 1 - Compute similarity between two text documents.

Problem statement: measure how similar two text documents are. The text is
tokenised, stop-words are removed, and the documents are compared with cosine
similarity (on raw term frequency and on TF-IDF weights) and Jaccard similarity.

New libs used (all standard library): re, math, collections.Counter.

Input: three text files (data/doc1.txt, doc2.txt, doc3.txt, set in doc_paths) are read and
compared pairwise. Change doc_paths to compare your own documents.
"""

import math
import re
from collections import Counter
from pathlib import Path

STOP_WORDS = {"a", "an", "the", "is", "are", "of", "in", "on", "to", "and", "for", "it", "that", "this", "with", "as", "by"}

# documents to compare (relative to this folder, full paths also work)
doc_paths = ["data/doc1.txt", "data/doc2.txt", "data/doc3.txt"]


def read_file(path):
    return (Path(__file__).parent / path).read_text(encoding="utf-8")


def tokenize(text):
    return [w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP_WORDS]


def cosine(v1, v2):
    dot = sum(v1[t] * v2.get(t, 0) for t in v1)
    norm = math.sqrt(sum(x * x for x in v1.values())) * math.sqrt(sum(x * x for x in v2.values()))
    return dot / norm if norm else 0.0


def jaccard(t1, t2):
    a, b = set(t1), set(t2)
    return len(a & b) / len(a | b)


def tfidf(docs_tokens):
    """TF-IDF vector (dict) for every document in the list."""
    n = len(docs_tokens)
    df = Counter(t for tokens in docs_tokens for t in set(tokens))
    vectors = []
    for tokens in docs_tokens:
        tf = Counter(tokens)
        vectors.append({t: (c / len(tokens)) * (math.log((1 + n) / (1 + df[t])) + 1) for t, c in tf.items()})
    return vectors


def compare(name, d1, d2):
    t1, t2 = tokenize(d1), tokenize(d2)
    tf_cos = cosine(Counter(t1), Counter(t2))
    v1, v2 = tfidf([t1, t2])
    print(f"{name}: TF cosine = {tf_cos:.3f} | TF-IDF cosine = {cosine(v1, v2):.3f} | Jaccard = {jaccard(t1, t2):.3f}")
    print(f"    common terms: {sorted(set(t1) & set(t2))}")


def main():
    d1, d2, d3 = (read_file(p) for p in doc_paths)
    compare("Doc1 vs Doc2 (same topic)     ", d1, d2)
    compare("Doc1 vs Doc3 (different topic)", d1, d3)
    compare("Doc1 vs Doc1 (identical)      ", d1, d1)


if __name__ == "__main__":
    main()
