from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from app.crawlers.base import BaseCrawler
from app.extractors.article_extractor import extract_article
from app.utils.text_cleaner import clean_text
from app.utils.dedup import content_hash
from app.models.raw_event import RawEvent


class NewsDeepCrawler(BaseCrawler):
    def __init__(self, seeds, max_articles=20):
        super().__init__()
        self.seeds = seeds
        self.max_articles = max_articles
        self.seen_hashes = set()

    def crawl(self):
        results = []

        for seed in self.seeds:
            html = self.fetch(seed)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")

            links = [
                urljoin(seed, a["href"])
                for a in soup.find_all("a", href=True)
                if self._valid_link(a["href"], seed)
            ]

            if not links:
                continue

            for link in links[: self.max_articles]:
                article_html = self.fetch(link)
                if not article_html:
                    continue

                try:
                    article = extract_article(link, article_html)

                    if not article or not article.get("content"):
                        continue

                    article["content"] = clean_text(article["content"])
                    h = content_hash(article["content"])

                    if h in self.seen_hashes:
                        continue

                    self.seen_hashes.add(h)
                    from datetime import datetime, timezone

                    article["ingested_at"] = datetime.now(timezone.utc)



                    
                    results.append(
    RawEvent(
        source="news_deep",
        url=link,
        title=article.get("title", ""),
        content=article.get("content"),
        author=article.get("author"),
        timestamp=article.get("published_at"),
        engagement=None,
        metadata={"seed": seed},
    )
)

                except Exception:
                    continue

        return results

    def _valid_link(self, href, base):
        if href.startswith("#"):
            return False
        return urlparse(urljoin(base, href)).netloc == urlparse(base).netloc
