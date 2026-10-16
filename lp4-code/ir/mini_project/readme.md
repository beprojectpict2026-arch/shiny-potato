# Document Summarization System (IR mini-project)

A tool that shortens an article to its most important sentences (extractive summarization). It picks sentences from the original text and does not rewrite them. It uses **NLTK** for the text processing.

## How it works

1. **Split into sentences** (NLTK sentence tokenizer, which knows that "Dr." or "e.g." do not end a sentence).
2. **Clean the words** of each sentence: split into words, make lowercase, drop stop words ("the", "is", "of"), and reduce each word to its stem with the Porter stemmer ("searches" and "searching" both become "search").
3. **Score every sentence** in two ways:
   - **Word frequency:** words that appear many times in the article are important, so a sentence full of frequent words scores high.
   - **TextRank:** sentences that share words with many other sentences are important. This is PageRank (from the IR syllabus) applied to sentences instead of web pages: each sentence is a page, and word overlap is the link.
4. **Keep the top sentences** and print them in their original order.

The demo article has one off-topic sentence ("My neighbour bought a new bicycle last week."). It shares no words with the rest, so both methods leave it out.

## What NLTK does here

| NLTK part | Used for |
|---|---|
| `sent_tokenize` | splitting the article into sentences |
| `word_tokenize` | splitting a sentence into words |
| `stopwords` | the list of English stop words to ignore |
| `PorterStemmer` | reducing words to their stem so that word forms are counted together |

The first run downloads two small NLTK data packages (`punkt_tab` and `stopwords`), so it needs internet once. After that it works offline.

## Run it

```
cd lp4-code
uv sync
uv run python ir/mini_project/summarize.py       # prints both summaries
uv run pytest ir/mini_project -s                 # tests
```

To summarize another article, put a `.txt` file in `articles/` and set `article_path` (and `num_sentences`) at the top of `summarize.py`. A full path also works.

## Files

| File | Purpose |
|---|---|
| `summarizer.py` | The summarizer: sentence splitting, word cleaning, the two scoring methods |
| `summarize.py` | Runs it on `article_path` and prints both summaries with how much shorter they are |
| `test_summarizer.py` | pytest tests |
| `articles/` | Sample articles (`search_engines`, `electric_buses`, `online_learning`) |

## Limits

- It only picks existing sentences, so the summary can read a little choppy. Rewriting sentences in new words is abstractive summarization, which is a different mini-project.
- It works best on plain English articles of at least 6 to 8 sentences.
- There is no ground-truth summary to measure against, so quality is judged by reading the result.
