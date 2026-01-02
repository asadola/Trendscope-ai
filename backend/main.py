from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.topics import topic_router

app = FastAPI(
    title="TrendScope AI",
    description="AI-powered trend intelligence platform",
    version="1.0.0",
)

# ✅ ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(router)
app.include_router(topic_router)  # Include the topic router
