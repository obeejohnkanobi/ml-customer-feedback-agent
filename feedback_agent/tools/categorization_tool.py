"""
Categorization tool: mapper keywords til business-temaer via keyword matching.
"""

from typing import List

# ============================================================
# ▼▼▼  TILPAS KATEGORIER OG KEYWORDS TIL DIT DOMÆNE  ▼▼▼
# ============================================================
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Product Quality": [
        "product", "quality", "broke", "broken", "defective", "damaged",
        "works", "item", "packaging", "material", "durable", "refund",
    ],
    "Delivery & Shipping": [
        "delivery", "shipping", "arrived", "arrive", "wait", "late",
        "delayed", "weeks", "days", "tracking",
    ],
    "Customer Support": [
        "support", "chat", "respond", "response", "answer", "help",
        "communication", "contact", "waiting",
    ],
    "Staff & Service": [
        "staff", "rude", "helpful", "employee", "team", "assisted",
        "wonderful", "assistant", "cashier",
    ],
    "App & Website": [
        "app", "website", "crash", "interface", "checkout", "navigate",
        "login", "bug", "slow", "fast",
    ],
    "Price & Value": [
        "price", "expensive", "cheap", "value", "worth", "cost",
        "competitive", "affordable", "refund", "money",
    ],
}
# ============================================================


def categorize_feedback(keywords: List[str]) -> List[str]:
    """Categorize feedback into business themes based on extracted keywords.

    Matches keywords against predefined categories. A single piece of feedback
    can belong to multiple categories. Returns ['General'] if no match is found.

    Args:
        keywords: List of keyword strings (output from extract_keywords).

    Returns:
        List of matched category names, e.g. ["Product Quality", "Delivery & Shipping"].
    """
    keywords_lower = {kw.lower() for kw in keywords}

    matched: List[str] = [
        category
        for category, category_kws in CATEGORY_KEYWORDS.items()
        if any(kw in keywords_lower for kw in category_kws)
    ]

    return matched if matched else ["General"]
