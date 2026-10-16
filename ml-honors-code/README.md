# ML Honors - Practical assignments

One Jupyter notebook per assignment. Each notebook starts with the name, roll no, problem statement, dataset and requirements, followed by the code, so that after running it can be exported as the PDF to submit.

| Notebook | Assignment | Data | Libraries |
|---|---|---|---|
| `a1.ipynb` | 1. Create and visualize a neural network | Pima Indians Diabetes (Kaggle) | Keras, ANN Visualizer, Graphviz |
| `a2.ipynb` | 2. Optical character recognition with ANN | MNIST digits (loaded by Keras) | Keras |
| `a3.ipynb` | 3. Logic gates with Hebbnet | none | plain Python |
| `a4.ipynb` | 4. Sentiment classification with KNN | Twitter US Airline Sentiment (Kaggle) | scikit-learn |
| `a5.ipynb` | 5. Exploratory analysis of Twitter text (pre-processing, Zipf, Heaps, topics) | Twitter US Airline Sentiment (Kaggle) | scikit-learn |
| `a6.ipynb` | 6. Positive / negative documents from polarity words | Twitter US Airline Sentiment (Kaggle) | scikit-learn |

The numbers follow the assignment list (Sr. No 5 is the exploratory analysis and Sr. No 4 is the KNN classifier).

## Run in Google Colab

1. Upload the notebook to [colab.research.google.com](https://colab.research.google.com) (File > Upload notebook).
2. Runtime > Run all. Datasets are downloaded by the first cells with `kagglehub`, nothing to upload.
3. Save as PDF with File > Print > Save as PDF, and use the Print dialog's option to keep outputs and plots.

## Notes

- Only `a3.ipynb` is saved with its output. The others need the Kaggle data or TensorFlow, so run them once to produce the outputs before exporting.
- `a1.ipynb` uses `ann_visualizer`, an old library that may fail on the newest Keras. If it does, the rest of the notebook is unaffected.
