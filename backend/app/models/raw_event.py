from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class RawEvent(BaseModel):
    platform: str
    source: str
    title: str
    content: str
    author: Optional[str]
    timestamp: datetime
    engagement: Optional[Dict]
    url: str                 # ✅ SINGLE SOURCE OF TRUTH
    published_at: Optional[datetime] = None  # ✅
    metadata: Optional[Dict] = {}
