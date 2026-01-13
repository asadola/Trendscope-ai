def topic_insight_prompt(topic: str, articles: list[dict]) -> str:
    context = "\n".join(
        f"- {a['title']} ({a['source']}): {a.get('content','')[:300]}"
        for a in articles[:8]
        if a.get("title") and a.get("source")
    )

    return f"""
You are an analyst explaining current events clearly and concisely.

Topic: {topic}

Recent coverage:
{context}

Respond in JSON with keys:
summary, why_it_matters, key_points, outlook

Rules:
- Be factual and neutral
- If data is limited, say so
"""

def trend_summary_prompt(topic: str, frequency: int, sources: list):
    source_text = ", ".join(
        f"{s['source']} ({s['percentage']}%)" for s in sources
    )

    return f"""
You are an intelligence analyst.

Topic: {topic}
Mentions: {frequency}
Source distribution: {source_text}

Explain:
1. What is driving this trend
2. Why it matters now
3. What could happen next

Write in clear, neutral language.
"""