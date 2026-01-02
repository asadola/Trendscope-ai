from typing import List
from datetime import datetime
import feedparser
from urllib.parse import quote_plus

from app.etl.extract.base import BaseExtractor
from app.models.raw_event import RawEvent


class GoogleNewsExtractor(BaseExtractor):
    """
    Extracts trending news articles using Google News RSS.
    """

    BASE_URL = "https://news.google.com/rss/search"

    def __init__(self, query: str, language: str = "en", region: str = "US"):
        self.query = query
        self.language = language
        self.region = region

    def _build_url(self) -> str:
        encoded_query = quote_plus(self.query)
        return (
            f"{self.BASE_URL}?q={encoded_query}"
            f"&hl={self.language}"
            f"&gl={self.region}"
            f"&ceid={self.region}:{self.language}"
        )

    def extract(self) -> List[RawEvent]:
        events: List[RawEvent] = []

        feed = feedparser.parse(self._build_url())

        for entry in feed.entries:
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])

            event = RawEvent(
                platform="google_news",
                source=(
                    entry.source.title
                    if hasattr(entry, "source") and hasattr(entry.source, "title")
                    else "google_news"
                ),
                title=entry.title,
                content=entry.summary if hasattr(entry, "summary") else entry.title,
                author=None,
                timestamp=datetime.utcnow(),
                published_at=published,
                engagement=None,
                url=entry.link,  # ✅ REQUIRED
                metadata={
                    "query": self.query,
                },
            )

            events.append(event)

        return events
