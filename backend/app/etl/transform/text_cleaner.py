from datetime import datetime, timezone

from email.mime import text
import re
from langdetect import detect, LangDetectException

from app.etl.transform.base import BaseTransformer
from app.models.raw_event import RawEvent
from app.models.clean_event import CleanEvent
from app.classifiers.topic_classifier import classify_topic


class TextCleaner(BaseTransformer):

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"@\w+", "", text)
        text = re.sub(r"#\w+", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def detect_language(self, text: str):
        try:
            return detect(text)
        except LangDetectException:
            return None
    
    def transform(self, event: RawEvent) -> CleanEvent:
    # 🔥 FALLBACK LOGIC
        base_text = event.content or event.title or ""

        cleaned = self.clean_text(base_text)
        lang = self.detect_language(cleaned) if cleaned else None

        topic_data = classify_topic(cleaned)

        return CleanEvent(
            title=event.title,
            platform=event.platform,
            source=event.source,
            clean_text=cleaned,
            language=lang,
            timestamp=event.timestamp,
            published_at=event.published_at,
            ingested_at=datetime.utcnow(),
            engagement=event.engagement,
            url=event.url,
            topic=topic_data["category"],
            metadata={
            **(event.metadata or {}),
            "keywords": topic_data["keywords"],
            "confidence": topic_data["confidence"],
        },
    )
