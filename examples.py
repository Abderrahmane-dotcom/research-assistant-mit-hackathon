"""
Example usage of the Multi-Agent Research Assistant

This script demonstrates various ways to use the research system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.research_system import ResearchSystem
from src.config import Config
from src.scrapers import WikipediaScraper, ArxivScraper
from src.retrievers import DocumentLoader, BM25Retriever


def example_1_basic_research():
    """Example 1: Basic research workflow"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Research Workflow")
    print("=" * 80)
    
    # Initialize system
    system = ResearchSystem()
    system.initialize()
    
    # Research a topic
    topic = "renewable energy"
    result = system.research(topic)
    
    # Display results
    system.display_results(result)


def example_2_wikipedia_only():
    """Example 2: Wikipedia scraping only"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Wikipedia Scraping Only")
    print("=" * 80)
    
    scraper = WikipediaScraper()
    
    # Search and scrape articles
    articles = scraper.scrape_by_keywords("quantum computing", max_articles=2)
    
    # Display results
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}] {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Content preview: {article['content'][:300]}...")
        print("-" * 80)


def example_3_arxiv_scraping():
    """Example 3: ArXiv paper scraping"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: ArXiv Paper Scraping")
    print("=" * 80)
    
    scraper = ArxivScraper()
    
    # Scrape papers with content extraction
    papers = scraper.scrape_articles(
        query="machine learning climate",
        max_results=2,
        extract_content=True,
        save_pdf=False
    )
    
    # Display results
    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}] {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'][:3])}")
        print(f"Published: {paper['published']}")
        print(f"Abstract: {paper['abstract'][:200]}...")
        if paper['content']:
            print(f"Content length: {len(paper['content'])} characters")
        print("-" * 80)


def example_4_custom_retriever():
    """Example 4: Custom BM25 retriever usage"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Custom BM25 Retriever")
    print("=" * 80)
    
    # Load documents
    loader = DocumentLoader()
    chunks = loader.load_and_chunk_pdfs(str(Config.FILES_DIR))
    
    if not chunks:
        print("⚠️  No documents found. Add PDFs to 'files/' directory.")
        return
    
    # Create retriever
    retriever = BM25Retriever(chunks)
    
    # Search for documents
    query = "climate change"
    results = retriever.get_relevant_documents(query, k=3)
    
    print(f"\nTop 3 results for query: '{query}'")
    print("-" * 80)
    
    for i, doc in enumerate(results, 1):
        print(f"\n[{i}] Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Chunk ID: {doc.metadata.get('chunk_id', 'Unknown')}")
        print(f"Content preview: {doc.page_content[:200]}...")
        print("-" * 80)


def example_5_batch_research():
    """Example 5: Batch research on multiple topics"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Batch Research on Multiple Topics")
    print("=" * 80)
    
    # Initialize system once
    system = ResearchSystem()
    system.initialize()
    
    # Research multiple topics
    topics = [
        "artificial intelligence ethics",
        "renewable energy storage",
        "biodiversity conservation"
    ]
    
    results = []
    
    for topic in topics:
        print(f"\n🔬 Researching: {topic}")
        result = system.research(topic)
        results.append(result)
    
    # Display summary
    print("\n" + "=" * 80)
    print("BATCH RESEARCH SUMMARY")
    print("=" * 80)
    
    for i, (topic, result) in enumerate(zip(topics, results), 1):
        print(f"\n[{i}] {topic}")
        sources = result.get('sources', [])
        print(f"    Sources: {len(sources)}")
        print(f"    Summary: {result.get('summary', 'N/A')[:100]}...")


def main():
    """Run examples"""
    print("=" * 80)
    print("Multi-Agent Research Assistant - Examples")
    print("=" * 80)
    print("\nAvailable examples:")
    print("  1. Basic research workflow (full system)")
    print("  2. Wikipedia scraping only")
    print("  3. ArXiv paper scraping")
    print("  4. Custom BM25 retriever")
    print("  5. Batch research on multiple topics")
    print("  0. Run all examples")
    
    try:
        choice = input("\nSelect example (0-5): ").strip()
        
        examples = {
            '1': example_1_basic_research,
            '2': example_2_wikipedia_only,
            '3': example_3_arxiv_scraping,
            '4': example_4_custom_retriever,
            '5': example_5_batch_research,
        }
        
        if choice == '0':
            # Run all examples
            for func in examples.values():
                func()
        elif choice in examples:
            examples[choice]()
        else:
            print("Invalid choice!")
            return
        
        print("\n✅ Example completed!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
