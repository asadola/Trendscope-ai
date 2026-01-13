from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models import CleanEventDB
from app.utils.time_filters import fresh_since




def compute_topic_velocity(db: Session, topic: str) -> float:
    now = datetime.utcnow()

    buckets = {
        "15m": now - timedelta(minutes=15),
        "1h": now - timedelta(hours=1),
        "24h": now - timedelta(hours=24),
    }

    counts = {}
    for key, since in buckets.items():
        counts[key] = (
            db.query(func.count(CleanEventDB.id))
            .filter(
                CleanEventDB.topic == topic,
                CleanEventDB.ingested_at >= max(since, fresh_since()),
            )
            .scalar()
        )



    velocity = (
        counts["15m"] * 1.0
        + counts["1h"] * 0.6
        + counts["24h"] * 0.2
    )

    return round(velocity, 2)
def compute_hotness(velocity: float, baseline: float = 5.0) -> float:
    if baseline == 0:
        return 0.0
    return round(velocity / baseline, 2)
def recompute_all_trends(db: Session):
    """
    Forces recomputation of velocity & hotness for all topics.
    Used by background workers.
    """

    topics = (
        db.query(CleanEventDB.topic)
        .group_by(CleanEventDB.topic)
        .all()
    )

    for (topic,) in topics:
        velocity = compute_topic_velocity(db, topic)
        hotness = compute_hotness(velocity)

        # At the moment we don't persist these,
        # but calling them warms caches & validates pipeline
        print(f"📈 {topic}: velocity={velocity:.2f}, hotness={hotness:.2f}")
def get_top_trends(
    db: Session,
    limit: int = 5,
):
    """
    Returns top trending topics for digests & automation.
    Stable, deterministic, worker-safe.
    """

    topics = (
        db.query(
            CleanEventDB.topic,
            func.count(CleanEventDB.id).label("article_count"),
        )
        .filter(CleanEventDB.ingested_at >= fresh_since(days=1))
        .group_by(CleanEventDB.topic)
        .order_by(func.count(CleanEventDB.id).desc())
        .limit(limit)
        .all()
    )

    results = []

    for topic, article_count in topics:
        velocity = compute_topic_velocity(db, topic)
        hotness = compute_hotness(velocity)

        results.append({
            "topic": topic,
            "velocity": velocity,
            "hotness": hotness,
            "article_count": article_count,
        })

    return results
def get_quiet_topics(db, limit=6):
    """
    Topics with steady but non-spiking coverage.
    """

    rows = (
        db.query(
            CleanEventDB.topic,
            func.count(CleanEventDB.id).label("count"),
        )
        .filter(
            CleanEventDB.ingested_at >= fresh_since(days=7)
        )
        .group_by(CleanEventDB.topic)
        .having(func.count(CleanEventDB.id).between(5, 80))
        .order_by(func.count(CleanEventDB.id).asc())
        .limit(limit)
        .all()
    )

    return [
        {
            "topic": topic,
            "article_count": count,
            "status": "stable",
        }
        for topic, count in rows
    ]
def is_quiet_signal(article_count: int, velocity: float) -> bool:
    return (
        article_count >= 3
        and article_count <= 50
        and velocity > 0
    )
