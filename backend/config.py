import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI")
    DB_NAME: str = "news_mlops_free"
    NEWS_API_SOURCES: list = [
        'http://feeds.bbci.co.uk/news/rss.xml',
        'http://feeds.reuters.com/reuters/topNews',
        'http://feeds.feedburner.com/TechCrunch/'
    ]
    class Config:
        env_file = ".env"

settings = Settings()
