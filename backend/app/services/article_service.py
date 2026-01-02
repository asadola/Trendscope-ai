from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import CleanEventDB


def fetch_articles_for_topic(topic: str, limit: int = 10):
    """
    Fetch recent cleaned articles related to a topic.
    Used by AI insight builder & API.
    """

    db: Session = SessionLocal()
    try:
        articles = (
            db.query(CleanEventDB)
            .filter(CleanEventDB.topic == topic)
            .order_by(CleanEventDB.ingested_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "title": a.title,
                "content": a.clean_text,
                "source": a.source,
                "url": a.url,
                "published_at": a.published_at,
            }
            for a in articles
        ]
    finally:
        db.close()
