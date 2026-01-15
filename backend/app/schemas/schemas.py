from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Any
from datetime import datetime

# Feed Schemas
class FeedBase(BaseModel):
    url: str
    name: str

class FeedCreate(FeedBase):
    pass

class Feed(FeedBase):
    id: int
    is_active: bool
    last_fetched_at: Optional[datetime] = None
    error_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis Schemas
class AnalysisResultBase(BaseModel):
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    entities: Optional[List[Any]]
    keywords: Optional[List[str]]

class AnalysisResult(AnalysisResultBase):
    id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    url: str
    content: Optional[str] = None
    published_at: Optional[datetime] = None

class Article(ArticleBase):
    id: int
    feed_id: int
    created_at: datetime
    analysis: Optional[AnalysisResult] = None

    class Config:
        from_attributes = True
