from app.etl.extract.x_extractor import XExtractor

extractor = XExtractor(query="AI regulation", limit=10)
events = extractor.extract()

for e in events:
    print(e.json())
