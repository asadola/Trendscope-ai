import feedparser
from datetime import datetime
from urllib.parse import quote_plus

from app.crawlers.base import BaseCrawler
from app.models.raw_event import RawEvent


class GoogleNewsCrawler(BaseCrawler):
    name = "google_news"

    def __init__(self, query: str, region="US", language="en"):
        self.query = query
        self.region = region
        self.language = language

    def crawl(self):
        encoded_query = quote_plus(self.query)

        url = (
            f"https://news.google.com/rss/search?"
            f"q={encoded_query}"
            f"&hl={self.language}"
            f"&gl={self.region}"
            f"&ceid={self.region}:{self.language}"
        )

        feed = feedparser.parse(url)
        events = []

        for entry in feed.entries:
            events.append(
                RawEvent(
                    source=self.name,
                    url=entry.link,
                    title=entry.title,
                    published_at=(
                        datetime(*entry.published_parsed[:6])
                        if hasattr(entry, "published_parsed")
                        else None
                    ),
                    language=self.language,
                    region=self.region,
                    metadata={"publisher": entry.get("source", {}).get("title")},
                )
            )

        return events
