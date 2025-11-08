# Source Code Directory (`src/`)

This directory contains the core implementation of the Multi-Agent Research Assistant.

## Directory Structure

```
src/
├── __init__.py              # Package initialization
├── config.py                # Global configuration
├── research_system.py       # Main orchestrator
│
├── agents/                  # Multi-agent system
│   ├── __init__.py
│   ├── base_agent.py       # Abstract base class
│   ├── researcher_agent.py # Information gathering
│   ├── reviewer_agent.py   # Critical analysis
│   ├── synthesizer_agent.py # Insight synthesis
│   └── state.py            # State schema
│
├── retrievers/             # Document search
│   ├── __init__.py
│   ├── bm25_retriever.py   # BM25 algorithm
│   └── document_loader.py  # PDF processing
│
├── scrapers/               # Web scraping
│   ├── __init__.py
│   ├── wikipedia_scraper.py # Wikipedia integration
│   └── arxiv_scraper.py    # ArXiv integration
│
└── utils/                  # Helper functions
    ├── __init__.py
    ├── tokenizer.py        # Text tokenization
    └── text_utils.py       # Text processing
```

## Module Overview

### Core Modules

**`config.py`**
- Global configuration settings
- API keys and model settings
- Directory paths
- Processing parameters

**`research_system.py`**
- Main `ResearchSystem` class
- Orchestrates all components
- Manages workflow
- Provides high-level API

### Agents Package

**Purpose:** Multi-agent debate and research workflow

**`base_agent.py`**
- Abstract base class for all agents
- Common interface and utilities
- LLM invocation wrapper

**`researcher_agent.py`**
- Gathers information from multiple sources
- Combines BM25 retrieval with Wikipedia
- Generates comprehensive summaries

**`reviewer_agent.py`**
- Two independent reviewers (A & B)
- Critical analysis of summaries
- Different perspectives

**`synthesizer_agent.py`**
- Combines all perspectives
- Generates actionable insights
- Creates testable hypotheses

**`state.py`**
- TypedDict for workflow state
- Ensures type safety across agents

### Retrievers Package

**Purpose:** Document search and retrieval

**`document_loader.py`**
- Loads PDF documents
- Chunks text for processing
- Manages metadata

**`bm25_retriever.py`**
- Implements BM25 ranking
- Fast lexical search
- Relevance scoring

### Scrapers Package

**Purpose:** External data sources

**`wikipedia_scraper.py`**
- Wikipedia API integration
- Article search and retrieval
- Content extraction

**`arxiv_scraper.py`**
- ArXiv paper scraping
- PDF download and extraction
- Metadata parsing

### Utils Package

**Purpose:** Helper functions

**`tokenizer.py`**
- Text tokenization for BM25
- Simple but effective

**`text_utils.py`**
- Text truncation
- Query cleaning
- String processing

## Usage

### Import from src

```python
# Main system
from src.research_system import ResearchSystem

# Agents
from src.agents import (
    ResearcherAgent,
    ReviewerAgentA,
    ReviewerAgentB,
    SynthesizerAgent
)

# Retrievers
from src.retrievers import BM25Retriever, DocumentLoader

# Scrapers
from src.scrapers import WikipediaScraper, ArxivScraper

# Utilities
from src.utils import simple_tokenize, truncate_text

# Configuration
from src.config import Config
```

### Example

```python
from src.research_system import ResearchSystem

# Initialize
system = ResearchSystem()
system.initialize()

# Research
result = system.research("artificial intelligence")

# Display
system.display_results(result)
```

## Design Principles

1. **Modularity:** Each module has a single responsibility
2. **Abstraction:** Base classes for extensibility
3. **Type Safety:** Type hints throughout
4. **Documentation:** Comprehensive docstrings
5. **Testability:** Functions are pure where possible
6. **Configuration:** Centralized in `config.py`

## Adding New Components

### New Agent

1. Create file in `agents/`
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Add to `agents/__init__.py`

### New Retriever

1. Create file in `retrievers/`
2. Implement search interface
3. Add to `retrievers/__init__.py`

### New Scraper

1. Create file in `scrapers/`
2. Implement scraping methods
3. Add to `scrapers/__init__.py`

## Dependencies

See `../requirements.txt` for complete list:
- langchain
- langchain-community
- langchain-groq
- langgraph
- rank-bm25
- beautifulsoup4
- requests
- pypdf

## Testing

```python
# Test individual components
from src.retrievers import DocumentLoader

loader = DocumentLoader()
chunks = loader.load_and_chunk_pdfs("../files")
print(f"Loaded {len(chunks)} chunks")
```

## More Information

- See [API Documentation](../API.md) for detailed API reference
- See [Architecture](../ARCHITECTURE.md) for system diagrams
- See [Contributing](../CONTRIBUTING.md) for development guidelines
