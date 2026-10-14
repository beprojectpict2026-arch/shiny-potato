# LP4 (410247) - Laboratory Practice IV

Solutions for Cyber Security & Digital Forensics (`csdf/`) and Information Retrieval (`ir/`).
Python 3.14, **standard library only** (no packages to install). Every script starts with a docstring (problem statement, libraries used, driver) and runs without any input.

## Run

```
cd lp4-code
uv run python csdf/a1.py        # any script works the same way
```

Without uv: `python csdf/a1.py` (Python 3.14).

## Cyber Security and Digital Forensics (`csdf/`)

| File | Assignment | What it does |
|---|---|---|
| `a1.py` | 1. Email tracking | Parses e-mail headers: relay route, SPF/DKIM/DMARC results, From / Return-Path / Reply-To mismatches (a genuine and a spoofed sample) |
| `a2.py` | 2. CAPTCHA | Generates a CAPTCHA PNG (`captcha_sample.png`) and verifies answers, with single use and limited attempts |
| `a3_a4_guide.md` | 3. Wi-Fi cracking detection, 4. Deleted file/partition recovery | Guide only (setup, hardware and tools needed), because both need real hardware or disks |
| `a5.py` | 5. Log capture and event correlation | Parses auth, firewall and web logs and correlates them by IP to raise alerts (brute force, port scan, SQL injection) |
| `mini_image_forensics.py` | Mini-project: image forensics | Hashes, metadata, editing-software traces, data hidden after the image end and in pixel LSBs, and original-vs-suspect comparison (PNG and JPEG) |

## Information Retrieval (`ir/`)

| File | Assignment | What it does |
|---|---|---|
| `a1.py` | 1. Text similarity | TF and TF-IDF cosine similarity and Jaccard similarity between documents |
| `a2.py` | 2. PageRank | Power-iteration PageRank (damping 0.85, dangling pages handled) on a 5-page graph |
| `a3.py` | 3. Map-reduce | Case-insensitive letter count with map, shuffle and reduce phases |
| `a4.py` | 4. Web crawler | Breadth-first crawler with a depth limit, run against a small local test site (no internet needed) |
| `a5.py` | 5. XML web graph | Parses XML pages into a web graph and computes ordinary and topic-specific PageRank |
| `mini_document_summarization.py` | Mini-project: summarization | Extractive summaries by word frequency and TextRank, with compression ratios |

## Notes

- All data in the scripts is embedded sample data, so results are repeatable.
- `csdf/a2.py` writes `captcha_sample.png` next to the script each time it runs.
