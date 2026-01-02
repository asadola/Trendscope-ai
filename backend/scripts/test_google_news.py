from app.etl.extract.google_news_extractor import GoogleNewsExtractor
from app.etl.transform.text_cleaner import TextCleaner

extractor = GoogleNewsExtractor(query="AI regulation", language="en", region="US")

transformer = TextCleaner()

raw_events = extractor.extract()
print("Raw events:", len(raw_events))

for raw in raw_events[:5]:
    clean = transformer.transform(raw)
    print("RAW:", raw.content)
    print("CLEAN:", clean.clean_text)
    print("LANG:", clean.language)
    print("SOURCE:", raw.source)
    print("-" * 40)
