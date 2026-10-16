# ML Honors - Practical assignments

One Jupyter notebook per assignment. Each notebook starts with the name, roll no, problem statement, dataset and requirements, followed by the code and its output, so it can be exported as the PDF to submit.

| Notebook | Assignment | Data | Libraries |
|---|---|---|---|
| `a1.ipynb` | 1. Create and visualize a neural network | `data/diabetes.csv` (Pima Indians Diabetes, Kaggle) | Keras, ANN Visualizer, Graphviz |
| `a2.ipynb` | 2. Optical character recognition with ANN | MNIST digits (loaded by Keras) | Keras |
| `a3.ipynb` | 3. Logic gates with Hebbnet | none | plain Python |
| `a4.ipynb` | 4. Sentiment classification with KNN | `data/Tweets.csv` (Twitter US Airline Sentiment, Kaggle) | scikit-learn |
| `a5.ipynb` | 5. Exploratory analysis of Twitter text (pre-processing, Zipf, Heaps, topics) | `data/Tweets.csv` | scikit-learn |
| `a6.ipynb` | 6. Positive / negative documents from polarity words | `data/Tweets.csv` | scikit-learn |

The numbers follow the assignment list (Sr. No 5 is the exploratory analysis and Sr. No 4 is the KNN classifier).

## Data

The two CSV files are not stored in git. Download them from Kaggle and save them as `data/diabetes.csv` and `data/Tweets.csv` inside this folder. The notebooks read them with the relative path `data/...`, so open each notebook from this folder (in Colab, upload the CSVs into a `data` folder first).

## Export to PDF

Run all cells, then print the notebook to PDF from the browser or editor (outputs and plots are kept).

## Notes

- `a3` to `a6` are saved with their output. `a1` needs TensorFlow, so run it once before exporting.
- `a1` uses `ann_visualizer`, an old library that may fail on the newest Keras. If it does, the rest of the notebook is unaffected.
