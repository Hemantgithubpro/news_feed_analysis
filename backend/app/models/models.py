from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.core.database import Base
import datetime

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_fetched_at = Column(DateTime, nullable=True)
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

    articles = relationship("Article", back_populates="feed")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    title = Column(String, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    feed = relationship("Feed", back_populates="articles")
    analysis = relationship("AnalysisResult", back_populates="article", uselist=False)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), unique=True)
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    entities = Column(JSONB, nullable=True)
    keywords = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=func.now())

    article = relationship("Article", back_populates="analysis")
