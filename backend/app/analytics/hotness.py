from math import log


def compute_hotness(article, velocity):
    """
    Combines:
    - keyword velocity
    - article confidence
    - recency
    """

    score = 0.0

    for kw in article.get("keywords", []):
        score += max(0, velocity.get(kw, 0))

    confidence = article.get("confidence", 0.5)

    # dampen extreme spikes
    score = log(score + 1)

    return round(score * confidence, 3)
