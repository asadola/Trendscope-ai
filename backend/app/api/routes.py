from fastapi import APIRouter
from app.db.session import SessionLocal
from app.analysis.keyword_trends import KeywordTrendAnalyzer
from app.analysis.source_share import SourceShareAnalyzer
from app.ai.local_llm import LocalLLM
from app.ai.prompts import trend_summary_prompt
from app.services.topic_service import build_topic_view
from app.services.trend_velocity import compute_topic_velocity, compute_hotness
from app.db.models import CleanEventDB
from sqlalchemy import func
from app.services.topic_ai_insight_service import get_or_build_topic_insight
from app.services.article_service import fetch_articles_for_topic
from datetime import datetime, timedelta



router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/trends/keywords")
def keyword_trends(hours: int = 24, limit: int = 10):
    db = SessionLocal()
    trends = KeywordTrendAnalyzer(db, hours=hours).get_trending_keywords(limit)
    db.close()
    return [{"keyword": w, "count": c} for w, c in trends]

@router.get("/trends/sources")
def source_share():
    db = SessionLocal()
    data = SourceShareAnalyzer(db).source_percentages()
    db.close()
    return data

@router.get("/insights/ai")
def ai_insights(limit: int = 5):
    db = SessionLocal()
    keywords = KeywordTrendAnalyzer(db).get_trending_keywords(limit)
    sources = SourceShareAnalyzer(db).source_percentages(limit=5)
    llm = LocalLLM(model="llama3.1")

    insights = []
    for topic, freq in keywords:
        prompt = trend_summary_prompt(topic, freq, sources)
        summary = llm.generate(prompt)
        insights.append({"topic": topic, "mentions": freq, "summary": summary})

    db.close()
    return insights



@router.get("/trends/velocity")
def trend_velocity(limit: int = 10):
    db = SessionLocal()

    topics = (
        db.query(CleanEventDB.topic, func.count(CleanEventDB.id))
        .group_by(CleanEventDB.topic)
        .order_by(func.count(CleanEventDB.id).desc())
        .limit(limit)
        .all()
    )

    results = []
    for topic, count in topics:
        velocity = compute_topic_velocity(db, topic)
        hotness = compute_hotness(velocity)

        status = (
            "breaking" if hotness >= 2
            else "trending" if hotness >= 1
            else "stable"
        )

        results.append({
            "topic": topic,
            "velocity": velocity,
            "hotness": hotness,
            "status": status,
            "article_count": count,
        })

    db.close()
    return results
@router.get("/topics/{topic}")
def topic_view(topic: str):
    db = SessionLocal()

    insight = get_or_build_topic_insight(db, topic)
    articles = fetch_articles_for_topic(topic, limit=10)

    db.close()

    return {
    "topic": topic,
    "article_count": len(articles),
    "insight": {
        "summary": insight.explanation if insight else None,
        "why_it_matters": insight.why_it_matters if insight else None,
        "key_points": insight.key_points if insight else [],
        "confidence": insight.confidence if insight else None,
        "generated_at": insight.generated_at if insight else None,
        "fresh": (
            insight.generated_at > datetime.utcnow() - timedelta(hours=6)
            if insight else False
        ),
    },
    "articles": articles,
}
