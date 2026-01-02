from app.db.session import SessionLocal
from app.analysis.topic_clustering import TopicClusterer

db = SessionLocal()
clusterer = TopicClusterer(db)

topics = clusterer.cluster(min_occurrences=8)

for topic, data in list(topics.items())[:5]:
    print(topic, "→", data)

db.close()
