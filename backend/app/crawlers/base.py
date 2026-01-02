import time
import random
import requests
from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    def __init__(self, delay=(1.5, 3.5)):
        self.session = requests.Session()
        self.delay = delay
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
            }
        )

    def wait(self):
        time.sleep(random.uniform(*self.delay))

    def fetch(self, url):
        self.wait()
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code >= 400:
                return None
            return resp.text
        except Exception:
            return None

    @abstractmethod
    def crawl(self):
        pass
