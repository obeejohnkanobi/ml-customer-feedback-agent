from feedback_agent.tools import sentiment_analysis_tool


class _FakeAssistantAgent:
    def __init__(self, *args, **kwargs):
        _ = args, kwargs

    def generate_reply(self, messages):
        _ = messages
        return {"content": "[positive]"}


class _NoisyAssistantAgent:
    def __init__(self, *args, **kwargs):
        _ = args, kwargs

    def generate_reply(self, messages):
        _ = messages
        return "The sentiment is definitely negative."


class _FailingAssistantAgent:
    def __init__(self, *args, **kwargs):
        _ = args, kwargs

    def generate_reply(self, messages):
        _ = messages
        raise RuntimeError("Temporary API issue")


def test_analyze_sentiment_parses_bracketed_value(monkeypatch) -> None:
    monkeypatch.setattr(sentiment_analysis_tool, "AssistantAgent", _FakeAssistantAgent)

    assert sentiment_analysis_tool.analyze_sentiment("Great product") == "positive"


def test_analyze_sentiment_parses_sentence_value(monkeypatch) -> None:
    monkeypatch.setattr(sentiment_analysis_tool, "AssistantAgent", _NoisyAssistantAgent)

    assert sentiment_analysis_tool.analyze_sentiment("Bad experience") == "negative"


def test_analyze_sentiment_returns_neutral_on_repeated_failures(monkeypatch) -> None:
    monkeypatch.setattr(sentiment_analysis_tool, "AssistantAgent", _FailingAssistantAgent)
    monkeypatch.setattr(sentiment_analysis_tool.time, "sleep", lambda _seconds: None)

    assert sentiment_analysis_tool.analyze_sentiment("Anything") == "neutral"


def test_analyze_sentiment_empty_text_returns_neutral() -> None:
    assert sentiment_analysis_tool.analyze_sentiment("  ") == "neutral"

