from fastapi import APIRouter
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.db.models import TopicInsightDB
from app.services.article_service import fetch_articles_for_topic
from app.services.insight_builder import build_topic_insight

router = APIRouter(prefix="/api", tags=["Insights"])


@router.get("/insights/{topic}")
def get_insight(topic: str):
    db = SessionLocal()
    try:
        insight = (
            db.query(TopicInsightDB)
            .filter(TopicInsightDB.topic == topic)
            .first()
        )

        # ✅ reuse insight if still fresh (6 hours)
        if insight and insight.created_at:
            age = datetime.utcnow() - insight.created_at
            if age < timedelta(hours=6):
                return insight

        # 🔥 analyze a controlled, diverse set
        articles = fetch_articles_for_topic(
            topic=topic,
            limit=15,          # analyze more than before
            include_old=False  # only fresh news
        )

        if not articles:
            return insight  # fallback safely

        insight = build_topic_insight(topic, articles, db)
        return insight

    finally:
        db.close()
