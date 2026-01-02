from app.db.session import SessionLocal
from app.analysis.keyword_trends import KeywordTrendAnalyzer
from app.analysis.source_share import SourceShareAnalyzer
from app.analysis.insight_generator import InsightGenerator

db = SessionLocal()

keywords = KeywordTrendAnalyzer(db).get_trending_keywords(limit=10)
sources = SourceShareAnalyzer(db).source_percentages(limit=5)
insight_gen = InsightGenerator()

insights = []

for word, count in keywords:
    insight = insight_gen.generate(topic=word, frequency=count, sources=sources)
    insights.append(insight)

for i in insights:
    print(i)

db.close()
