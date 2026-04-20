"""
Keyword extraction via spaCy noun chunks + named entities.

Kræver:
    pip install spacy
    python -m spacy download en_core_web_sm
"""

from typing import List

import spacy

# Lazy-load modellen én gang (undgår genindlæsning ved hvert kald)
_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError as exc:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' is not installed. "
                "Run: python -m spacy download en_core_web_sm"
            ) from exc
    return _nlp


def extract_keywords(text: str) -> List[str]:
    """Extract relevant keywords from a piece of feedback text.

    Uses spaCy noun chunks and named entities. Returns a deduplicated
    list of lowercase keyword strings.

    Args:
        text: The raw feedback string to extract keywords from.

    Returns:
        List of keyword strings, e.g. ["product quality", "delivery time"].
    """
    if not text or not text.strip():
        return []

    nlp = _get_nlp()
    doc = nlp(text)

    noun_chunks = [chunk.text.lower().strip() for chunk in doc.noun_chunks if len(chunk.text.strip()) > 2]
    named_entities = [
        ent.text.lower().strip()
        for ent in doc.ents
        if ent.label_ not in ("CARDINAL", "ORDINAL", "DATE", "TIME") and len(ent.text.strip()) > 2
    ]

    # Deduplicer og bevar rækkefølge
    seen = set()
    keywords: List[str] = []
    for kw in noun_chunks + named_entities:
        if kw not in seen:
            seen.add(kw)
            keywords.append(kw)

    return keywords
