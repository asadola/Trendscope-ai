from app.db.session import SessionLocal
from app.db.models import SubscriberDB
from app.services.trend_velocity import get_top_trends

from app.services.email_service import send_email


def send_daily_digest():
    db = SessionLocal()

    subscribers = (
        db.query(SubscriberDB)
        .filter(SubscriberDB.is_active == True)
        .all()
    )

    top_trends = get_top_trends(db=db, limit=5)

    html = "<h2>🔥 Today’s Trending Topics</h2><ul>"
    for t in top_trends:
        html += f"<li><b>{t['topic']}</b> — {t['article_count']} articles</li>"
    html += "</ul>"

    for sub in subscribers:
        send_email(
            to=sub.email,
            subject="Your Daily TrendScope AI Update",
            html=html,
        )

    db.close()
