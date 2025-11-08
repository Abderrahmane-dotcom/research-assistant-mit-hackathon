"""
BM25-based document retriever
"""

from typing import List
from rank_bm25 import BM25Okapi

from .document_loader import DocChunk
from ..utils.tokenizer import simple_tokenize


class BM25Retriever:
    """BM25-based retriever for semantic document search"""
    
    def __init__(self, chunks: List[DocChunk]):
        """
        Initialize BM25 retriever with document chunks.
        
        Args:
            chunks: List of document chunks to index
        """
        self.chunks = chunks
        self.tokenized_texts = [
            simple_tokenize(c.page_content) for c in chunks
        ]
        self.bm25 = BM25Okapi(self.tokenized_texts)
    
    def get_relevant_documents(self, query: str, k: int = 3) -> List[DocChunk]:
        """
        Retrieve the most relevant documents for a query.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of most relevant document chunks
        """
        q_tokens = simple_tokenize(query)
        
        if not q_tokens:
            return []
        
        scores = self.bm25.get_scores(q_tokens)
        idx_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        
        # Get top-k indices with positive scores
        top = [i for i, sc in idx_scores[:k] if sc > 0]
        
        # If no positive scores, get top-k anyway
        if not top and len(idx_scores) > 0:
            top = [i for i, _ in idx_scores[:k]]
        
        return [self.chunks[i] for i in top]
