from app.db.session import SessionLocal
from app.repositories.events_repository import EventsRepository
from app.etl.extract.google_news_extractor import GoogleNewsExtractor
from app.etl.transform.text_cleaner import TextCleaner


def main():
    db = SessionLocal()
    repo = EventsRepository()

    extractor = GoogleNewsExtractor(query="AI regulation")
    transformer = TextCleaner()

    raw_events = extractor.extract()

    for raw in raw_events:
        clean = transformer.transform(raw)
        repo.save_raw(db, raw)
        repo.save_clean(db, clean)

    db.commit()
    db.close()

    print(f"Loaded {len(raw_events)} events into database.")


if __name__ == "__main__":
    main()
