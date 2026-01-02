from sqlalchemy.orm import Session
from app.db.models import RawEventDB, CleanEventDB
from app.models.raw_event import RawEvent
from app.models.clean_event import CleanEvent


class EventsRepository:

    def save_raw(self, db: Session, event: RawEvent):
        db_event = RawEventDB(
            platform=event.platform,
            source=event.source,
            content=event.content,
            timestamp=event.timestamp,
            engagement=event.engagement,
            url=event.url,
            extra=event.metadata,  # map metadata → extra
        )
        db.add(db_event)

    def save_clean(self, db: Session, event: CleanEvent):
        db_event = CleanEventDB(
            title=event.title,
            platform=event.platform,
            source=event.source,
            clean_text=event.clean_text,
            language=event.language,
            timestamp=event.timestamp,
            published_at=event.published_at,
            engagement=event.engagement,
            url=event.url,
            extra=event.metadata,  # map metadata → extra
            topic=event.topic,
        )
        db.add(db_event)
