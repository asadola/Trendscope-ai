from app.crawlers.youtube_dynamic import YouTubeTrendingCrawler


def main():
    crawler = YouTubeTrendingCrawler()
    events = crawler.crawl()

    print(f"Fetched {len(events)} YouTube events\n")

    for e in events[:5]:
        print("TITLE:", e.title)
        print("URL:", e.url)
        print("-" * 50)


if __name__ == "__main__":
    main()
