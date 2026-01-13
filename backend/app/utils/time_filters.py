from datetime import datetime, timedelta

def fresh_since(days=7, hours=0):
    return datetime.utcnow() - timedelta(days=days, hours=hours)
