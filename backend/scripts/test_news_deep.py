from app.config.news_seeds import NEWS_SEEDS
from app.crawlers.news_deep_crawler import NewsDeepCrawler


def main():
    crawler = NewsDeepCrawler(NEWS_SEEDS, max_articles=10)
    articles = crawler.crawl()

    print(f"Fetched {len(articles)} articles\n")
    for a in articles[:5]:
        print("TITLE:", a["title"])
        print("URL:", a["url"])
        print("-" * 40)


if __name__ == "__main__":
    main()
