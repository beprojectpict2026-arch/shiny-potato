"""IR Mini-project - run the document summarizer on a text file.

Set article_path (a .txt file in articles/, or a full path) and num_sentences below, then run this file.
It prints the summary made by word frequency and by TextRank, and how much shorter each one is.
Libs used: pathlib, plus summarizer.py (which uses nltk).
"""

from pathlib import Path

from summarizer import split_sentences, summarize

FOLDER = Path(__file__).parent

article_path = "articles/search_engines.txt"
num_sentences = 3


def main():
    path = FOLDER / article_path
    if not path.exists():
        print("File not found:", path)
        return
    text = path.read_text(encoding="utf-8")
    original_words = len(text.split())
    print(f"{path.name}: {len(split_sentences(text))} sentences, {original_words} words\n")
    for method in ("frequency", "textrank"):
        summary = summarize(text, num_sentences, method)
        size = sum(len(s.split()) for s in summary)
        print(f"--- {method} summary ({size} words, {size / original_words:.0%} of original) ---")
        for sentence in summary:
            print("  *", sentence)
        print()


if __name__ == "__main__":
    main()
