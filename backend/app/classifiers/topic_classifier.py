from collections import defaultdict

from app.classifiers.keyword_extractor import extract_keywords

CATEGORIES = {
    "finance": [
        "market",
        "stocks",
        "shares",
        "trading",
        "economy",
        "inflation",
        "interest rate",
        "bank",
        "crypto",
        "bitcoin",
        "earnings",
    ],
    "politics": [
        "election",
        "government",
        "parliament",
        "president",
        "minister",
        "policy",
        "law",
        "regulation",
        "vote",
        "diplomacy",
    ],
    "technology": [
        "software",
        "hardware",
        "startup",
        "tech",
        "cyber",
        "data",
        "internet",
        "cloud",
    ],
    "entertainment": [
        "movie",
        "film",
        "music",
        "artist",
        "celebrity",
        "tv",
        "netflix",
        "concert",
        "show",
    ],
    "sports": [
        "football",
        "soccer",
        "basketball",
        "tennis",
        "cricket",
        "fifa",
        "nba",
        "goal",
        "match",
        "tournament",
    ],
    "weather": [
        "weather",
        "storm",
        "rain",
        "flood",
        "drought",
        "climate",
        "temperature",
        "forecast",
        "hurricane",
    ],
    "health": [
        "health",
        "disease",
        "virus",
        "covid",
        "vaccine",
        "medicine",
        "hospital",
        "treatment",
        "mental health",
    ],
    "environment": [
        "environment",
        "pollution",
        "sustainability",
        "wildlife",
        "conservation",
        "ecosystem",
        "carbon",
        "emissions",
        "recycling",
    ],
    "education": [
        "education",
        "school",
        "university",
        "college",
        "student",
        "teacher",
        "curriculum",
        "learning",
        "exam",
    ],
    "ai": [
        "ai",
        "airtificial intelligence",
        "machine learning",
        "neural network",
        "algorithm",
        "data science",
        "deep learning",
        "computer vision",
        "openai",
    ],
    "automotive": [
        "car",
        "automotive",
        "engine",
        "vehicle",
        "driver",
        "road",
        "traffic",
        "fuel",
        "electric",
        "hybrid"
    ]

}


def classify_topic(text: str):
    if not text:
        return {
            "category": "unknown",
            "confidence": 0.0,
            "keywords": [],
        }

    text_lower = text.lower()
    scores = defaultdict(int)

    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text_lower:
                scores[category] += 1

    if not scores:
        return {
            "category": "unknown",
            "confidence": 0.0,
            "keywords": extract_keywords(text_lower)[:10],
        }

    category = max(scores, key=scores.get)
    total = sum(scores.values())
    confidence = scores[category] / total if total else 0.0

    matched_keywords = [kw for kw in CATEGORIES[category] if kw in text_lower]

    dynamic_keywords = extract_keywords(text_lower)

    return {
        "category": category,
        "confidence": round(confidence, 2),
        "keywords": list(dict.fromkeys(matched_keywords + dynamic_keywords))[:15],
    }
