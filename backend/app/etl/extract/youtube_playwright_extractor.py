from typing import List
from datetime import datetime
import time

from playwright.sync_api import sync_playwright

from app.etl.extract.base import BaseExtractor
from app.models.raw_event import RawEvent


class YouTubePlaywrightExtractor(BaseExtractor):
    """
    Extract YouTube comments using a headless browser (Playwright).
    JS-aware, production-grade approach.
    """

    def __init__(self, video_url: str, max_comments: int = 30):
        self.video_url = video_url
        self.max_comments = max_comments

    def extract(self) -> List[RawEvent]:
        events: List[RawEvent] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.video_url, timeout=60000)

            # Let page load
            page.wait_for_timeout(5000)

            # Scroll to load comments
            for _ in range(5):
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(3000)

            comment_elements = page.query_selector_all(
                "ytd-comment-thread-renderer #content-text"
            )

            for el in comment_elements[: self.max_comments]:
                text = el.inner_text().strip()
                if not text:
                    continue

                events.append(
                    RawEvent(
                        platform="youtube",
                        source=self.video_url,
                        content=text,
                        author=None,
                        timestamp=datetime.utcnow(),
                        engagement=None,
                        url=self.video_url,
                        metadata={"method": "playwright"},
                    )
                )

            browser.close()

        return events
