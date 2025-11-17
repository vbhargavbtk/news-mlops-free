from ml.utils import get_categorizer

categorizer = None

def load_categorizer():
    """Loads the categorizer model into memory."""
    global categorizer
    if categorizer is None:
        categorizer = get_categorizer()

def categorize_text(text: str) -> str:
    """
    Categorizes the given text.
    
    NOTE: This is a placeholder using a sentiment model. For a real-world
    application, you would replace this with a model fine-tuned on your
    specific news categories (e.g., 'Technology', 'Sports', 'Politics').
    
    Args:
        text (str): The text to categorize.
        
    Returns:
        str: The predicted category (e.g., 'POSITIVE'/'NEGATIVE' in this placeholder).
    """
    if categorizer is None:
        load_categorizer()
        
    try:
        # Since we're using a sentiment model as a stand-in, the labels will be
        # 'POSITIVE' or 'NEGATIVE'. We'll map them to broader, fake categories.
        result = categorizer(text)
        sentiment_label = result[0]['label']
        
        # Example mapping to fake news categories
        if sentiment_label == 'POSITIVE':
            return 'Technology'
        else:
            return 'Business'
            
    except Exception as e:
        print(f"Error during categorization: {e}")
        return "Uncategorized"
