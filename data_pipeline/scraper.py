import newspaper
from typing import List
from backend.config import settings
from backend.database import get_db
from backend.models import NewsArticle
import datetime

def scrape_and_save_news():
    """
    Scrapes news from a list of sources and saves new articles to the database.
    """
    print("Starting news scraping process...")
    db = get_db()
    collection = db.articles
    
    existing_urls = {article['url'] for article in collection.find({}, {'url': 1})}
    print(f"Found {len(existing_urls)} existing articles.")

    new_articles_count = 0
    for source_url in settings.NEWS_API_SOURCES:
        print(f"Scraping source: {source_url}")
        paper = newspaper.build(source_url, memoize_articles=False)
        
        for article in paper.articles:
            if article.url in existing_urls:
                continue

            try:
                article.download()
                article.parse()
                
                if not article.text or not article.title:
                    continue

                news_item = NewsArticle(
                    title=article.title,
                    text=article.text,
                    url=article.url,
                    source=paper.brand,
                    published_date=article.publish_date.isoformat() if article.publish_date else datetime.datetime.utcnow().isoformat()
                )
                
                collection.insert_one(news_item.dict(by_alias=True))
                existing_urls.add(article.url)
                new_articles_count += 1
                
            except Exception as e:
                print(f"Failed to process article {article.url}: {e}")

    print(f"Scraping complete. Added {new_articles_count} new articles.")
    return new_articles_count

if __name__ == '__main__':
    # This allows running the scraper directly for testing
    # Note: Requires MongoDB connection to be configured in .env
    from backend.database import connect_to_mongo, close_mongo_connection
    
    print("Running scraper as a standalone script...")
    connect_to_mongo()
    scrape_and_save_news()
    close_mongo_connection()
    print("Standalone scraper run finished.")
