"""
Main research system orchestrating multi-agent workflow
"""

from typing import Optional
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph

from .config import Config
from .agents import (
    ResearchState,
    ResearcherAgent,
    ReviewerAgentA,
    ReviewerAgentB,
    SynthesizerAgent
)
from .retrievers import BM25Retriever, DocumentLoader
from .scrapers import WikipediaScraper, ArxivScraper


class ResearchSystem:
    """Main research system coordinating agents and retrievers"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        files_dir: Optional[str] = None,
        use_wikipedia: bool = True,
        use_arxiv: bool = True,
        max_wikipedia_articles: int = 3,
        max_arxiv_papers: int = 3
    ):
        """
        Initialize research system.
        
        Args:
            api_key: GROQ API key (uses Config default if not provided)
            files_dir: Directory containing PDF files (uses Config default if not provided)
            use_wikipedia: Whether to use Wikipedia scraper
            use_arxiv: Whether to use ArXiv scraper
            max_wikipedia_articles: Maximum Wikipedia articles to retrieve
            max_arxiv_papers: Maximum ArXiv papers to retrieve
        """
        # Set API key
        if api_key:
            Config.set_groq_api_key(api_key)
        
        # Initialize LLM
        self.llm = ChatGroq(
            model=Config.LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE
        )
        
        # Set files directory
        self.files_dir = files_dir or str(Config.FILES_DIR)
        
        # Initialize components
        self.retriever: Optional[BM25Retriever] = None
        
        # Initialize scrapers based on configuration
        self.use_wikipedia = use_wikipedia
        self.use_arxiv = use_arxiv
        self.max_wikipedia_articles = max_wikipedia_articles
        self.max_arxiv_papers = max_arxiv_papers
        
        self.wikipedia_scraper = WikipediaScraper() if use_wikipedia else None
        self.arxiv_scraper = ArxivScraper() if use_arxiv else None
        
        # Initialize agents
        self.researcher: Optional[ResearcherAgent] = None
        self.reviewer_a: Optional[ReviewerAgentA] = None
        self.reviewer_b: Optional[ReviewerAgentB] = None
        self.synthesizer: Optional[SynthesizerAgent] = None
        
        # Workflow graph
        self.app = None
    
    def initialize(self):
        """Initialize the research system by loading documents and building index"""
        print("📥 Ingesting PDFs and building BM25 index...")
        
        # Load and index documents
        doc_loader = DocumentLoader()
        chunks = doc_loader.load_and_chunk_pdfs(self.files_dir)
        
        if chunks:
            self.retriever = BM25Retriever(chunks)
            print("✅ BM25 index ready.")
        else:
            print("⚠️  BM25 retriever not created (no chunks).")
        
        # Display scraper configuration
        scrapers_enabled = []
        if self.use_wikipedia:
            scrapers_enabled.append(f"Wikipedia (max {self.max_wikipedia_articles} articles)")
        if self.use_arxiv:
            scrapers_enabled.append(f"ArXiv (max {self.max_arxiv_papers} papers)")
        
        if scrapers_enabled:
            print(f"🌐 Scrapers enabled: {', '.join(scrapers_enabled)}")
        else:
            print("⚠️  No web scrapers enabled (only using local PDFs)")
        
        # Initialize agents
        self.researcher = ResearcherAgent(
            self.llm,
            self.retriever,
            self.wikipedia_scraper,
            self.arxiv_scraper,
            max_wikipedia_articles=self.max_wikipedia_articles,
            max_arxiv_papers=self.max_arxiv_papers
        )
        self.reviewer_a = ReviewerAgentA(self.llm)
        self.reviewer_b = ReviewerAgentB(self.llm)
        self.synthesizer = SynthesizerAgent(self.llm)
        
        # Build workflow graph
        self._build_graph()
        
        print("✅ Research system initialized!")
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        graph = StateGraph(ResearchState)
        
        # Add nodes
        graph.add_node("researcher", self.researcher.process)
        graph.add_node("reviewer_A", self.reviewer_a.process)
        graph.add_node("reviewer_B", self.reviewer_b.process)
        graph.add_node("synthesizer", self.synthesizer.process)
        
        # Add edges (debate pattern)
        graph.add_edge("researcher", "reviewer_A")
        graph.add_edge("researcher", "reviewer_B")
        graph.add_edge("reviewer_A", "synthesizer")
        graph.add_edge("reviewer_B", "synthesizer")
        
        # Set entry point
        graph.set_entry_point("researcher")
        
        # Compile graph
        self.app = graph.compile()
    
    def research(self, topic: str) -> ResearchState:
        """
        Run the research workflow on a topic.
        
        Args:
            topic: Research topic/query
            
        Returns:
            Final research state with all results
        """
        if not self.app:
            raise RuntimeError(
                "Research system not initialized. Call initialize() first."
            )
        
        print(f"\n🔬 Running debate pipeline for: {topic}")
        print("   Researcher → Reviewers → Synthesizer\n")
        
        result = self.app.invoke({"topic": topic})
        return result
    
    @staticmethod
    def print_divider():
        """Print a visual divider"""
        print("\n" + "=" * 80 + "\n")
    
    def display_results(self, result: ResearchState):
        """
        Display research results in a formatted way.
        
        Args:
            result: Research state with results
        """
        self.print_divider()
        print(f"📝 Topic: {result.get('topic', 'N/A')}\n")
        
        print("📘 Researcher Summary:\n")
        print(result.get("summary", "—"))
        
        self.print_divider()
        print("🔍 Reviewer A Critique:\n")
        print(result.get("critique_A", "—"))
        
        self.print_divider()
        print("🧐 Reviewer B Critique:\n")
        print(result.get("critique_B", "—"))
        
        self.print_divider()
        print("💡 Collective Insight:\n")
        print(result.get("insight", "—"))
        
        self.print_divider()
        sources = result.get("sources", [])
        print(f"📚 Sources used: {', '.join(sources) if sources else 'None'}")
        self.print_divider()
