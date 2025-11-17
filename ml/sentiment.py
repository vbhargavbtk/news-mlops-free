from ml.utils import get_sentiment_analyzer

sentiment_analyzer = None

def load_sentiment_analyzer():
    """Loads the sentiment analysis model into memory."""
    global sentiment_analyzer
    if sentiment_analyzer is None:
        sentiment_analyzer = get_sentiment_analyzer()

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of the given text.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        dict: A dictionary containing the label and score.
    """
    if sentiment_analyzer is None:
        load_sentiment_analyzer()
        
    try:
        result = sentiment_analyzer(text)
        return result[0]
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return {"label": "UNKNOWN", "score": 0.0}
