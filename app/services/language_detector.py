from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """
    Detect if text is in English or Hindi.
    Returns 'en' or 'hi'.
    """
    try:
        lang = detect(text)
        # Map common Indian language codes to 'hi'
        if lang in ['hi', 'mr', 'bn', 'ta', 'te', 'gu']:
            return 'hi'
        return 'en'
    except LangDetectException:
        # Default to English if detection fails
        return 'en'