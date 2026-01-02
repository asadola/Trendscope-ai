from app.crawlers.google_news import GoogleNewsCrawler

crawler = GoogleNewsCrawler("AI regulation")
events = crawler.crawl()

print(f"Fetched {len(events)} events")
print(events[0])
