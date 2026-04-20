from typing import List, TypedDict, Literal


class Feedback(TypedDict):
    id: str
    text: str
    source: Literal["email", "chat", "survey"]


# ============================================================
# ▼▼▼  TILFØJ/ÆNDR FEEDBACK HER – eller udskift med
#       en CSV/database-læser efter behov              ▼▼▼
# ============================================================
feedback_store: List[Feedback] = [
    {
        "id": "1",
        "text": "I love the product! It arrived quickly and works perfectly.",
        "source": "email",
    },
    {
        "id": "2",
        "text": "The app keeps crashing every time I try to check my order. Very frustrating.",
        "source": "chat",
    },
    {
        "id": "3",
        "text": "Staff was rude and unhelpful. I waited 20 minutes and nobody assisted me.",
        "source": "survey",
    },
    {
        "id": "4",
        "text": "Delivery took 3 weeks instead of the promised 5 days. No communication from support.",
        "source": "email",
    },
    {
        "id": "5",
        "text": "Love the new interface! Checkout process is smooth and fast.",
        "source": "chat",
    },
    {
        "id": "6",
        "text": "Product broke after two days. Terrible quality for the price. I want a refund.",
        "source": "survey",
    },
    {
        "id": "7",
        "text": "Customer support never responds. I have been waiting 3 days for an answer.",
        "source": "email",
    },
    {
        "id": "8",
        "text": "The staff member was absolutely wonderful. She went above and beyond to help me.",
        "source": "survey",
    },
]
# ============================================================


def query_feedback() -> List[Feedback]:
    """Read all customer feedback from the feedback store.
    Returns a list of feedback items, each with id, text, and source."""
    return feedback_store
