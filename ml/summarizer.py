from ml.utils import get_summarizer

summarizer = None

def load_summarizer():
    """Loads the summarizer model into memory."""
    global summarizer
    if summarizer is None:
        summarizer = get_summarizer()

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using the pre-loaded model.
    
    Args:
        text (str): The text to summarize.
        
    Returns:
        str: The summarized text.
    """
    if summarizer is None:
        load_summarizer()
        
    # Ensure text is not too short
    if len(text.split()) < 50:
        return text

    try:
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summarization failed."
