from app.ai.category_summaries import summarize_by_category
from scripts.sample_articles import articles

summaries = summarize_by_category(articles)

for k, v in summaries.items():
    print(f"\n[{k.upper()}]\n{v}")
