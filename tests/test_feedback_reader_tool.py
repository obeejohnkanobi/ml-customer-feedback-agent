from feedback_agent.tools import feedback_reader_tool


def test_query_feedback_returns_expected_shape() -> None:
    rows = feedback_reader_tool.query_feedback()

    assert isinstance(rows, list)
    assert len(rows) > 0
    for row in rows:
        assert set(row.keys()) == {"id", "text", "source"}
        assert row["source"] in {"email", "chat", "survey"}


def test_query_feedback_filters_invalid_items(monkeypatch) -> None:
    monkeypatch.setattr(
        feedback_reader_tool,
        "feedback_store",
        [
            {"id": "ok-1", "text": "Works", "source": "email"},
            {"id": "bad-1", "text": "", "source": "email"},
            {"id": "bad-2", "text": "Missing source", "source": "sms"},
        ],
    )

    rows = feedback_reader_tool.query_feedback()
    assert rows == [{"id": "ok-1", "text": "Works", "source": "email"}]

