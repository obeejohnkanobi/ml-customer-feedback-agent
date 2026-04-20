"""
Feedback Analysis Agent
========================
Kør med: python -m feedback_agent.agent.feedback_analysis_agent
"""

import json
import os
from datetime import datetime

from autogen import ConversableAgent

from feedback_agent.tools.categorization_tool import categorize_feedback
from feedback_agent.tools.feedback_reader_tool import query_feedback
from feedback_agent.tools.keyword_extraction_tool import extract_keywords
from feedback_agent.tools.sentiment_analysis_tool import analyze_sentiment
from feedback_agent.config import LLM_CONFIG


def create_feedback_analysis_agent() -> ConversableAgent:
    agent = ConversableAgent(
        name="Feedback Analysis Agent",
        system_message=(
            "You are a customer feedback analysis expert. "
            "Work through the following steps IN ORDER:\n"
            "1. Call 'feedback_reader' to get all feedback.\n"
            "2. For each feedback item call 'sentiment_analysis' on its text.\n"
            "3. For each feedback item call 'keyword_extraction' on its text.\n"
            "4. For each feedback item call 'categorization' with the extracted keywords.\n"
            "5. When all items are processed, produce a final JSON summary structured as:\n"
            "   [\n"
            "     {\"id\": \"1\", \"source\": \"...\", \"sentiment\": \"...\","
            " \"keywords\": [...], \"categories\": [...]},\n"
            "     ...\n"
            "   ]\n"
            "   followed by a short plain-text business insight for each category found.\n"
            "6. Return 'TERMINATE' when done.\n"
            "Do not skip any step or any feedback item."
        ),
        llm_config=LLM_CONFIG,
    )

    # register_for_llm = fortæl LLM'en at dette tool eksisterer
    agent.register_for_llm(
        name="feedback_reader",
        description="Read all customer feedback. Returns a list of {id, text, source}.",
    )(query_feedback)

    agent.register_for_llm(
        name="sentiment_analysis",
        description="Analyze sentiment of a single feedback text. Returns 'positive', 'negative', or 'neutral'.",
    )(analyze_sentiment)

    agent.register_for_llm(
        name="keyword_extraction",
        description="Extract keywords from a single feedback text. Returns a list of keyword strings.",
    )(extract_keywords)

    agent.register_for_llm(
        name="categorization",
        description=(
            "Categorize feedback into business themes given a list of keywords. "
            "Returns a list of category names such as 'Product Quality', "
            "'Delivery & Shipping', 'Customer Support', 'Staff & Service', "
            "'App & Website', 'Price & Value', or 'General'."
        ),
    )(categorize_feedback)

    return agent


def create_user_proxy() -> ConversableAgent:
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: (
            msg.get("content") is not None and "TERMINATE" in msg["content"]
        ),
        human_input_mode="NEVER",
    )

    # register_for_execution = den agent der rent faktisk kører Python-funktionen
    user_proxy.register_for_execution(name="feedback_reader")(query_feedback)
    user_proxy.register_for_execution(name="sentiment_analysis")(analyze_sentiment)
    user_proxy.register_for_execution(name="keyword_extraction")(extract_keywords)
    user_proxy.register_for_execution(name="categorization")(categorize_feedback)

    return user_proxy


def save_report(chat_result) -> str:
    """Gem den endelige chat-konklusion som Markdown-rapport."""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"reports/feedback_report_{timestamp}.md"

    # Hent sidste besked fra assistant (indeholder den endelige analyse)
    last_message = ""
    for msg in reversed(chat_result.chat_history):
        if msg.get("role") == "assistant" and msg.get("content"):
            last_message = msg["content"].replace("TERMINATE", "").strip()
            break

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Feedback Analysis Report\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.write(last_message)

    return path


def main() -> None:
    user_proxy = create_user_proxy()
    feedback_analysis_agent = create_feedback_analysis_agent()

    chat_result = user_proxy.initiate_chat(
        feedback_analysis_agent,
        message=(
            "Analyze all customer feedback:\n"
            "1. Read the feedback using the feedback_reader tool.\n"
            "2. For each item: run sentiment_analysis, keyword_extraction, and categorization.\n"
            "3. Return a JSON array with all results plus a short business insight per category."
        ),
    )

    report_path = save_report(chat_result)
    print(f"\n✅ Report saved to: {report_path}")


if __name__ == "__main__":
    main()
