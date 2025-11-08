"""
Researcher agent for information gathering and summarization
"""

from typing import Dict, Any, Optional
from langchain_groq import ChatGroq

from .base_agent import BaseAgent
from .state import ResearchState
from ..retrievers.bm25_retriever import BM25Retriever
from ..scrapers.wikipedia_scraper import WikipediaScraper
from ..utils.text_utils import truncate_text
from ..config import Config


class ResearcherAgent(BaseAgent):
    """Agent responsible for researching topics using multiple sources"""
    
    def __init__(
        self,
        llm: ChatGroq,
        retriever: Optional[BM25Retriever] = None,
        wikipedia_scraper: Optional[WikipediaScraper] = None
    ):
        """
        Initialize researcher agent.
        
        Args:
            llm: Language model instance
            retriever: BM25 retriever for PDF documents
            wikipedia_scraper: Wikipedia scraper instance
        """
        super().__init__(llm)
        self.retriever = retriever
        self.wikipedia_scraper = wikipedia_scraper or WikipediaScraper()
    
    def process(self, state: ResearchState) -> Dict[str, Any]:
        """
        Research a topic using BM25 retrieval and Wikipedia scraping.
        
        Args:
            state: Current research state
            
        Returns:
            Dictionary with summary, sources, and snippets
        """
        topic = state.get("topic", "").strip()
        
        if not topic:
            return {
                "summary": "No topic provided.",
                "topic": topic
            }
        
        context_pieces = []
        sources = []
        
        # BM25 PDF retrieval
        if self.retriever:
            docs = self.retriever.get_relevant_documents(
                topic,
                k=Config.BM25_TOP_K
            )
            
            for d in docs:
                snippet = truncate_text(
                    d.page_content.strip(),
                    Config.MAX_SNIPPET_LENGTH
                )
                source = d.metadata.get("source", "unknown")
                chunk_id = d.metadata.get("chunk_id", "")
                
                context_pieces.append(
                    f"[PDF SOURCE: {source} | CHUNK: {chunk_id}]\n{snippet}"
                )
                sources.append(source)
        
        # Wikipedia scraping
        wiki_articles = self.wikipedia_scraper.scrape_by_keywords(
            topic,
            max_articles=Config.WIKIPEDIA_MAX_ARTICLES
        )
        
        for art in wiki_articles:
            snippet = truncate_text(
                art['content'],
                Config.MAX_SNIPPET_LENGTH
            )
            context_pieces.append(
                f"[WIKI: {art['title']} | URL: {art['url']}]\n{snippet}"
            )
            sources.append(art['title'])
        
        if not context_pieces:
            return {
                "summary": "No relevant documents found.",
                "topic": topic
            }
        
        # Generate summary using LLM
        context = "\n\n---\n\n".join(context_pieces)
        prompt = (
            f"You are a research assistant. User asked about: '{topic}'.\n\n"
            f"Read the following retrieved excerpts (PDF + Wikipedia) and produce a concise summary "
            f"of the main findings. Include explicit sources/snippets for each claim.\n\n"
            f"EXCERPTS:\n\n{context}\n\n"
            "Return a short summary and a list of (source -> supporting snippet)."
        )
        
        summary_text = self.invoke_llm(prompt)
        
        return {
            "summary": summary_text,
            "sources": list(dict.fromkeys(sources)),
            "snippets": context_pieces,
            "topic": topic
        }
