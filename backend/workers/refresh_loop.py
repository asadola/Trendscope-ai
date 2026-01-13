from app.db.session import SessionLocal
from app.crawlers import run_all_crawlers
from app.services.trend_velocity import recompute_all_trends
from app.services.topic_ai_insight_service import refresh_stale_insights
import time
from datetime import datetime, timezone

REFRESH_INTERVAL_SECONDS = 300  # 5 minutes


def run_once():
    db = SessionLocal()
    try:
        run_all_crawlers(db)
        recompute_all_trends(db)
        refresh_stale_insights(db)
        db.commit()
    except Exception as e:
        db.rollback()
        print("❌ Worker error:", e)
    finally:
        db.close()


def main():
    print("🧠 TrendScope background worker started")

    while True:
        print(f"🔁 Cycle started at {datetime.now(timezone.utc).isoformat()}")
        run_once()
        print(f"😴 Sleeping for {REFRESH_INTERVAL_SECONDS}s\n")
        time.sleep(REFRESH_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
