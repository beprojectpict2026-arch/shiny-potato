"""IR Mini-project - pytest tests for the document summarizer.

Run `pytest -s test_summarizer.py` to also see the summaries printed. The tests check the summary length,
that sentences stay in their original order, that an off-topic sentence is left out, and every article in articles/.
Libs used: pytest, plus summarizer.py (which uses nltk).
"""

from pathlib import Path

import pytest

from summarizer import split_sentences, summarize

ARTICLES = sorted((Path(__file__).parent / "articles").glob("*.txt"))
METHODS = ("frequency", "textrank")


def read(name):
    return (Path(__file__).parent / "articles" / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("method", METHODS)
def test_summary_has_requested_length(method):
    assert len(summarize(read("search_engines.txt"), 3, method)) == 3


@pytest.mark.parametrize("method", METHODS)
def test_sentences_keep_original_order(method):
    text = read("search_engines.txt")
    sentences = split_sentences(text)
    positions = [sentences.index(s) for s in summarize(text, 3, method)]
    assert positions == sorted(positions)


@pytest.mark.parametrize("method", METHODS)
def test_off_topic_sentence_is_left_out(method):
    summary = " ".join(summarize(read("search_engines.txt"), 3, method))
    assert "bicycle" not in summary


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("article", ARTICLES, ids=lambda p: p.name)
def test_every_article_gets_shorter(article, method):
    text = article.read_text(encoding="utf-8")
    summary = summarize(text, 3, method)
    assert 0 < len(" ".join(summary).split()) < len(text.split())


def test_asking_for_more_sentences_than_exist():
    text = "Search engines index web pages. Ranking uses links."
    assert len(summarize(text, 5, "frequency")) == 2


def test_empty_text():
    assert summarize("", 3, "textrank") == []
