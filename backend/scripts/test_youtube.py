from app.etl.extract.youtube_extractor import YouTubeExtractor

url = "https://www.youtube.com/watch?v=VIDEO_ID_HERE"
extractor = YouTubeExtractor(url)

events = extractor.extract()

for e in events:
    print(e.json())
