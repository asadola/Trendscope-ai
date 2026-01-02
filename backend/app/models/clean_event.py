from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class CleanEvent(BaseModel):
    title: Optional[str]
    platform: str
    source: str
    clean_text: str
    language: Optional[str] = None   
    timestamp: datetime
    published_at: Optional[datetime] = None
    engagement: Optional[Dict[str, int]]
    url: Optional[str]
    topic: Optional[str]
    metadata: Optional[Dict]
