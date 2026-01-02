from datetime import datetime, timedelta, timezone

from app.analytics.trend_velocity import compute_velocity
from app.analytics.hotness import compute_hotness

articles = [
    {
        "keywords": ["ai", "regulation"],
        "confidence": 0.9,
        "ingested_at": datetime.now(timezone.utc),
    },
    {
        "keywords": ["ai", "stocks"],
        "confidence": 0.8,
        "ingested_at": datetime.now(timezone.utc) - timedelta(minutes=10),
    },
    {
        "keywords": ["football"],
        "confidence": 0.7,
        "ingested_at": datetime.now(timezone.utc) - timedelta(minutes=90),
    },
]

velocity = compute_velocity(articles)
print("Velocity:", velocity)

for a in articles:
    print("Hotness:", compute_hotness(a, velocity))
