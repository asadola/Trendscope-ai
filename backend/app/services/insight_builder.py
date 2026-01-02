from datetime import datetime, timezone

from app.ai.local_llm import LocalLLM
from app.ai.prompts import topic_insight_prompt
from app.db.models import TopicInsightDB


def build_topic_insight(topic: str, articles: list, db):
    """
    Generate and persist an AI insight for a topic.
    Cached in DB so it is not regenerated repeatedly.
    """

    if not articles:
        summary = f"No sufficient data available yet for {topic}."
        why = "The topic has limited coverage at the moment."
        outlook = "Monitor for new developments."
    else:
        llm = LocalLLM(model="llama3.1")

        prompt = topic_insight_prompt(topic, articles)
        response = llm.generate(prompt)

        summary = response.get("summary", "")
        why = response.get("why_it_matters", "")
        outlook = response.get("outlook", "")

    insight = TopicInsightDB(
        topic=topic,
        summary=summary,
        why_it_matters=why,
        outlook=outlook,
        created_at=datetime.now(timezone.utc),
    )

    db.add(insight)
    db.commit()
    db.refresh(insight)

    return insight
def build_topic_insight(topic: str, articles: list[dict], db):
    llm = LocalLLM(model="llama3.1")

    prompt = topic_insight_prompt(topic, articles)
    response = llm.generate(prompt)

    # Simple parsing (LLM outputs paragraphs)
    parts = response.split("\n\n")

    summary = parts[0] if len(parts) > 0 else response
    why = parts[1] if len(parts) > 1 else ""
    outlook = parts[2] if len(parts) > 2 else ""

    insight = TopicInsightDB(
        topic=topic,
        summary=summary.strip(),
        why_it_matters=why.strip(),
        outlook=outlook.strip(),
    )

    db.add(insight)
    db.commit()
    db.refresh(insight)

    return insight