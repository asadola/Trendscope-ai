from datetime import timedelta

def bucket_by_time(articles):
    buckets = {
        "1h": [],
        "6h": [],
        "24h": [],
    }

    now = max(a["ingested_at"] for a in articles)

    for a in articles:
        delta = now - a["ingested_at"]

        if delta <= timedelta(hours=1):
            buckets["1h"].append(a)
        if delta <= timedelta(hours=6):
            buckets["6h"].append(a)
        if delta <= timedelta(hours=24):
            buckets["24h"].append(a)

    return buckets
