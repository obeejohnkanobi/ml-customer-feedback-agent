from typing import Literal, Optional, Union, cast
import time
from autogen import AssistantAgent
from feedback_agent.config import LLM_CONFIG

SENTIMENT_VALUES = {"positive", "negative", "neutral"}


def _extract_sentiment_value(reply: Optional[Union[str, dict]]) -> str:
    if isinstance(reply, dict):
        reply_value = (reply.get("content") or "").strip()
    else:
        reply_value = str(reply).strip()

    if not reply_value:
        return ""

    normalized = (
        reply_value.lower()
        .replace("[", " ")
        .replace("]", " ")
        .replace(".", " ")
        .replace(",", " ")
    )
    tokens = normalized.split()

    for sentiment in SENTIMENT_VALUES:
        if sentiment in tokens:
            return sentiment
    return ""

def analyze_sentiment(text: str) -> Literal["positive", "negative", "neutral"]:
    if not text or not text.strip():
        return "neutral"

    agent = AssistantAgent(
        name="Sentiment Analysis Agent",
        system_message="You are a helpful AI assistant. "
                      "You can analyze the sentiment of a customer feedback. "
                      "Given a customer feedback, you can use the sentiment_analysis tool to analyze the sentiment. "
                      "You will provide sentiment analysis result in the following format: '[sentiment]'. "
                      "Example result: 'positive'. "
                      "Example of invalid result: 'sentiment is positive'."
                      "Sentiment can be 'positive', 'negative', or 'neutral'. "
                      "Don't include any other text in your response."
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            reply = agent.generate_reply(
                messages=[
                    {"role": "user", "content": f"analyze the sentiment of the following feedback: {text}"}
                ],
            )
            if reply is None:
                continue
            parsed_reply = cast(Union[str, dict], reply)
            sentiment = _extract_sentiment_value(parsed_reply)
            if sentiment == "positive":
                return "positive"
            if sentiment == "negative":
                return "negative"
            if sentiment == "neutral":
                return "neutral"
        except Exception:
            pass

        if attempt < max_attempts:
            time.sleep(attempt)

    # Graceful fallback keeps full pipeline alive for reports/demo runs.
    return "neutral"
