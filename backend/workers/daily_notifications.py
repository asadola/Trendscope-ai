from app.db.session import SessionLocal
from app.db.models import SubscriberDB
from app.analysis.trend_velocity import compute_top_trends

def send_daily_notifications():
    db = SessionLocal()

    subscribers = (
        db.query(SubscriberDB)
        .filter(SubscriberDB.is_active == True)
        .all()
    )

    top_trends = compute_top_trends(db, limit=5)

    for sub in subscribers:
        print(f"📨 Sending daily digest to {sub.email}")
        # Later: email / SMS integration

    db.close()
