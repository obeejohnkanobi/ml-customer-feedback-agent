from feedback_agent.tools.categorization_tool import categorize_feedback


def test_categorize_feedback_with_partial_keyword_match() -> None:
    categories = categorize_feedback(["customer support team", "delivery delay"])

    assert "Customer Support" in categories
    assert "Delivery & Shipping" in categories


def test_categorize_feedback_falls_back_to_general() -> None:
    assert categorize_feedback([]) == ["General"]
    assert categorize_feedback(["   "]) == ["General"]

