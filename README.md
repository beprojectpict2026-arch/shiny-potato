# SEM7 Practicals

B.E. Computer Engineering, Semester I (2026-27), Pune Institute of Computer Technology.
Lab manuals and solutions for Laboratory Practice III and IV.

## Contents

| Path | What it is |
|---|---|
| [`lab_manual_lp3.pdf`](lab_manual_lp3.pdf) | LP III manual: DAA, Machine Learning, Blockchain Technology |
| [`lab_manual_lp4.pdf`](lab_manual_lp4.pdf) | LP IV schedule: Cyber Security & Digital Forensics, Information Retrieval |
| [`lp3-code/`](lp3-code) | LP III solutions: `daa/` (C++), `ml/` (Jupyter notebooks), `bt/` (Solidity) |
| [`lp4-code/`](lp4-code) | LP IV solutions: `csdf/` and `ir/` (Python) |
| [`ml-honors-code/`](ml-honors-code) | ML honors solutions: neural networks, Hebbnet, Twitter text analysis (Python, Kaggle data) |

Each folder has its own file layout and run instructions: see the README inside each folder. Every program starts with a short comment or docstring (problem statement, libraries used, driver), and none of them asks for input while running.

## LP IV (Python; standard library only, except `ir/a4` uses Scrapy)

```
cd lp4-code
uv run python csdf/a1.py        # run any script the same way
```

| Subject | Files |
|---|---|
| Cyber Security & Digital Forensics (`csdf/`) | `a1` email header analysis, `a2` CAPTCHA, `a5` log correlation, `mini_image_forensics` image forensics tool; `a3_a4_guide.md` explains Wi-Fi attack detection and file/partition recovery (hardware needed, so no code) |
| Information Retrieval (`ir/`) | `a1` text similarity, `a2` PageRank, `a3` map-reduce character count, `a4` web crawler (Scrapy), `a5` XML web graph + topic-specific PageRank, `mini_document_summarization` |

## LP III

| Subject | Language | Run |
|---|---|---|
| `daa/` Design and Analysis of Algorithms | C++17 | `g++ -std=c++17 -O2 a1.cpp -o a1 && ./a1` |
| `ml/` Machine Learning | Jupyter notebooks | `uv sync`, then `uv run jupyter lab` |
| `bt/` Blockchain Technology | Solidity (Remix IDE + MetaMask) | open the `.sol` file in [Remix](https://remix.ethereum.org) |

## Adding more work

Put each subject's code in its own folder at the top level (for example `lp5-code/`) and add a row to the table above.
