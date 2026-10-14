# ML Honors - Practical assignments

Neural networks and text analysis in Python 3.14 with pandas, scikit-learn and matplotlib. Every script starts with a docstring (problem statement, libraries, driver), runs without any input and saves its plots in `outputs/`.

## Run

```
cd ml-honors-code
uv sync
uv run python a3.py        # any script works the same way
```

The Kaggle datasets are not in git: download them first, as listed in [`data/README.md`](data/README.md). A script that cannot find its CSV stops with a message saying which file is missing.

| File | Assignment | Data | What it does |
|---|---|---|---|
| `a1.py` | 1. Create and visualize a neural network | `data/diabetes.csv` | Trains a small MLP (8-8-4-1), prints metrics, draws the loss curve and the network diagram |
| `a2.py` | 2. Optical character recognition with ANN | built into scikit-learn | Reads 8x8 handwritten digits with an MLP, prints accuracy and confusion matrix, saves sample predictions |
| `a3.py` | 3. Logic gates with Hebbnet | none | Hebb rule on bipolar AND, OR, NAND, NOR, and shows that XOR fails |
| `a4.py` | 4. Sentiment classification with KNN | `data/Tweets.csv` | TF-IDF + KNN on tweets, K chosen by cross-validation |
| `a5.py` | 5. Exploratory analysis of Twitter text | `data/Tweets.csv` | Statistics, text pre-processing, Zipf's law, Heaps' law and LDA topics |
| `a6.py` | 6. Positive / negative documents from polarity words | `data/Tweets.csv` | Naive Bayes on word counts compared with a hand-made polarity word list, lists strongest polarity words |

The numbers follow the assignment list (Sr. No 5 is the exploratory analysis and Sr. No 4 is the KNN classifier).

## Notes

- Keras and the ANN visualizer are not used. Networks are built with scikit-learn's `MLPClassifier` and the diagram in `a1.py` is drawn with matplotlib, so nothing beyond the four packages in `pyproject.toml` is needed.
- Scripts were tested on Python 3.13 with stand-in CSV files of the same format, not with the real Kaggle files.
