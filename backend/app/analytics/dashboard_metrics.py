from app.analytics.aggregations import aggregate_keywords
from app.analytics.time_buckets import bucket_by_time
from app.analytics.category_stats import category_distribution

def build_dashboard_metrics(articles):
    buckets = bucket_by_time(articles)

    return {
        "keywords": aggregate_keywords(articles),
        "categories": category_distribution(articles),
        "trends": {
            k: aggregate_keywords(v)
            for k, v in buckets.items()
        },
    }
