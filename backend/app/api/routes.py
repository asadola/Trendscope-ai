from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr

from app.db.session import SessionLocal
from app.db.models import CleanEventDB, SubscriberDB
from app.analysis.keyword_trends import KeywordTrendAnalyzer
from app.analysis.source_share import SourceShareAnalyzer
from app.ai.local_llm import LocalLLM
from app.ai.prompts import trend_summary_prompt
from app.services.article_service import fetch_articles_for_topic
from app.services.topic_ai_insight_service import get_or_build_topic_insight
from app.services.trend_velocity import compute_topic_velocity, compute_hotness
from app.utils.time_filters import fresh_since
from app.services.article_service import fetch_topic_feed



# --------------------------------------------------
# Router & DB
# --------------------------------------------------

router = APIRouter(prefix="/api")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Health
# --------------------------------------------------

@router.get("/health")
def health_check():
    return {"status": "ok"}


# --------------------------------------------------
# Keyword Trends
# --------------------------------------------------

@router.get("/trends/keywords")
def keyword_trends(hours: int = 24, limit: int = 10):
    db = SessionLocal()
    trends = KeywordTrendAnalyzer(db, hours=hours).get_trending_keywords(limit)
    db.close()
    return [{"keyword": w, "count": c} for w, c in trends]


# --------------------------------------------------
# Source Share
# --------------------------------------------------

@router.get("/trends/sources")
def source_share():
    db = SessionLocal()
    data = SourceShareAnalyzer(db).source_percentages()
    db.close()
    return data


# --------------------------------------------------
# AI Insights (summary cards)
# --------------------------------------------------

@router.get("/insights/ai")
def ai_insights(limit: int = 5):
    db = SessionLocal()
    keywords = KeywordTrendAnalyzer(db).get_trending_keywords(limit)
    sources = SourceShareAnalyzer(db).source_percentages(limit=5)
    llm = LocalLLM(model="llama3.1")

    insights = []
    for topic, freq in keywords:
        prompt = trend_summary_prompt(
            topic=topic,
            frequency=freq,
            sources=sources,
        )
        summary = "AI summary temporarily disabled"

        insights.append({
            "topic": topic,
            "mentions": freq,
            "summary": summary,
        })

    db.close()
    return insights


# --------------------------------------------------
# TRENDING NOW (MAIN GRID)
# --------------------------------------------------

@router.get("/trends/velocity")
def trend_velocity(limit: int = 30):
    db = SessionLocal()
    now = datetime.utcnow()

    topics = (
        db.query(
            CleanEventDB.topic,
            func.count(CleanEventDB.id).label("count"),
            func.max(CleanEventDB.ingested_at).label("latest")
        )
        .group_by(CleanEventDB.topic)
        .all()  # ❗ DO NOT LIMIT HERE
    )

    results = []

    for topic, count, latest in topics:
        age_hours = (now - latest).total_seconds() / 3600

        # --- velocity buckets ---
        v_15m = db.query(func.count(CleanEventDB.id)).filter(
            CleanEventDB.topic == topic,
            CleanEventDB.ingested_at >= now - timedelta(minutes=15)
        ).scalar()

        v_1h = db.query(func.count(CleanEventDB.id)).filter(
            CleanEventDB.topic == topic,
            CleanEventDB.ingested_at >= now - timedelta(hours=1)
        ).scalar()

        velocity = (v_15m * 1.0) + (v_1h * 0.6)

        # --- status logic ---
        if age_hours <= 6 and velocity >= 3:
            status = "breaking"
        elif velocity >= 2:
            status = "trending"
        elif 3 <= count <= 50 and velocity > 0:
            status = "quiet"
        else:
            status = "stable"

        results.append({
            "topic": topic,
            "status": status,
            "article_count": count,
            "velocity": round(velocity, 2),
            "last_seen": latest,
        })

    db.close()

    # 🔥 Rank by intelligence, not raw count
    results.sort(
        key=lambda x: (
            x["status"] == "breaking",
            x["status"] == "trending",
            x["status"] == "quiet",
            x["velocity"],
            x["article_count"],
        ),
        reverse=True,
    )

    return results[:limit]

# --------------------------------------------------
# BREAKING MARQUEE (RARE)
# --------------------------------------------------

@router.get("/trends/breaking")
def breaking_trends(limit: int = 15):
    db = SessionLocal()
    now = datetime.utcnow()

    rows = (
        db.query(
            CleanEventDB.topic,
            func.count(CleanEventDB.id).label("count"),
            func.max(CleanEventDB.ingested_at).label("latest"),
        )
        .group_by(CleanEventDB.topic)
        .order_by(func.max(CleanEventDB.ingested_at).desc())
        .limit(limit)
        .all()
    )

    results = []
    for topic, count, latest in rows:
        age_hours = (now - latest).total_seconds() / 3600

        if age_hours <= 6:  # ONLY filter here
            insight = get_or_build_topic_insight(db, topic)
            results.append({
                "topic": topic,
                "category": topic,
                "summary": (
                    insight.explanation
                    if insight and insight.explanation
                    else f"{topic.capitalize()} is seeing fresh activity."
                ),
                "article_count": count,
            })

    db.close()
    return results


# --------------------------------------------------
# Topic Page
# --------------------------------------------------

@router.get("/topics/{topic}")
def topic_view(topic: str):
    db = SessionLocal()

    insight = get_or_build_topic_insight(db, topic)
    articles = fetch_articles_for_topic(topic, limit=50)

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
                insight.generated_at.replace(tzinfo=None)
                > datetime.utcnow() - timedelta(hours=6)
                if insight else False
            ),
        },
        "articles": articles,
    }


# --------------------------------------------------
# Sources
# --------------------------------------------------

@router.get("/sources/{source}")
def source_articles(source: str, limit: int = 20):
    db = SessionLocal()

    articles = (
        db.query(CleanEventDB)
        .filter(
            CleanEventDB.source == source,
            CleanEventDB.ingested_at >= fresh_since(days=7),
        )
        .order_by(CleanEventDB.ingested_at.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return [
        {
            "title": a.title,
            "url": a.url,
            "topic": a.topic,
            "source": a.source,
            "ingested_at": a.ingested_at.isoformat(),
        }
        for a in articles
    ]


# --------------------------------------------------
# Subscribe
# --------------------------------------------------

class SubscribeRequest(BaseModel):
    email: EmailStr
    phone: str | None = None


@router.post("/subscribe")
def subscribe_user(payload: SubscribeRequest, request: Request):
    db = SessionLocal()

    if db.query(SubscriberDB).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="Already subscribed")

    subscriber = SubscriberDB(
        email=payload.email,
        phone=payload.phone,
        ip_address=request.client.host,
    )

    db.add(subscriber)
    db.commit()
    db.close()

    return {"status": "ok", "message": "Subscribed successfully"}
@router.get("/topics/{topic}/articles")
def topic_articles(
    topic: str,
    limit: int = 50,
    offset: int = 0,
):
    return fetch_topic_feed(
        topic=topic,
        limit=limit,
        offset=offset,
    )
@router.get("/topics/search")
def search_topics(q: str):
    db = SessionLocal()
    try:
        rows = (
            db.query(
                CleanEventDB.topic,
                func.count(CleanEventDB.id).label("count")
            )
            .filter(CleanEventDB.topic.ilike(f"%{q}%"))
            .group_by(CleanEventDB.topic)
            .order_by(func.count(CleanEventDB.id).desc())
            .limit(20)
            .all()
        )

        return [
            {
                "topic": t,
                "article_count": c,
            }
            for t, c in rows
        ]
    finally:
        db.close()
