from fastapi import APIRouter
from app.db.session import SessionLocal
from app.services.topic_ai_insight_service import get_or_build_topic_insight
from app.services.article_service import fetch_articles_for_topic
from datetime import datetime, timedelta

router = APIRouter(prefix="/api", tags=["Topics"])


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
