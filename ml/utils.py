from transformers import pipeline
import os

def get_summarizer():
    """
    Initializes and returns the summarization pipeline.
    """
    # Use a smaller model for quicker local setup if needed
    # model_name = "sshleifer/distilbart-cnn-6-6" 
    model_name = "facebook/bart-large-cnn"
    print(f"Loading summarizer model: {model_name}")
    return pipeline("summarization", model=model_name)

def get_categorizer():
    """
    Initializes and returns the text classification pipeline for categorization.
    """
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    print(f"Loading categorizer model: {model_name}")
    # This is a sentiment model, but we'll use it as a stand-in for categorization
    # For a real scenario, you'd fine-tune a model on your specific categories
    return pipeline("text-classification", model=model_name)

def get_sentiment_analyzer():
    """
    Initializes and returns the sentiment analysis pipeline.
    """
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    print(f"Loading sentiment analyzer model: {model_name}")
    return pipeline("sentiment-analysis", model=model_name)

# Example of how to use these functions
if __name__ == '__main__':
    # This block will only run when the script is executed directly
    # It's useful for testing the model loading process
    
    print("Testing model loaders...")
    
    # Test summarizer
    try:
        summarizer = get_summarizer()
        print("Summarizer loaded successfully.")
        del summarizer
    except Exception as e:
        print(f"Error loading summarizer: {e}")

    # Test categorizer
    try:
        categorizer = get_categorizer()
        print("Categorizer loaded successfully.")
        del categorizer
    except Exception as e:
        print(f"Error loading categorizer: {e}")

    # Test sentiment analyzer
    try:
        sentiment_analyzer = get_sentiment_analyzer()
        print("Sentiment analyzer loaded successfully.")
        del sentiment_analyzer
    except Exception as e:
        print(f"Error loading sentiment analyzer: {e}")

    print("Model loading tests complete.")
