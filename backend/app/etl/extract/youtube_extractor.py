from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import re

from app.etl.extract.base import BaseExtractor
from app.models.raw_event import RawEvent
from app.services.http_client import fetch


class YouTubeExtractor(BaseExtractor):
    """
    Extracts public video metadata and comments from YouTube.
    NO API. NO LOGIN.
    """

    def __init__(self, video_url: str):
        self.video_url = video_url

    def extract(self) -> List[RawEvent]:
        html = fetch(self.video_url)
        soup = BeautifulSoup(html, "lxml")

        events: List[RawEvent] = []

        # --- VIDEO TITLE ---
        title_tag = soup.find("title")
        title = title_tag.text.replace("- YouTube", "").strip() if title_tag else ""

        # --- VIDEO ID ---
        match = re.search(r"v=([^&]+)", self.video_url)
        video_id = match.group(1) if match else None

        # --- COMMENTS (LIMITED – PUBLIC SNAPSHOT) ---
        for comment in soup.select("yt-formatted-string#content-text")[:20]:
            text = comment.text.strip()
            if not text:
                continue

            events.append(
                RawEvent(
                    platform="youtube",
                    source=video_id or "unknown_video",
                    content=text,
                    author=None,
                    timestamp=datetime.utcnow(),
                    engagement=None,
                    url=self.video_url,
                    metadata={"video_title": title},
                )
            )

        return events
