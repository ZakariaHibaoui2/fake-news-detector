"""predict.py — Inference module used by Flask.

Loads serialised PAC model and TF-IDF vectoriser, then runs
full Veritas AI dual-module inference on a given article.

Usage (standalone test):
  python predict.py
"""
import os
import math
import joblib
from preprocess import clean_text
from clickbait_scorer import clickbait_score

MODEL_PATH = os.path.join("model", "pac_model.joblib")
VEC_PATH   = os.path.join("model", "tfidf_vectorizer.joblib")


def load_artefacts():
    """Load serialised model and vectoriser."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run train.py first.")
    return joblib.load(MODEL_PATH), joblib.load(VEC_PATH)


def classify_article(title: str, body: str) -> dict:
    """Run Veritas AI dual-module inference.

    Args:
        title: Article headline.
        body:  Article body text.

    Returns:
        dict with keys:
            verdict    -- "REAL" or "FAKE"
            confidence -- float [0, 1]
            cb_score   -- float [0, 1]
            cb_risk    -- "LOW" | "MODERATE" | "HIGH"
    """
    model, vec = load_artefacts()

    # Module A: Veracity classification
    content    = clean_text(title + " " + body)
    vector     = vec.transform([content])
    prediction = model.predict(vector)[0]
    raw_score  = model.decision_function(vector)[0]
    confidence = 1 / (1 + math.exp(-abs(raw_score)))  # sigmoid

    # Module B: Clickbait scoring
    cb_score, cb_risk = clickbait_score(title, body)

    return {
        "verdict"   : "REAL" if prediction == 1 else "FAKE",
        "confidence": round(confidence, 4),
        "cb_score"  : cb_score,
        "cb_risk"   : cb_risk,
    }


if __name__ == "__main__":
    test_title = "Aliens Land in Nilai — Residents Terrified"
    test_body  = ("Residents of Nilai reported an unusual cloud formation "
                  "above the town Tuesday. Meteorologists confirmed it was "
                  "a routine lenticular cloud with no unusual activity.")
    try:
        result = classify_article(test_title, test_body)
        print("=== Veritas AI Result ===")
        for k, v in result.items():
            print(f"  {k:<15}: {v}")
    except FileNotFoundError as e:
        print(f"[INFO] {e}")
        from clickbait_scorer import clickbait_score
        score, risk = clickbait_score(test_title, test_body)
        print(f"\n[Clickbait module only]")
        print(f"  Score : {score}")
        print(f"  Risk  : {risk}")
