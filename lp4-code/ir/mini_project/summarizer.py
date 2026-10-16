"""IR Mini-project - document summarization system using NLTK.

Problem statement: shorten an article to its most important sentences. Sentences are scored by word
frequency and by TextRank (PageRank over a sentence-similarity graph); the top ones are kept in order.
Libs used: nltk (sentence and word tokenizer, English stop words, Porter stemmer), math, collections.Counter.
The first run downloads two small NLTK data packages (punkt_tab, stopwords), so it needs internet once.
"""

import math
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

RESOURCES = {"punkt_tab": "tokenizers/punkt_tab", "stopwords": "corpora/stopwords"}


def setup_nltk():
    for name, path in RESOURCES.items():
        try:
            nltk.data.find(path)
        except LookupError:
            if not nltk.download(name, quiet=True):
                raise RuntimeError(f"NLTK data '{name}' is missing and could not be downloaded. Connect to the internet and run again.")


setup_nltk()
STOP_WORDS = set(stopwords.words("english"))
stemmer = PorterStemmer()


def split_sentences(text):
    return [s.strip() for s in sent_tokenize(" ".join(text.split())) if s.strip()]


def words(sentence):
    tokens = word_tokenize(sentence.lower())
    return [stemmer.stem(w) for w in tokens if w.isalpha() and w not in STOP_WORDS]


def frequency_scores(sentences):
    """Score = average normalised frequency of a sentence's words in the whole document."""
    freq = Counter(w for s in sentences for w in words(s))
    if not freq:
        return [0] * len(sentences)
    top = max(freq.values())
    scores = []
    for s in sentences:
        ws = words(s)
        scores.append(sum(freq[w] / top for w in ws) / len(ws) if ws else 0)
    return scores


def similarity(a, b):
    """Normalised word-overlap similarity between two sentences (TextRank edge weight)."""
    wa, wb = set(words(a)), set(words(b))
    if len(wa) < 2 or len(wb) < 2:
        return 0.0
    return len(wa & wb) / (math.log(len(wa)) + math.log(len(wb)))


def textrank_scores(sentences, d=0.85, iterations=50):
    n = len(sentences)
    weight = [[similarity(sentences[i], sentences[j]) if i != j else 0 for j in range(n)] for i in range(n)]
    out_sum = [sum(row) for row in weight]
    score = [1 / n] * n
    for _ in range(iterations):
        score = [
            (1 - d) / n + d * sum(weight[j][i] / out_sum[j] * score[j] for j in range(n) if out_sum[j])
            for i in range(n)
        ]
    return score


def summarize(text, count, method):
    sentences = split_sentences(text)
    if not sentences:
        return []
    scores = textrank_scores(sentences) if method == "textrank" else frequency_scores(sentences)
    best = sorted(sorted(range(len(sentences)), key=lambda i: -scores[i])[:count])
    return [sentences[i] for i in best]
