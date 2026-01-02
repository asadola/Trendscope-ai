from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import CleanEventDB


class SourceShareAnalyzer:

    def __init__(self, db: Session):
        self.db = db

    def source_percentages(self, limit: int = 10):
        total = self.db.query(func.count(CleanEventDB.id)).scalar()

        rows = (
            self.db.query(
                CleanEventDB.source, func.count(CleanEventDB.id).label("count")
            )
            .group_by(CleanEventDB.source)
            .order_by(func.count(CleanEventDB.id).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "source": source,
                "count": count,
                "percentage": round((count / total) * 100, 2),
            }
            for source, count in rows
        ]
