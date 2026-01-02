from app.db.session import SessionLocal
from app.analysis.keyword_trends import KeywordTrendAnalyzer

db = SessionLocal()

analyzer = KeywordTrendAnalyzer(db, hours=24)
trends = analyzer.get_trending_keywords(limit=15)

for word, count in trends:
    print(f"{word}: {count}")

db.close()
