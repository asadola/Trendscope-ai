from collections import Counter
from datetime import datetime, timedelta
import re

from sqlalchemy.orm import Session
from app.db.models import CleanEventDB


STOPWORDS = {
    "the",
    "and",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "is",
    "are",
    "this",
    "that",
    "from",
    "as",
    "by",
}


class KeywordTrendAnalyzer:
    """
    Extracts trending keywords from clean_events.
    """

    def __init__(self, db: Session, hours: int = 24):
        self.db = db
        self.hours = hours

    def _tokenize(self, text: str):
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        return [w for w in words if w not in STOPWORDS]

    def get_trending_keywords(self, limit: int = 20):
        since = datetime.utcnow() - timedelta(hours=self.hours)

        rows = (
            self.db.query(CleanEventDB.clean_text)
            .filter(CleanEventDB.timestamp >= since)
            .all()
        )

        counter = Counter()

        for (text,) in rows:
            counter.update(self._tokenize(text))

        return counter.most_common(limit)
