from app.etl.extract.youtube_playwright_extractor import YouTubePlaywrightExtractor
from app.etl.transform.text_cleaner import TextCleaner

url = "https://www.youtube.com/watch?v=VIDEO_ID_HERE"

extractor = YouTubePlaywrightExtractor(url, max_comments=10)
transformer = TextCleaner()

raw_events = extractor.extract()
print("Raw events:", len(raw_events))

for raw in raw_events[:5]:
    clean = transformer.transform(raw)
    print("RAW:", raw.content)
    print("CLEAN:", clean.clean_text)
    print("LANG:", clean.language)
    print("-" * 40)
