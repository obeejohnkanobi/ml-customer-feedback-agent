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
        _nlp = spacy.load("en_core_web_sm")
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
    nlp = _get_nlp()
    doc = nlp(text)

    noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text) > 2]
    named_entities = [
        ent.text.lower()
        for ent in doc.ents
        if ent.label_ not in ("CARDINAL", "ORDINAL", "DATE", "TIME")
    ]

    # Deduplicer og bevar rækkefølge
    seen = set()
    keywords: List[str] = []
    for kw in noun_chunks + named_entities:
        if kw not in seen:
            seen.add(kw)
            keywords.append(kw)

    return keywords
