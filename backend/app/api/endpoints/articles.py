from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app.models.models import Article, AnalysisResult
from app.schemas import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Article])
def read_articles(
    skip: int = 0, 
    limit: int = 50, 
    feed_id: Optional[int] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    
    if feed_id:
        query = query.filter(Article.feed_id == feed_id)
        
    if sentiment:
        # Join with AnalysisResult to filter by sentiment
        query = query.join(AnalysisResult).filter(AnalysisResult.sentiment_label == sentiment.upper())
    
    # Eager load analysis
    # query = query.options(joinedload(Article.analysis))
    
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("/stats/sentiment")
def get_sentiment_stats(db: Session = Depends(get_db)):
    """
    Returns the count of articles per sentiment label.
    """
    results = db.query(
        AnalysisResult.sentiment_label, 
        func.count(AnalysisResult.id)
    ).group_by(AnalysisResult.sentiment_label).all()
    
    return {label: count for label, count in results}
