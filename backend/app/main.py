from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import feeds, articles
from app.core.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time News Intelligence Engine")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feeds.router, prefix="/api/v1/feeds", tags=["feeds"])
app.include_router(articles.router, prefix="/api/v1/articles", tags=["articles"])

@app.get("/")
def read_root():
    return {"message": "News Intelligence Engine API is running"}
