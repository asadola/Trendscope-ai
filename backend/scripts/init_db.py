from app.db.session import engine
from app.db.models import Base

# 🔥 CRITICAL: IMPORT ALL MODELS
from app.db.models import RawEventDB, CleanEventDB, TopicInsightDB, SubscriberDB


def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    main()
