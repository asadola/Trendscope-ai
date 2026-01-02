import requests
from bs4 import BeautifulSoup
from app.crawlers.base import BaseCrawler
from app.models.raw_event import RawEvent


class HackerNewsCrawler(BaseCrawler):
    name = "hackernews"

    def crawl(self):
        url = "https://news.ycombinator.com/"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        events = []

        for item in soup.select(".athing"):
            title_tag = item.select_one(".titleline a")
            if not title_tag:
                continue

            events.append(
                RawEvent(
                    source=self.name,
                    url=title_tag["href"],
                    title=title_tag.text,
                    metadata={},
                )
            )

        return events
