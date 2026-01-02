# from fastapi import APIRouter
# from app.services.topic_service import build_topic_view

# router = APIRouter(prefix="/api/topics", tags=["Topics"])

# @router.get("/{topic}")
# def get_topic(topic: str):
#     return build_topic_view(topic)
from fastapi import APIRouter

topic_router = APIRouter(prefix="/api")

@topic_router.get("/topics/{topic}")
def topic_view(topic: str):
    return {"topic": topic, "status": "route works"}
