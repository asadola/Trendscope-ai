from collections import Counter
from datetime import datetime, timezone, timedelta

def aggregate_keywords(articles, window_minutes=120):
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)

    counter = Counter()

    for a in articles:
        if a["ingested_at"] < cutoff:
            continue

        weight = a.get("confidence", 1.0)
        for kw in a.get("keywords", []):
            counter[kw] += weight

    return counter.most_common(20)
