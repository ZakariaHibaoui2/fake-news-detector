"""clickbait_scorer.py — Cosine dissimilarity clickbait detection module.

Computes a Clickbait Score in [0, 1] measuring semantic divergence
between an article headline and the article body lead (first 100 words).

  Score 0.0 - 0.30 -> LOW      (headline reflects body accurately)
  Score 0.30 - 0.60 -> MODERATE (some divergence)
  Score 0.60 - 1.0  -> HIGH     (probable clickbait framing)

Usage (standalone test):
  python clickbait_scorer.py
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def _clean(text: str) -> str:
    """Minimal cleaning for clickbait comparison."""
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()


def clickbait_score(title: str, body: str,
                    lead_words: int = 100) -> tuple:
    """Compute Clickbait Score for a headline-body pair.

    Args:
        title:      Article headline.
        body:       Article body text.
        lead_words: Number of body words used as semantic lead.

    Returns:
        (score: float, risk: str)
        score -- float in [0, 1]; higher = more clickbait
        risk  -- "LOW" | "MODERATE" | "HIGH"
    """
    if not title or not body:
        return 0.0, "LOW"

    t = _clean(title)
    l = _clean(" ".join(body.split()[:lead_words]))

    if not t or not l:
        return 0.0, "LOW"

    vect   = TfidfVectorizer(max_features=2000, stop_words="english")
    matrix = vect.fit_transform([t, l])
    sim    = cosine_similarity(matrix[0], matrix[1])[0][0]
    score  = round(1.0 - float(sim), 4)

    if score >= 0.6:
        risk = "HIGH"
    elif score >= 0.3:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return score, risk


# Standalone test
if __name__ == "__main__":
    test_cases = [
        (
            "Aliens Land in Nilai — Residents Terrified",
            "Residents of Nilai reported an unusual lenticular cloud formation "
            "above the town Tuesday evening. Meteorologists confirmed it was a "
            "routine atmospheric phenomenon with no unusual activity recorded.",
        ),
        (
            "Federal Reserve Holds Interest Rates Steady Amid Inflation Concerns",
            "The Federal Reserve voted unanimously to hold the federal funds rate "
            "at its current target range. Chair Jerome Powell cited continued "
            "labour market strength and declining inflation as key factors.",
        ),
        (
            "SHOCKING: You Will NOT Believe What This Politician Did",
            "Senator Jane Smith attended a ribbon-cutting ceremony for a new "
            "public library in Springfield on Wednesday afternoon. The event was "
            "attended by local officials and school children.",
        ),
    ]

    print(f"\n{'Headline':<52} {'Score':>6}  Risk")
    print("-" * 70)
    for title, body in test_cases:
        score, risk = clickbait_score(title, body)
        print(f"{title[:51]:<52} {score:>6.3f}  {risk}")
