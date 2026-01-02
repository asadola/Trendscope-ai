from datetime import datetime, timedelta, timezone
from collections import Counter

def compute_velocity(items, window_minutes=60):
    """
    Compute velocity based on published or ingested timestamps.
    Works for both events and articles.
    """

    now = datetime.now(timezone.utc)
    window = now - timedelta(minutes=window_minutes)

    recent = []

    for item in items:
        ts = item.get("ingested_at") or item.get("published_at")
        if not ts:
            continue

        if ts >= window:
            recent.append(item)

    return len(recent)

def compute_hotness(velocity: dict) -> float:
    """
    Converts keyword velocity into a single hotness score.
    """
    if not velocity:
        return 0.0

    # simple weighted score (can evolve later)
    score = 0.0
    for count in velocity.values():
        score += count

    return round(score / len(velocity), 3)
def compute_insight_confidence(article_count: int) -> int:
    if article_count >= 20:
        return 90
    elif article_count >= 10:
        return 75
    elif article_count >= 5:
        return 60
    return 40

