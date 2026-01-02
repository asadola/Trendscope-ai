def topic_insight_prompt(topic: str, articles: list):
    joined = "\n\n".join(
        f"- {a['title']}: {a['content'][:500]}"
        for a in articles[:5]
    )

    return f"""
You are an analyst.

Topic: {topic}

Articles:
{joined}

Produce:
1. A concise summary
2. Why this topic matters
3. A short outlook

Respond in structured JSON with keys:
summary, why_it_matters, outlook
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
def topic_insight_prompt(topic: str, articles: list[dict]) -> str:
    context = "\n".join(
        f"- {a['title']} ({a['source']})"
        for a in articles[:10]
        if a.get("title") and a.get("source")
    )

    return f"""
You are an analyst explaining current events clearly and concisely.

Topic: {topic}

Recent coverage:
{context}

Write:
1. A short summary of what is happening
2. Why this topic matters right now
3. A realistic outlook (next days or weeks)

Be factual, neutral, and avoid hype.
If information is limited, say so.
"""
def topic_insight_prompt(topic: str, articles: list[str]) -> str:
    joined = "\n".join(f"- {a}" for a in articles[:10])

    return f"""
You are an analyst.

Topic: {topic}

Recent news snippets:
{joined}

Tasks:
1. Summarize what is happening (2–3 sentences)
2. Explain why this topic matters now
3. List 3 key points
4. Predict short-term outlook (1 sentence)

Respond in JSON with keys:
summary, why_it_matters, key_points, outlook
"""
