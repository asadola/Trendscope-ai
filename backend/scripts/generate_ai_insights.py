from app.db.session import SessionLocal
from app.analysis.keyword_trends import KeywordTrendAnalyzer
from app.analysis.source_share import SourceShareAnalyzer
from app.ai.local_llm import LocalLLM
from app.ai.prompts import trend_summary_prompt

db = SessionLocal()

keywords = KeywordTrendAnalyzer(db).get_trending_keywords(limit=5)
sources = SourceShareAnalyzer(db).source_percentages(limit=5)

llm = LocalLLM(model="llama3.1")

for topic, freq in keywords:
    prompt = trend_summary_prompt(topic, freq, sources)
    summary = llm.generate(prompt)

    print("TOPIC:", topic)
    print(summary)
    print("-" * 50)

db.close()
