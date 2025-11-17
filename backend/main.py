from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from bson import ObjectId

from backend.database import connect_to_mongo, close_mongo_connection, get_db
from backend.models import NewsArticle, SummarizeRequest, CategorizeRequest, SentimentRequest
from ml.summarizer import summarize_text, load_summarizer
from ml.categorizer import categorize_text, load_categorizer
from ml.sentiment import analyze_sentiment, load_sentiment_analyzer
from data_pipeline.scraper import scrape_and_save_news
from apscheduler.schedulers.background import BackgroundScheduler
import mlflow
import mlflow.pytorch

# Initialize FastAPI app
app = FastAPI(
    title="News MLOps Free",
    description="A free, end-to-end MLOps project for news processing.",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing)
origins = ["*"]  # Allow all origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MLFlow Setup ---
# Set up a local tracking URI
mlflow.set_tracking_uri("file:./mlruns")

# --- Background Job Scheduler ---
scheduler = BackgroundScheduler()

def refresh_news_job():
    """
    The background job that scrapes news and runs ML models.
    """
    print("Running scheduled job: Refreshing news and applying ML models...")
    with mlflow.start_run(run_name="Automated News Pipeline") as run:
        # 1. Scrape new articles
        new_count = scrape_and_save_news()
        mlflow.log_param("new_articles_scraped", new_count)
        
        if new_count > 0:
            # 2. Process articles that need ML processing
            db = get_db()
            articles_to_process = db.articles.find({"summary": None}) # Process if summary is missing
            
            processed_count = 0
            for article_data in articles_to_process:
                article_id = article_data['_id']
                text = article_data['text']
                
                # Run ML models
                summary = summarize_text(text)
                category = categorize_text(text)
                sentiment = analyze_sentiment(text)
                
                # Update article in DB
                db.articles.update_one(
                    {"_id": article_id},
                    {"$set": {
                        "summary": summary,
                        "category": category,
                        "sentiment": sentiment
                    }}
                )
                processed_count += 1
            
            print(f"Processed {processed_count} articles with ML models.")
            mlflow.log_metric("articles_processed_ml", processed_count)
        else:
            print("No new articles to process.")
            mlflow.log_metric("articles_processed_ml", 0)
            
    print("Scheduled job finished.")


# --- App Events (Startup and Shutdown) ---
@app.on_event("startup")
def startup_event():
    """
    On startup, connect to DB, load ML models, and start background job.
    """
    print("Application startup...")
    connect_to_mongo()
    
    # Pre-load ML models to avoid cold starts on first request
    print("Loading ML models...")
    load_summarizer()
    load_categorizer()
    load_sentiment_analyzer()
    print("ML models loaded.")
    
    # Start the background job scheduler
    # It will run the job once immediately, then every 4 hours
    scheduler.add_job(refresh_news_job, 'interval', hours=4, id="news_refresh_job", replace_existing=True)
    scheduler.start()
    print("Background scheduler started.")

@app.on_event("shutdown")
def shutdown_event():
    """
    On shutdown, close DB connection and shut down scheduler.
    """
    print("Application shutdown...")
    scheduler.shutdown()
    close_mongo_connection()
    print("Shutdown complete.")

# --- API Endpoints ---
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the News MLOps Free API!"}

@app.get("/news", response_model=List[NewsArticle], tags=["News"])
def get_news(limit: int = 20):
    """
    Retrieve the latest news articles that have been processed.
    """
    db = get_db()
    # Fetch articles that have a summary (i.e., have been processed)
    articles = db.articles.find({"summary": {"$ne": None}}).sort("published_date", -1).limit(limit)
    return list(articles)

@app.post("/summarize", tags=["ML Models"])
def summarize(request: SummarizeRequest):
    """
    Summarize a piece of text.
    """
    with mlflow.start_run(run_name="Single Summarization") as run:
        summary = summarize_text(request.text)
        mlflow.log_param("input_length", len(request.text))
        mlflow.log_param("output_length", len(summary))
        return {"summary": summary}

@app.post("/categorize", tags=["ML Models"])
def categorize(request: CategorizeRequest):
    """
    Categorize a piece of text.
    """
    with mlflow.start_run(run_name="Single Categorization") as run:
        category = categorize_text(request.text)
        mlflow.log_param("input_text", request.text[:100]) # Log snippet
        mlflow.log_param("category", category)
        return {"category": category}

@app.post("/sentiment", tags=["ML Models"])
def sentiment(request: SentimentRequest):
    """
    Analyze the sentiment of a piece of text.
    """
    with mlflow.start_run(run_name="Single Sentiment Analysis") as run:
        sentiment_result = analyze_sentiment(request.text)
        mlflow.log_param("label", sentiment_result['label'])
        mlflow.log_metric("score", sentiment_result['score'])
        return sentiment_result

@app.post("/refresh_news", tags=["Admin"])
def refresh_news(background_tasks: BackgroundTasks):
    """
    Manually trigger the background job to scrape and process news.
    """
    background_tasks.add_task(refresh_news_job)
    return {"message": "News refresh job has been triggered in the background."}
