"""train.py — Training pipeline. Run once to generate model artefacts.

Dataset:
  Download True.csv and Fake.csv from:
  https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
  Place both files in the data/ folder before running.

Usage:
  python train.py
"""
import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from preprocess import clean_text

os.makedirs("model", exist_ok=True)

print("[1/5] Loading datasets from data/ ...")
real = pd.read_csv("data/True.csv")
fake = pd.read_csv("data/Fake.csv")
real["label"] = 1   # 1 = Real
fake["label"] = 0   # 0 = Fake
df = pd.concat([real, fake], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print(f"      Total: {len(df):,} samples | Real: {real.shape[0]:,} | Fake: {fake.shape[0]:,}")

print("[2/5] Preprocessing text (title + body) ...")
df["content"] = (df["title"].fillna("") + " " +
                 df["text"].fillna("")).apply(clean_text)

print("[3/5] Stratified 80/20 split ...")
X_tr, X_te, y_tr, y_te = train_test_split(
    df["content"], df["label"],
    test_size=0.20, stratify=df["label"], random_state=42)
print(f"      Train: {len(X_tr):,} | Test: {len(X_te):,}")

print("[4/5] Fitting TF-IDF vectoriser on training data only ...")
vec = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    min_df=2)
X_tr_v = vec.fit_transform(X_tr)
X_te_v = vec.transform(X_te)   # transform only — no fit on test data

print("[5/5] Training Passive-Aggressive Classifier ...")
model = PassiveAggressiveClassifier(C=0.1, max_iter=50, random_state=42)
model.fit(X_tr_v, y_tr)

# Evaluation
y_pred = model.predict(X_te_v)
print("\n" + "="*55)
print("  EVALUATION RESULTS")
print("="*55)
print(f"  Accuracy : {accuracy_score(y_te, y_pred):.4f}")
print("\n  Classification Report:")
print(classification_report(y_te, y_pred, target_names=["Fake (0)", "Real (1)"]))
print("  Confusion Matrix:")
print(confusion_matrix(y_te, y_pred))
print("="*55)

# Save artefacts
joblib.dump(model, "model/pac_model.joblib")
joblib.dump(vec,   "model/tfidf_vectorizer.joblib")
print("\n  Saved: model/pac_model.joblib")
print("  Saved: model/tfidf_vectorizer.joblib")
