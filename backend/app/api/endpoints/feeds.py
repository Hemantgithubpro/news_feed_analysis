from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Feed
from app.schemas import schemas
from worker.tasks import fetch_feed_task

router = APIRouter()

@router.post("/", response_model=schemas.Feed)
def create_feed(feed: schemas.FeedCreate, db: Session = Depends(get_db)):
    db_feed = db.query(Feed).filter(Feed.url == feed.url).first()
    if db_feed:
        raise HTTPException(status_code=400, detail="Feed already registered")
    
    new_feed = Feed(url=feed.url, name=feed.name)
    db.add(new_feed)
    db.commit()
    db.refresh(new_feed)
    
    # Trigger initial fetch
    fetch_feed_task.delay(new_feed.id)
    
    return new_feed

@router.get("/", response_model=List[schemas.Feed])
def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feeds = db.query(Feed).offset(skip).limit(limit).all()
    return feeds

@router.post("/{feed_id}/refresh")
def refresh_feed(feed_id: int, db: Session = Depends(get_db)):
    feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    task = fetch_feed_task.delay(feed_id)
    return {"message": "Feed refresh scheduled", "task_id": str(task.id)}

@router.delete("/{feed_id}")
def delete_feed(feed_id: int, db: Session = Depends(get_db)):
    feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    db.delete(feed)
    db.commit()
    return {"message": "Feed deleted"}
