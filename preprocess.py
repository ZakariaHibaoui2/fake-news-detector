"""preprocess.py — Text cleaning pipeline for Veritas AI."""
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
STOP_WORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """Clean raw article text for TF-IDF vectorisation.
    Steps: lowercase, strip HTML, strip URLs, remove punctuation,
           remove stop words, collapse whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"<[^>]+>",          " ", text)   # HTML tags
    text = re.sub(r"http\S+|www\S+",   " ", text)   # URLs
    text = re.sub(r"[^a-z0-9\s]",      " ", text)   # punctuation
    tokens = [t for t in text.split()
              if t not in STOP_WORDS and len(t) > 1]
    return " ".join(tokens)
