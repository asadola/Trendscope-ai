from collections import Counter

def category_distribution(articles):
    counter = Counter(a["category"] for a in articles if a.get("category"))
    total = sum(counter.values())

    return {
        k: round(v / total, 3)
        for k, v in counter.items()
    }
