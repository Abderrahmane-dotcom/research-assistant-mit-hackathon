"""
Tokenization utilities for BM25 indexing
"""

import re
from typing import List


def simple_tokenize(text: str) -> List[str]:
    """
    Simple tokenizer for BM25 indexing.
    
    Args:
        text: Input text to tokenize
        
    Returns:
        List of lowercase tokens (words with length > 1)
    """
    tokens = re.findall(r"\w+", text.lower())
    return [t for t in tokens if len(t) > 1]
