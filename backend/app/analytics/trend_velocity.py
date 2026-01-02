from collections import defaultdict
from datetime import datetime, timedelta, timezone


def compute_velocity(events, window_minutes=60):
    """
    events: list of articles
    Each article must have:
      - keywords
      - ingested_at (datetime)
    """

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=window_minutes)

    current = defaultdict(int)
    previous = defaultdict(int)

    for e in events:
        ts = e.get("ingested_at")
        if not ts:
            continue

        for kw in e.get("keywords", []):
            if ts >= window_start:
                current[kw] += 1
            else:
                previous[kw] += 1

    velocity = {}

    for kw, count in current.items():
        prev = previous.get(kw, 0)
        velocity[kw] = count - prev

    return velocity
