from app.db.session import engine
from app.db.session import Base

Base.metadata.create_all(bind=engine)