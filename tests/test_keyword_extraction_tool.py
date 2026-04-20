from types import SimpleNamespace

from feedback_agent.tools import keyword_extraction_tool


class _FakeNLP:
    def __call__(self, text: str):
        _ = text
        return SimpleNamespace(
            noun_chunks=[
                SimpleNamespace(text="product quality"),
                SimpleNamespace(text="delivery time"),
            ],
            ents=[
                SimpleNamespace(text="Acme", label_="ORG"),
                SimpleNamespace(text="2 days", label_="DATE"),
            ],
        )


def test_extract_keywords_empty_text_returns_empty() -> None:
    assert keyword_extraction_tool.extract_keywords("   ") == []


def test_extract_keywords_uses_chunks_and_entities(monkeypatch) -> None:
    monkeypatch.setattr(keyword_extraction_tool, "_get_nlp", lambda: _FakeNLP())

    keywords = keyword_extraction_tool.extract_keywords("Any text")

    assert keywords == ["product quality", "delivery time", "acme"]

