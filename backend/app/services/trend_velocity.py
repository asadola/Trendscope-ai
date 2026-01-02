from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models import CleanEventDB


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
                CleanEventDB.ingested_at >= since,
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
