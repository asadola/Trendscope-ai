from fastapi import APIRouter

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

        if insight:
            return insight

        articles = fetch_articles_for_topic(topic)
        insight = build_topic_insight(topic, articles, db)

        return insight
    finally:
        db.close()
