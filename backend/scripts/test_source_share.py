from app.db.session import SessionLocal
from app.analysis.source_share import SourceShareAnalyzer

db = SessionLocal()
analyzer = SourceShareAnalyzer(db)

for row in analyzer.source_percentages():
    print(row)

db.close()
