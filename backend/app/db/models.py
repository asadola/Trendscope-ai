from sqlalchemy import Column, Integer, String, DateTime, JSON, Text , func
from datetime import datetime
from app.db.session import Base
from sqlalchemy.ext.declarative import declarative_base




class RawEventDB(Base):
    __tablename__ = "raw_events"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    source = Column(String, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    engagement = Column(JSON)
    url = Column(Text)
    extra = Column(JSON)  # ← renamed from metadata


class CleanEventDB(Base):
    __tablename__ = "clean_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    platform = Column(String, index=True)
    source = Column(String, index=True)
    clean_text = Column(Text)
    language = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    engagement = Column(JSON)
    url = Column(Text)
    published_at = Column(DateTime)
    ingested_at = Column(DateTime)
    extra = Column(JSON)  # ← renamed from metadata

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

    # ✅ ADD THESE
    confidence = Column(Integer)  # 0–100
    generated_at = Column(DateTime, default=func.now())