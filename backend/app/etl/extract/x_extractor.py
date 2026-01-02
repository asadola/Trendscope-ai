from datetime import datetime
from typing import List

import snscrape.modules.twitter as sntwitter

from app.etl.extract.base import BaseExtractor
from app.models.raw_event import RawEvent


class XExtractor(BaseExtractor):
    """
    Extracts public posts from X (Twitter) using snscrape.
    No API. No login.
    """

    def __init__(self, query: str, limit: int = 50):
        self.query = query
        self.limit = limit

    def extract(self) -> List[RawEvent]:
        events: List[RawEvent] = []

        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(self.query).get_items()
        ):
            if i >= self.limit:
                break

            events.append(
                RawEvent(
                    platform="x",
                    source=self.query,
                    content=tweet.content,
                    author=tweet.user.username if tweet.user else None,
                    timestamp=tweet.date,
                    engagement={
                        "likes": tweet.likeCount,
                        "retweets": tweet.retweetCount,
                        "replies": tweet.replyCount,
                    },
                    url=tweet.url,
                    metadata={
                        "hashtags": tweet.hashtags,
                        "lang": tweet.lang,
                    },
                )
            )

        return events
