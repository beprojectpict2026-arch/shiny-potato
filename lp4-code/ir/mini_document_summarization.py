"""IR Mini-project - Document summarization system.

Problem statement: build an extractive summarizer that condenses a document into its
most important sentences. Sentences are scored with two methods - word-frequency scoring
and TextRank (PageRank over a sentence-similarity graph) - and the top sentences are
returned in their original order. The two summaries are compared with the original.

New libs used (all standard library): re (sentence/word splitting), math,
collections.Counter. No external NLP packages or model downloads.

Driver: an embedded article is summarized to 3 sentences with both methods and the
compression ratios are printed. No input is taken at runtime.
"""

import math
import re
from collections import Counter

STOP_WORDS = set(
    "a an the is are was were be been of in on at to and or for from it its that this these those with as by "
    "has have had not but also can may will more most such their they which who into than then so if".split()
)

ARTICLE = """
Search engines have changed the way people find information on the internet. A search engine crawls billions of
web pages and stores them in a large index. When a user types a query, the search engine matches the query with
the indexed pages and ranks the results by relevance. Ranking algorithms such as PageRank use the link structure
of the web to estimate the importance of each page. Pages that are linked from many important pages receive a
higher rank. Modern search engines also use machine learning to understand the intent behind a query. My
neighbour bought a new bicycle last week. Evaluation of a search engine is done with measures such as precision
and recall, which compare the retrieved documents with the documents that are actually relevant. Summarization
helps users because it shows the key points of a long document in a few sentences, saving the reading time of the
user. Extractive summarization selects the most important sentences from the original text without rewriting them.
"""


def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if s.strip()]


def words(sentence):
    return [w for w in re.findall(r"[a-z]+", sentence.lower()) if w not in STOP_WORDS]


def frequency_scores(sentences):
    """Score = average normalised frequency of a sentence's words in the whole document."""
    freq = Counter(w for s in sentences for w in words(s))
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
    scores = textrank_scores(sentences) if method == "textrank" else frequency_scores(sentences)
    best = sorted(sorted(range(len(sentences)), key=lambda i: -scores[i])[:count])  # keep original order
    return [sentences[i] for i in best]


def main():
    original_words = len(ARTICLE.split())
    print(f"Original: {len(split_sentences(ARTICLE))} sentences, {original_words} words\n")
    for method in ("frequency", "textrank"):
        summary = summarize(ARTICLE, 3, method)
        size = sum(len(s.split()) for s in summary)
        print(f"--- {method} summary ({size} words, {size / original_words:.0%} of original) ---")
        for sentence in summary:
            print("  *", sentence)
        print()


if __name__ == "__main__":
    main()
