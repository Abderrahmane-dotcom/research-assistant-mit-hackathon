# API Documentation

## Core Classes

### ResearchSystem

Main orchestrator for the multi-agent research system.

```python
from src.research_system import ResearchSystem

system = ResearchSystem(api_key=None, files_dir=None)
system.initialize()
result = system.research(topic="your topic")
system.display_results(result)
```

**Methods:**
- `initialize()`: Load documents and build BM25 index
- `research(topic: str) -> ResearchState`: Run research pipeline
- `display_results(result: ResearchState)`: Pretty print results

---

### Agents

#### BaseAgent

Abstract base class for all agents.

```python
from src.agents import BaseAgent

class CustomAgent(BaseAgent):
    def process(self, state: ResearchState) -> Dict[str, Any]:
        # Implementation
        return {"key": "value"}
```

#### ResearcherAgent

Gathers information from PDF documents and Wikipedia.

```python
from src.agents import ResearcherAgent
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
agent = ResearcherAgent(llm, retriever=None, wikipedia_scraper=None)
result = agent.process(state)
```

#### ReviewerAgentA / ReviewerAgentB

Critical analysis of research summaries.

```python
from src.agents import ReviewerAgentA, ReviewerAgentB

reviewer_a = ReviewerAgentA(llm)
reviewer_b = ReviewerAgentB(llm)

critique_a = reviewer_a.process(state)
critique_b = reviewer_b.process(state)
```

#### SynthesizerAgent

Combines research and critiques into insights.

```python
from src.agents import SynthesizerAgent

synthesizer = SynthesizerAgent(llm)
insight = synthesizer.process(state)
```

---

### Retrievers

#### DocumentLoader

Loads and chunks PDF documents.

```python
from src.retrievers import DocumentLoader

loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)
chunks = loader.load_and_chunk_pdfs("files/")
```

**Methods:**
- `load_and_chunk_pdfs(files_dir: str) -> List[DocChunk]`

#### BM25Retriever

BM25-based document retrieval.

```python
from src.retrievers import BM25Retriever

retriever = BM25Retriever(chunks)
docs = retriever.get_relevant_documents(query="AI", k=5)
```

**Methods:**
- `get_relevant_documents(query: str, k: int = 3) -> List[DocChunk]`

---

### Scrapers

#### WikipediaScraper

Scrapes Wikipedia articles.

```python
from src.scrapers import WikipediaScraper

scraper = WikipediaScraper(user_agent="CustomBot/1.0")

# Search
results = scraper.search("quantum computing", limit=10)

# Scrape single article
title, content = scraper.scrape_article(url)

# Scrape by keywords
articles = scraper.scrape_by_keywords("AI", max_articles=5)
```

**Methods:**
- `search(query: str, limit: int = 10) -> List[Tuple[str, str]]`
- `scrape_article(url: str) -> Optional[Tuple[str, str]]`
- `scrape_by_keywords(keywords: str, max_articles: int = 5) -> List[Dict]`

**Returns:**
```python
{
    'title': str,
    'content': str,
    'url': str
}
```

#### ArxivScraper

Scrapes ArXiv academic papers with PDF extraction.

```python
from src.scrapers import ArxivScraper

scraper = ArxivScraper()

papers = scraper.scrape_articles(
    query="machine learning",
    max_results=10,
    save_pdf=False,
    extract_content=True,
    output_folder="pdfs",
    start_date="2024-01-01",
    end_date="2024-12-31",
    sort_by="relevance"  # or "updated", "submitted"
)
```

**Methods:**
- `scrape_articles(...) -> List[Dict]`
- `extract_pdf_content(pdf_data: bytes) -> str` (static method)

**Returns:**
```python
{
    'title': str,
    'abstract': str,
    'authors': List[str],
    'pdf_url': str,
    'published': str,  # YYYY-MM-DD
    'arxiv_id': str,
    'content': Optional[str],  # Extracted PDF text
    'local_path': Optional[str]  # Path if saved
}
```

---

### Configuration

#### Config

Global configuration settings.

```python
from src.config import Config

# Access settings
files_dir = Config.FILES_DIR
api_key = Config.GROQ_API_KEY
chunk_size = Config.CHUNK_SIZE

# Modify settings
Config.set_groq_api_key("new-key")
Config.ensure_files_dir()
```

**Attributes:**
- `PROJECT_ROOT`: Path to project root
- `FILES_DIR`: Path to PDF files directory
- `GROQ_API_KEY`: API key for GROQ
- `LLM_MODEL`: Model name
- `LLM_TEMPERATURE`: Temperature setting
- `CHUNK_SIZE`: Document chunk size
- `CHUNK_OVERLAP`: Chunk overlap size
- `BM25_TOP_K`: Number of BM25 results
- `WIKIPEDIA_MAX_ARTICLES`: Max Wikipedia articles
- `MAX_SNIPPET_LENGTH`: Max snippet length

---

### State

#### ResearchState

Shared state for agent workflow.

```python
from src.agents import ResearchState

state: ResearchState = {
    'topic': str,
    'summary': Optional[str],
    'critique_A': Optional[str],
    'critique_B': Optional[str],
    'insight': Optional[str],
    'sources': Optional[List[str]],
    'snippets': Optional[List[str]]
}
```

---

## Utilities

### Tokenizer

```python
from src.utils import simple_tokenize

tokens = simple_tokenize("Hello World!")
# Returns: ['hello', 'world']
```

### Text Utils

```python
from src.utils import truncate_text, clean_query_for_wiki

# Truncate text
short = truncate_text("Long text...", max_length=100)

# Clean query for Wikipedia
clean = clean_query_for_wiki("What is artificial intelligence?")
# Returns: "artificial intelligence"
```

---

## Complete Example

```python
#!/usr/bin/env python3
from src.research_system import ResearchSystem
from src.config import Config

# Optional: Set custom API key
Config.set_groq_api_key("your-api-key")

# Initialize system
system = ResearchSystem()
system.initialize()

# Research a topic
result = system.research("renewable energy")

# Access results
topic = result['topic']
summary = result['summary']
critique_a = result['critique_A']
critique_b = result['critique_B']
insight = result['insight']
sources = result['sources']

# Display formatted output
system.display_results(result)
```

---

## Error Handling

```python
from src.research_system import ResearchSystem

system = ResearchSystem()

try:
    system.initialize()
    result = system.research("topic")
except RuntimeError as e:
    print(f"System error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Advanced Usage

### Custom Agent Integration

```python
from src.agents import BaseAgent, ResearchState
from src.research_system import ResearchSystem
from langgraph.graph import StateGraph

class CustomAnalyzer(BaseAgent):
    def process(self, state: ResearchState):
        # Custom logic
        return {"custom_field": "value"}

# Build custom graph
graph = StateGraph(ResearchState)
graph.add_node("analyzer", CustomAnalyzer(llm).process)
# ... add more nodes and edges
app = graph.compile()

result = app.invoke({"topic": "test"})
```

### Custom Retriever

```python
from src.retrievers import DocumentLoader
from src.utils import simple_tokenize
from rank_bm25 import BM25Okapi

class CustomRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        # Custom indexing logic
    
    def search(self, query: str, k: int = 5):
        # Custom search logic
        return results
```

---

## Type Hints

All modules use type hints for better IDE support:

```python
from typing import List, Dict, Optional, Tuple
from src.retrievers import DocChunk

def process_documents(chunks: List[DocChunk]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for chunk in chunks:
        content: str = chunk.page_content
        metadata: Dict[str, Any] = chunk.metadata
    return result
```

---

## Best Practices

1. **Always initialize before use**
   ```python
   system = ResearchSystem()
   system.initialize()  # Required!
   ```

2. **Check for None values**
   ```python
   if result.get('summary'):
       print(result['summary'])
   ```

3. **Use context managers for resources**
   ```python
   with open('file.pdf', 'rb') as f:
       content = f.read()
   ```

4. **Handle exceptions gracefully**
   ```python
   try:
       result = system.research(topic)
   except Exception as e:
       logger.error(f"Research failed: {e}")
   ```

---

## Performance Tips

1. **Limit document chunks**: Adjust `CHUNK_SIZE` in Config
2. **Reduce Wikipedia articles**: Lower `WIKIPEDIA_MAX_ARTICLES`
3. **Cache results**: Store frequent queries
4. **Batch processing**: Process multiple topics in one session

---

## Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use in your code
logger.info("Processing topic")
logger.warning("No documents found")
logger.error("Failed to connect")
```
