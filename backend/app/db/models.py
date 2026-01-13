from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Text,
    Boolean,
    func,
)
from datetime import datetime, timezone
from app.db.session import Base


class RawEventDB(Base):
    __tablename__ = "raw_events"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    source = Column(String, index=True)
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    engagement = Column(JSON)
    url = Column(Text)
    extra = Column(JSON)


class CleanEventDB(Base):
    __tablename__ = "clean_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    platform = Column(String, index=True)
    source = Column(String, index=True)
    clean_text = Column(Text)
    language = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    engagement = Column(JSON)
    url = Column(Text)
    ingested_at = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    extra = Column(JSON, default=dict)

    topic = Column(String, index=True)


class TopicInsightDB(Base):
    __tablename__ = "topic_insights"

    id = Column(Integer, primary_key=True)
    topic = Column(String, index=True, unique=True)
    category = Column(String, index=True)

    explanation = Column(Text)
    why_it_matters = Column(Text)
    key_points = Column(JSON)
    sources = Column(JSON)

    confidence = Column(Integer)
    generated_at = Column(DateTime, default=func.now())


class SubscriberDB(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    ip_address = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
