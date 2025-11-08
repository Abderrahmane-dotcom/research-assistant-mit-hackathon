"""
Text processing utilities
"""

import re
from typing import List


def truncate_text(text: str, max_length: int = 800) -> str:
    """
    Truncate text to a maximum length, breaking at word boundaries.
    
    Args:
        text: Text to truncate
        max_length: Maximum length in characters
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length].rsplit(" ", 1)[0]
    return truncated + " ..."


def clean_query_for_wiki(query: str) -> str:
    """
    Simplify query to keywords for Wikipedia search by removing
    stopwords and punctuation.
    
    Args:
        query: Original search query
        
    Returns:
        Cleaned query string
    """
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query)  # remove punctuation
    
    stopwords = [
        'what', 'about', 'how', 'is', 'in', 'the', 
        'a', 'an', 'for', 'on', 'of', 'and'
    ]
    
    tokens = [t for t in query.split() if t not in stopwords]
    return " ".join(tokens)
