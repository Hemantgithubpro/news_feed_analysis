import feedparser
import newspaper
from sqlalchemy.orm import Session
from datetime import datetime
import time

from worker.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.models import Feed, Article, AnalysisResult
from worker.nlp_engine import nlp_engine

def get_db_session():
    return SessionLocal()

@celery_app.task
def schedule_feed_fetches():
    """
    Periodic task to check all active feeds and schedule a fetch task for them.
    """
    db = get_db_session()
    try:
        feeds = db.query(Feed).filter(Feed.is_active == True).all()
        for feed in feeds:
            fetch_feed_task.delay(feed.id)
    finally:
        db.close()

@celery_app.task
def fetch_feed_task(feed_id: int):
    """
    Fetches RSS feed, parses it, and triggers processing for new articles.
    """
    db = get_db_session()
    try:
        feed = db.query(Feed).filter(Feed.id == feed_id).first()
        if not feed:
            return f"Feed {feed_id} not found"

        print(f"Fetching feed: {feed.name} ({feed.url})")
        parsed_feed = feedparser.parse(feed.url)
        
        # Simple error handling
        if parsed_feed.bozo:
             feed.error_count += 1
             # Only save if we want to track errors persistently
             db.commit()
             print(f"Error parsing feed {feed.url}: {parsed_feed.bozo_exception}")
             # We might continue if it's just a malformed XML warning, but for now let's proceed carefully
        else:
             feed.error_count = 0 
             feed.last_fetched_at = datetime.utcnow()
             db.commit()

        new_articles_count = 0
        for entry in parsed_feed.entries:
            # Check for duplication
            existing = db.query(Article).filter(Article.url == entry.link).first()
            if existing:
                continue

            # Process new article
            process_article_task.delay(feed_id, entry)
            new_articles_count += 1
        
        return f"Feed {feed_id} processed. {new_articles_count} new articles found."

    except Exception as e:
        print(f"Error in fetch_feed_task for feed {feed_id}: {str(e)}")
        # In a real app, you might want to log this to the DB or a file
    finally:
        db.close()

@celery_app.task
def process_article_task(feed_id: int, entry_data: dict):
    """
    Downloads full text, runs NLP, and saves to DB.
    """
    db = get_db_session()
    try:
        url = entry_data.get('link')
        title = entry_data.get('title')
        
        # 1. Full text extraction
        print(f"Processing article: {title}")
        article_text = ""
        try:
            # Use newspaper3k to valid and download
            news_article = newspaper.Article(url)
            news_article.download()
            news_article.parse()
            article_text = news_article.text
        except Exception as e:
            print(f"Failed to extract text for {url}: {e}")
            # Fallback to description if available
            article_text = entry_data.get('summary', '') or entry_data.get('description', '')

        if not article_text:
            print(f"No text content found for {url}. Skipping NLP, but saving record.")
        
        # 2. NLP Analysis
        nlp_results = {
            "sentiment_score": 0.0,
            "sentiment_label": "NEUTRAL",
            "entities": [],
            "keywords": []
        }
        
        if article_text:
            nlp_results = nlp_engine.analyze_text(article_text[:5000]) # Limit text length for performance

        # 3. Save to DB
        # Convert published_at struct_time to datetime if possible
        published_at = datetime.utcnow()
        if 'published_parsed' in entry_data and entry_data.get('published_parsed'):
             try:
                published_at = datetime.fromtimestamp(time.mktime(entry_data.get('published_parsed')))
             except:
                pass

        new_article = Article(
            feed_id=feed_id,
            title=title,
            url=url,
            content=article_text,
            published_at=published_at
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)

        analysis = AnalysisResult(
            article_id=new_article.id,
            sentiment_score=nlp_results['sentiment_score'],
            sentiment_label=nlp_results['sentiment_label'],
            entities=nlp_results['entities'],
            keywords=nlp_results['keywords']
        )
        db.add(analysis)
        db.commit()

        return f"Article processed: {new_article.id}"

    except Exception as e:
        print(f"Error processing article {entry_data.get('link')}: {e}")
        db.rollback()
    finally:
        db.close()
