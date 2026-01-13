from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class RawEvent(BaseModel):
    # Core identifiers
    source: str
    url: str  # single source of truth

    # Flexible ingestion fields
    platform: str = "web"
    title: Optional[str] = ""
    content: Optional[str] = ""
    author: Optional[str] = "unknown"

    # Time
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None

    # Engagement & metadata
    engagement: Dict = Field(default_factory=dict)
    metadata: Dict = Field(default_factory=dict)
