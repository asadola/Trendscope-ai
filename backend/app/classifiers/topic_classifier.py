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
        "artificial intelligence",
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
    # ✅ absolute safety
    if not text or not text.strip():
        return {
            "category": "general",
            "confidence": 0.0,
            "keywords": [],
        }

    text_lower = text.lower()
    scores = defaultdict(int)

    # 1️⃣ keyword scoring
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if " " in kw:
                if all(token in text_lower for token in kw.split()):
                    scores[category] += 2
            else:
                if kw in text_lower:
                    scores[category] += 1

    # 2️⃣ ALWAYS extract keywords
    extracted = extract_keywords(text_lower)[:15]

    # 3️⃣ no strong match → heuristic rescue
    if not scores or max(scores.values()) < 2:
        if any(k in extracted for k in ["ai", "model", "algorithm", "llm"]):
            return {
                "category": "ai",
                "confidence": 0.35,
                "keywords": extracted,
            }

        if any(k in extracted for k in ["law", "bill", "regulation", "policy"]):
            return {
                "category": "politics",
                "confidence": 0.35,
                "keywords": extracted,
            }

        return {
            "category": "general",
            "confidence": 0.25,
            "keywords": extracted,
        }

    # 4️⃣ strong match
    category = max(scores, key=scores.get)
    max_score = scores[category]
    second_best = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0

    confidence = round(
        max(0.4, (max_score - second_best) / max_score),
        2
    )

    matched_keywords = [kw for kw in CATEGORIES[category] if kw in text_lower]

    return {
        "category": category,
        "confidence": confidence,
        "keywords": list(dict.fromkeys(matched_keywords + extracted))[:15],
    }
