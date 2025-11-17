from fastapi.testclient import TestClient
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the News MLOps Free API!"}

def test_get_news_unauthenticated():
    """
    Test the /news endpoint. 
    This will likely fail if the database is empty, which is expected on a fresh test run.
    A better test would mock the database.
    """
    response = client.get("/news")
    assert response.status_code == 200
    # Expect an empty list if the DB is empty
    assert isinstance(response.json(), list)

def test_summarize_endpoint():
    """
    Test the /summarize endpoint with some sample text.
    """
    sample_text = ("In a landmark decision, the city council has approved the construction of a new "
                   "state-of-the-art public library. The project, which is expected to break ground "
                   "next year, aims to provide residents with access to a vast collection of digital "
                   "and print resources. The library will also feature community spaces, a tech lab, "
                   "and a children's wing. Officials hope it will become a central hub for learning "
                   "and community engagement.")
    response = client.post("/summarize", json={"text": sample_text})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert len(data["summary"]) > 0
    assert len(data["summary"]) < len(sample_text)

def test_categorize_endpoint():
    """
    Test the /categorize endpoint.
    """
    response = client.post("/categorize", json={"text": "This is a test of the categorization system."})
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    # The placeholder model returns 'Technology' or 'Business'
    assert data["category"] in ["Technology", "Business"]

def test_sentiment_endpoint():
    """
    Test the /sentiment endpoint.
    """
    response = client.post("/sentiment", json={"text": "I love this new library project!"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
