from app.services.article_service import fetch_articles_for_topic
from app.db.session import SessionLocal


def build_topic_view(topic: str):
    """
    Build a topic detail view WITHOUT AI.
    This is the stable data backbone for the UI.
    """
    db = SessionLocal()
    try:
        articles = fetch_articles_for_topic(topic, limit=20)

        sources = {}
        for a in articles:
            if a.get("source") and a.get("url"):
                sources[a["source"]] = a["url"]

        return {
            "topic": topic,
            "article_count": len(articles),
            "sources": [
                {"name": name, "url": url}
                for name, url in sources.items()
            ],
            "articles": articles,
        }
    finally:
        db.close()
