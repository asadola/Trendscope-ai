from app.db.session import SessionLocal
from app.db.models import CleanEventDB
from app.classifiers.topic_classifier import classify_topic

db = SessionLocal()

rows = db.query(CleanEventDB).all()

for row in rows:
    base_text = " ".join(filter(None, [
        row.title,
        row.clean_text,
    ]))

    topic_data = classify_topic(base_text)

    row.topic = topic_data["category"]

    existing = dict(row.extra or {})   # ✅ SAFE
    existing.update({
        "keywords": topic_data["keywords"],
        "confidence": topic_data["confidence"],
    })
    row.extra = existing

db.commit()
db.close()

print(f"✔ Reclassified {len(rows)} records")
