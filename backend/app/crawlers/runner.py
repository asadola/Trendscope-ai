from app.crawlers.registry import get_crawlers


def run_all_crawlers():
    all_events = []

    for crawler in get_crawlers():
        try:
            events = crawler.crawl()
            all_events.extend(events)
        except Exception as e:
            print(f"[ERROR] {crawler.name}: {e}")

    return all_events
