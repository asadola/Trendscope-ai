from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.db.models import CleanEventDB
from app.utils.time_filters import fresh_since
from datetime import datetime, timedelta


def fetch_articles_for_topic(
    topic: str,
    limit: int = 50,
    include_old: bool = False,
):
    """
    Fetch recent articles for a topic.
    - Deduplicates by source
    - Returns latest first
    """

    db: Session = SessionLocal()
    try:
        query = (
            db.query(CleanEventDB)
            .filter(CleanEventDB.topic == topic)
        )

        if not include_old:
            query = query.filter(
                CleanEventDB.ingested_at >= fresh_since(days=7)
            )

        rows = (
            query
            .order_by(desc(CleanEventDB.ingested_at))
            .limit(limit * 3)  # overfetch for dedupe
            .all()
        )

        seen_sources = set()
        articles = []

        for a in rows:
            if a.source in seen_sources:
                continue

            seen_sources.add(a.source)
            articles.append({
                "title": a.title,
                "content": a.clean_text,
                "source": a.source,
                "url": a.url,
                "published_at": a.published_at,
            })

            if len(articles) >= limit:
                break

        return articles

    finally:
        db.close()
def fetch_topic_feed(
    topic: str,
    limit: int = 50,
    offset: int = 0,
):
    """
    Full reading feed for topic pages.
    Includes older articles.
    """

    db: Session = SessionLocal()
    try:
        articles = (
            db.query(CleanEventDB)
            .filter(CleanEventDB.topic == topic)
            .order_by(CleanEventDB.published_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
    {
        "title": a.title,
        "source": a.source,
        "url": a.url,
        "published_at": a.published_at,
        "is_past": a.ingested_at < fresh_since(days=7),
    }
    for a in articles
]

    finally:
        db.close()
