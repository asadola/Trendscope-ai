from collections import defaultdict
from sqlalchemy.orm import Session
from app.db.models import CleanEventDB
import re


class TopicClusterer:
    """
    Groups keywords into topics based on co-occurrence in articles.
    """

    def __init__(self, db: Session):
        self.db = db

    def _extract_keywords(self, text: str):
        return set(re.findall(r"\b[a-z]{3,}\b", text.lower()))

    def cluster(self, min_occurrences: int = 5):
        rows = self.db.query(CleanEventDB.clean_text).all()

        keyword_docs = defaultdict(int)
        co_occurrence = defaultdict(set)

        for (text,) in rows:
            keywords = self._extract_keywords(text)
            for kw in keywords:
                keyword_docs[kw] += 1
                co_occurrence[kw].update(keywords)

        topics = {}
        for kw, count in keyword_docs.items():
            if count >= min_occurrences:
                related = [
                    r
                    for r in co_occurrence[kw]
                    if keyword_docs.get(r, 0) >= min_occurrences and r != kw
                ]
                topics[kw] = {"frequency": count, "related_terms": related[:10]}

        return topics
