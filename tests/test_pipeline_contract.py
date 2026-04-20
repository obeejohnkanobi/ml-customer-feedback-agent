from feedback_agent.tools.feedback_reader_tool import query_feedback


EXPECTED_KEYS = {"id", "text", "source"}


def test_feedback_items_follow_contract() -> None:
    rows = query_feedback()

    assert rows, "Expected at least one feedback item in sample dataset"
    for row in rows:
        assert set(row.keys()) == EXPECTED_KEYS
        assert isinstance(row["id"], str) and row["id"].strip()
        assert isinstance(row["text"], str) and row["text"].strip()
        assert row["source"] in {"email", "chat", "survey"}

