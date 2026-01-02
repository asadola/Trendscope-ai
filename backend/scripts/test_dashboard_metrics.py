from app.analytics.dashboard_metrics import build_dashboard_metrics
from scripts.sample_articles import articles

metrics = build_dashboard_metrics(articles)
print(metrics)
