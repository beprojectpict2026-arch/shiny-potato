# LP4 (410247) - Laboratory Practice IV

Solutions for Cyber Security & Digital Forensics (`csdf/`) and Information Retrieval (`ir/`).
Python 3.14, standard library only, except `ir/a4.py` and `ir/a4_real_site.py` which use **Scrapy**, and the IR mini-project which uses **NLTK**. Every script starts with a docstring (problem statement, libraries used, input) and runs without any typing. Scripts that analyse a document read it from a `data/` folder next to them (`csdf/data/`, `ir/data/`); change the path variable at the top to use your own file.

## Run

```
cd lp4-code
uv run python csdf/a1.py        # any script works the same way
```

Without uv: `python csdf/a1.py` (Python 3.14). For the crawlers run `uv sync` first (or `pip install scrapy`).

## Cyber Security and Digital Forensics (`csdf/`)

| File | Assignment | What it does |
|---|---|---|
| `a1.py` | 1. Email tracking | Parses e-mail headers: relay route, SPF/DKIM/DMARC results, From / Return-Path / Reply-To mismatches (a genuine and a spoofed sample) |
| `a2.py` | 2. CAPTCHA | Generates a CAPTCHA PNG (`captcha_sample.png`) and verifies answers, with single use and limited attempts |
| `a3_a4_guide.md` | 3. Wi-Fi cracking detection, 4. Deleted file/partition recovery | Guide only (setup, hardware and tools needed), because both need real hardware or disks |
| `a5.py` | 5. Log capture and event correlation | Parses auth, firewall and web logs and correlates them by IP to raise alerts (brute force, port scan, SQL injection) |
| `mini_project/` | Mini-project: image forensics | Hashes, metadata, editing-software traces, data hidden after the image end and in pixel LSBs, original-vs-suspect comparison. Web page (`web_app.py` + `index.html`), pytest file (`test_forensics.py`) and an `images/` folder |

## Information Retrieval (`ir/`)

| File | Assignment | What it does |
|---|---|---|
| `a1.py` | 1. Text similarity | TF and TF-IDF cosine similarity and Jaccard similarity between documents |
| `a2.py` | 2. PageRank | Power-iteration PageRank (damping 0.85, dangling pages handled) on a 5-page graph |
| `a3.py` | 3. Map-reduce | Case-insensitive letter count with map, shuffle and reduce phases |
| `a4.py` | 4. Web crawler | Scrapy spider: breadth-first, depth limit, same-site only, run against a small local test site (no internet needed) |
| `a4_real_site.py` | 4. Web crawler (real site) | Same spider for a live website: robots.txt respected, polite delay, page limit, saves `pages.json` (needs internet) |
| `a5.py` | 5. XML web graph | Parses XML pages into a web graph and computes ordinary and topic-specific PageRank |
| `mini_project/` | Mini-project: summarization | NLTK-based extractive summaries by word frequency and TextRank on text files in `articles/`, with compression ratios and pytest tests |

## Image forensics mini-project (`csdf/mini_project/`)

```
cd lp4-code
uv run python csdf/mini_project/web_app.py        # web page at http://localhost:8000, Ctrl+C to stop
uv run pytest csdf/mini_project -s                # tests; set image_path in test_forensics.py to try your own image
```

Uploads from the web page are saved in `csdf/mini_project/images/`. Without uv: `python csdf/mini_project/web_app.py` and `pip install pytest`, then `python -m pytest csdf/mini_project -s`.

## Document summarization mini-project (`ir/mini_project/`)

```
cd lp4-code
uv sync
uv run python ir/mini_project/summarize.py       # set article_path at the top to use another .txt file
uv run pytest ir/mini_project -s
```

The first run downloads two small NLTK data packages (`punkt_tab`, `stopwords`), so it needs internet once.

## Notes

- Input files: `csdf/a1.py` reads `csdf/data/*.eml`, `csdf/a5.py` reads `csdf/data/sample.log`, `ir/a1.py` reads `ir/data/doc*.txt`, `ir/a2.py` reads `ir/data/graph.txt`, `ir/a3.py` reads `ir/data/dataset.txt`, `ir/a5.py` reads `ir/data/pages.xml`. The sample files are fixed, so results are repeatable.
- `csdf/a2.py`, `ir/a4.py` and `ir/a4_real_site.py` need no input file (a seed, a built-in demo site and a URL).
- `ir/a4_real_site.py` writes `pages.json` in the folder you run it from.
- `csdf/a2.py` writes `captcha_sample.png` next to the script each time it runs.
