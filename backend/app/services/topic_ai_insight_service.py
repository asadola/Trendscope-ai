from sqlalchemy.orm import Session
from app.db.models import TopicInsightDB
from app.services.article_service import fetch_articles_for_topic
from app.ai.local_llm import LocalLLM
from app.services.trend_metrics import compute_insight_confidence

import json
import re
from datetime import datetime, timedelta


INSIGHT_TTL_HOURS = 6  # refresh window


def get_or_build_topic_insight(db: Session, topic: str) -> TopicInsightDB | None:
    # 1️⃣ Try cache first (WITH freshness)
    insight = (
        db.query(TopicInsightDB)
        .filter(TopicInsightDB.topic == topic)
        .first()
    )

    if insight and insight.generated_at:
        if insight.generated_at > datetime.utcnow() - timedelta(hours=INSIGHT_TTL_HOURS):
            return insight

    # 2️⃣ Fetch articles
    articles = fetch_articles_for_topic(topic, limit=10)
    if not articles:
        return None

    # 3️⃣ Compute confidence (DATA-DRIVEN)
    confidence = compute_insight_confidence(len(articles))

    # 4️⃣ Build prompt
    context = "\n".join(a["content"] for a in articles[:5])

    prompt = f"""
You are an intelligence analyst.

Topic: {topic}

Articles:
{context}

IMPORTANT:
- Respond with ONLY valid JSON
- Do NOT include explanations, markdown, or extra text

Return this exact structure:

{{
  "explanation": "...",
  "why_it_matters": "...",
  "key_points": ["...", "...", "..."]
}}
"""

    # 5️⃣ Run LLM
    llm = LocalLLM(model="llama3.1")
    raw = llm.generate(prompt)

    print("LLM RAW OUTPUT:", raw)

    # 6️⃣ Extract JSON safely
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"LLM did not return JSON: {raw}")

    data = json.loads(match.group())

    # 7️⃣ Save / Update insight
    if not insight:
        insight = TopicInsightDB(topic=topic, category=topic)

    insight.explanation = data.get("explanation")
    insight.why_it_matters = data.get("why_it_matters")
    insight.key_points = data.get("key_points", [])
    insight.sources = [
        {"title": a["source"], "url": a["url"]}
        for a in articles[:5]
    ]
    insight.confidence = confidence
    insight.generated_at = datetime.utcnow()

    db.add(insight)
    db.commit()
    db.refresh(insight)

    return insight
