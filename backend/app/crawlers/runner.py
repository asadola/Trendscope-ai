from app.crawlers.registry import get_crawlers
from app.repositories.events_repository import EventsRepository
from app.etl.transform.text_cleaner import TextCleaner


def run_all_crawlers(db):
    repo = EventsRepository()
    cleaner = TextCleaner()
    total = 0

    for crawler in get_crawlers():
        try:
            print(f"🌍 Crawling {crawler.name}...")
            events = crawler.crawl()

            for raw_event in events:
                # Save raw event
                repo.save_raw(db, raw_event)

                # Transform + save clean event
                try:
                    clean_event = cleaner.transform(raw_event)
                    repo.save_clean(db, clean_event)
                except Exception as e:
                    print(f"[WARN] Clean failed: {e}")

            total += len(events)

        except Exception as e:
            print(f"[ERROR] {crawler.name}: {e}")

    db.commit()
    print(f"✅ Saved {total} raw events (and cleaned)")
