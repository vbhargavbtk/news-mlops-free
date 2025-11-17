# News MLOps Free

This is a complete, end-to-end MLOps project designed to be a free learning resource. It includes a news scraper, ML models for text processing, a FastAPI backend, a simple frontend, and a full CI/CD pipeline for automated deployment.

## Features

- **News Scraper**: Scrapes articles from multiple RSS feeds using `Newspaper3k`.
- **ML Models**:
    - **Summarizer**: `facebook/bart-large-cnn` for abstractive summarization.
    - **Categorizer**: `distilbert-base-uncased` (placeholder) for news categorization.
    - **Sentiment Analyzer**: `distilbert-base-uncased-finetuned-sst-2-english` for sentiment analysis.
- **Backend**: A robust `FastAPI` server with endpoints for serving news and running ML models.
- **Database**: `MongoDB Atlas` (free tier) for storing news articles.
- **Frontend**: A simple, responsive UI built with `HTML`, `CSS`, `JavaScript`, and `Bootstrap`.
- **Containerization**: `Docker` for the backend and `docker-compose` for local development.
- **CI/CD**: `GitHub Actions` for continuous integration and deployment to `Render`.
- **MLOps Tooling**:
    - `DVC`: For data and model versioning (conceptual setup).
    - `MLflow`: For local experiment tracking.

## Project Structure

```
.
├── .github/workflows/  # CI/CD pipeline
├── backend/            # FastAPI application
├── data/               # Raw and processed data (tracked by DVC)
├── data_pipeline/      # News scraping scripts
├── docker/             # Dockerfiles
├── docs/               # Project documentation
├── frontend/           # HTML, CSS, JS frontend
├── ml/                 # ML model logic and utilities
├── models/             # Trained model artifacts (tracked by DVC)
├── tests/              # Backend API tests
├── .env.example        # Environment variable template
├── .gitignore
├── dvc.yaml            # DVC pipeline definition
├── docker-compose.yml  # Local development setup
└── README.md
```

## Getting Started

Follow the deployment guide to get this project running live on the web and locally on your machine.

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.9+](https://www.python.org/downloads/)
- A [GitHub](https://github.com/) account
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (free tier)
- A [Render](https://render.com/) account (free tier)
- A [Netlify](https://www.netlify.com/) account (free tier)

## Deployment Guide

Follow the step-by-step instructions provided by the Gemini CLI to deploy this application.

## Local Development

To run the project locally using Docker:

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd news-mlops-free
    ```

2.  **Set up environment variables:**
    - Rename `.env.example` to `.env`.
    - Add your `MONGO_URI` from your MongoDB Atlas cluster.

3.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    The backend will be available at `http://localhost:8000`.

4.  **Run the frontend:**
    - Open the `frontend/index.html` file in your browser.
    - **Important**: You will need to update the `API_BASE_URL` in `frontend/js/app.js` to `http://localhost:8000` for local testing.

## API Endpoints

- `GET /news`: Fetches the latest processed news articles.
- `POST /summarize`: Summarizes a given text.
- `POST /categorize`: Categorizes a given text.
- `POST /sentiment`: Analyzes the sentiment of a given text.
- `POST /refresh_news`: Manually triggers the news scraping and processing pipeline.
- `GET /docs`: Access the interactive API documentation (Swagger UI).
