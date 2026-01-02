from app.etl.transform.text_cleaner import TextCleaner
from app.etl.extract.youtube_extractor import YouTubeExtractor

extractor = YouTubeExtractor("https://www.youtube.com/watch?v=VIDEO_ID_HERE")
transformer = TextCleaner()

raw_events = extractor.extract()

for raw in raw_events[:5]:
    clean = transformer.transform(raw)
    print("RAW:", raw.content)
    print("CLEAN:", clean.clean_text)
    print("LANG:", clean.language)
    print("-" * 40)

print("Extractor running...")

raw_events = extractor.extract()

print("Raw events count:", len(raw_events))
