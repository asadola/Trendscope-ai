from app.crawlers.google_news import GoogleNewsCrawler
from app.crawlers.hackernews import HackerNewsCrawler


def get_crawlers():
    return [
        GoogleNewsCrawler("AI regulation"),
        GoogleNewsCrawler("stock market"),
        HackerNewsCrawler(),
    ]
