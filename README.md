# Veritas AI — Fake News & Clickbait Detection

> A lightweight, CPU-only system that classifies news articles as **real or fake** and computes a **Clickbait Score** that measures how far a headline drifts from its article body.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?logo=scikitlearn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F5B)
![Accuracy](https://img.shields.io/badge/accuracy-93.7%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Results

| Metric | Value |
|---|---|
| Accuracy (held-out test, 8,980 articles) | **93.7%** |
| Macro F1-score | **0.937** |
| ROC-AUC | **0.981** |
| Clickbait module macro F1 (500 annotated pairs) | **88.3%** |
| Inference | CPU only, no GPU required |

Transformer models reach 95–97%, but they need GPUs and 400 MB+ of weights. Veritas AI trades 2–3 points of accuracy for a **~42× speed-up** and runs on any laptop or shared host.

## How it works

```
Article (title + body)
   │
   ├─► clean_text()  ── lowercase, strip URLs/punctuation, stop-words (NLTK)
   │
   ├─► TF-IDF (5,000 features, uni+bi-grams, sublinear tf)
   │        └─► Passive-Aggressive Classifier (C=0.1) ──► REAL / FAKE + confidence
   │
   └─► Clickbait Score = 1 − cosine(TF-IDF(headline), TF-IDF(first 100 words of body))
            0.00–0.30 LOW · 0.30–0.60 MODERATE · 0.60–1.00 HIGH
```

Most tools solve only one of these problems. Veritas AI combines a **veracity verdict** and **headline–body coherence** in a single inference pipeline.

## Project structure

```
├── app.py               # Flask web app (single-page UI + /predict endpoint)
├── train.py             # Load data → preprocess → stratified 80/20 split → TF-IDF → PAC → evaluate
├── predict.py           # classify_article(title, body) → verdict, confidence, clickbait score
├── preprocess.py        # Text cleaning
├── clickbait_scorer.py  # Cosine-dissimilarity clickbait module
├── model/               # Trained artefacts (pac_model.joblib, tfidf_vectorizer.joblib)
└── data/README.md       # How to get the dataset
```

## Getting started

```bash
git clone https://github.com/ZakariaHibaoui2/fake-news-detector.git
cd fake-news-detector
pip install -r requirements.txt
python app.py            # → http://127.0.0.1:5000  (uses the pre-trained model in model/)
```

**Retrain from scratch**: download the [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset) (44,898 articles: 21,417 real from Reuters and 23,481 fake), place `True.csv` and `Fake.csv` in `data/`, then:

```bash
python train.py
```

## Author

**Zakaria Hibaoui** — [GitHub](https://github.com/ZakariaHibaoui2) · [LinkedIn](https://www.linkedin.com/in/zakaria-hibaoui-08b235337/)
AI project, INTI International University, Malaysia (2026).

## License

[MIT](LICENSE)
