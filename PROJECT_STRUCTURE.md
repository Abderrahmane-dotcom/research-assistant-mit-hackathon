# 📁 Project Structure Overview

## Complete File Tree

```
mit_hackathon/
│
├── 📄 main.py                      # Main entry point for the application
├── 📄 examples.py                  # Example usage demonstrations
│
├── 📄 README.md                    # Main project documentation
├── 📄 API.md                       # API documentation
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 requirements.txt             # Python dependencies
│
├── 📁 src/                         # Main source code directory
│   ├── 📄 __init__.py             # Package initialization
│   ├── 📄 config.py               # Configuration settings
│   ├── 📄 research_system.py     # Main research orchestrator
│   │
│   ├── 📁 agents/                 # Multi-agent system
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base_agent.py      # Abstract base agent class
│   │   ├── 📄 researcher_agent.py # Research & information gathering
│   │   ├── 📄 reviewer_agent.py   # Critical analysis agents
│   │   ├── 📄 synthesizer_agent.py # Insight synthesis
│   │   └── 📄 state.py            # Shared state schema
│   │
│   ├── 📁 retrievers/             # Document retrieval
│   │   ├── 📄 __init__.py
│   │   ├── 📄 bm25_retriever.py   # BM25 search algorithm
│   │   └── 📄 document_loader.py  # PDF loading & chunking
│   │
│   ├── 📁 scrapers/               # Web scraping
│   │   ├── 📄 __init__.py
│   │   ├── 📄 wikipedia_scraper.py # Wikipedia API client
│   │   └── 📄 arxiv_scraper.py    # ArXiv paper scraper
│   │
│   └── 📁 utils/                  # Utility functions
│       ├── 📄 __init__.py
│       ├── 📄 tokenizer.py        # Text tokenization
│       └── 📄 text_utils.py       # Text processing helpers
│
├── 📁 files/                       # PDF documents for retrieval
│   └── (Place your PDF files here)
│
├── 📁 notebook/                    # Jupyter notebooks
│   ├── 📓 groq_agent.ipynb        # Agent design patterns
│   └── 📓 scraping_test.ipynb     # Scraper examples
│
├── 📁 myenv/                       # Virtual environment (created by setup)
│   ├── Scripts/                    # Windows executables
│   ├── bin/                        # Linux/Mac executables
│   └── Lib/                        # Python packages
│
└── 📁 hackathon - Copie/          # Legacy files (backup)
    └── (Old versions)
```

## 🗂️ Directory Descriptions

### Root Directory Files

| File | Purpose |
|------|---------|
| `main.py` | Interactive CLI for research queries |
| `examples.py` | Demonstration scripts for all features |
| `setup_check.py` | Validates installation and environment |
| `setup.bat` / `setup.sh` | Automated environment setup |
| `README.md` | Comprehensive project documentation |
| `QUICKSTART.md` | Fast-track setup instructions |
| `API.md` | Complete API reference |
| `CONTRIBUTING.md` | Guidelines for contributors |
| `LICENSE` | MIT License text |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Git exclusion patterns |

### src/ - Source Code

#### src/agents/ - Multi-Agent System

```
agents/
├── base_agent.py          # Abstract base for all agents
│   └── BaseAgent
│       └── process(state) -> Dict
│
├── researcher_agent.py    # Information gathering
│   └── ResearcherAgent(BaseAgent)
│       ├── __init__(llm, retriever, wikipedia_scraper)
│       └── process(state) -> summary, sources, snippets
│
├── reviewer_agent.py      # Critical analysis
│   ├── ReviewerAgent(BaseAgent)
│   ├── ReviewerAgentA     # Focus: support & logic
│   └── ReviewerAgentB     # Focus: gaps & biases
│
├── synthesizer_agent.py   # Insight generation
│   └── SynthesizerAgent(BaseAgent)
│       └── process(state) -> insight
│
└── state.py               # Shared state schema
    └── ResearchState (TypedDict)
```

#### src/retrievers/ - Document Retrieval

```
retrievers/
├── document_loader.py     # PDF processing
│   ├── DocChunk (dataclass)
│   └── DocumentLoader
│       └── load_and_chunk_pdfs() -> List[DocChunk]
│
└── bm25_retriever.py      # Search algorithm
    └── BM25Retriever
        └── get_relevant_documents(query, k) -> List[DocChunk]
```

#### src/scrapers/ - Web Scraping

```
scrapers/
├── wikipedia_scraper.py   # Wikipedia integration
│   └── WikipediaScraper
│       ├── search(query) -> List[Tuple[title, url]]
│       ├── scrape_article(url) -> Tuple[title, content]
│       └── scrape_by_keywords() -> List[Dict]
│
└── arxiv_scraper.py       # ArXiv integration
    └── ArxivScraper
        ├── scrape_articles(...) -> List[Dict]
        └── extract_pdf_content(pdf_data) -> str
```

#### src/utils/ - Utilities

```
utils/
├── tokenizer.py           # BM25 tokenization
│   └── simple_tokenize(text) -> List[str]
│
└── text_utils.py          # Text processing
    ├── truncate_text(text, max_length) -> str
    └── clean_query_for_wiki(query) -> str
```

#### Root Source Files

```
src/
├── config.py              # Global configuration
│   └── Config
│       ├── GROQ_API_KEY
│       ├── LLM_MODEL
│       ├── CHUNK_SIZE
│       └── ... (all settings)
│
└── research_system.py     # Main orchestrator
    └── ResearchSystem
        ├── initialize()
        ├── research(topic) -> ResearchState
        └── display_results(result)
```

## 🔄 Data Flow

```
User Input (topic)
        ↓
ResearchSystem.research()
        ↓
┌───────────────────────────┐
│   ResearcherAgent         │
│   - BM25 PDF Retrieval    │
│   - Wikipedia Scraping    │
└───────────┬───────────────┘
            ↓
    ┌──────────────┐
    │   Summary    │
    └──────┬───────┘
           ↓
    ┌──────────────┬──────────────┐
    │ ReviewerA    │ ReviewerB    │
    │ (Critique)   │ (Critique)   │
    └──────┬───────┴──────┬───────┘
           ↓              ↓
        ┌──────────────────────┐
        │   SynthesizerAgent   │
        │   (Collective        │
        │    Insight)          │
        └──────────┬───────────┘
                   ↓
            ResearchState
            (Final Output)
```

## 🎯 Entry Points

### For Users

```bash
# Interactive research
python main.py

# Example demonstrations
python examples.py

# Setup verification
python setup_check.py
```

### For Developers

```python
# Main system
from src.research_system import ResearchSystem

# Individual components
from src.agents import ResearcherAgent, ReviewerAgentA
from src.retrievers import BM25Retriever, DocumentLoader
from src.scrapers import WikipediaScraper, ArxivScraper

# Utilities
from src.utils import simple_tokenize, truncate_text
from src.config import Config
```

## 📊 File Statistics

| Category | Count | Description |
|----------|-------|-------------|
| **Python Modules** | 15 | Core source files |
| **Agents** | 5 | Multi-agent components |
| **Retrievers** | 2 | Document search |
| **Scrapers** | 2 | Web scraping |
| **Utilities** | 2 | Helper functions |
| **Entry Points** | 3 | User-facing scripts |
| **Documentation** | 5 | README, guides, API |
| **Setup Scripts** | 3 | Installation helpers |

## 🔑 Key Design Patterns

### 1. Strategy Pattern (Agents)
```
BaseAgent (abstract)
    ├── ResearcherAgent
    ├── ReviewerAgentA
    ├── ReviewerAgentB
    └── SynthesizerAgent
```

### 2. Builder Pattern (DocumentLoader)
```
DocumentLoader
    → load_pdfs()
    → chunk_documents()
    → build_metadata()
    → return List[DocChunk]
```

### 3. Facade Pattern (ResearchSystem)
```
ResearchSystem (facade)
    ├── Agents
    ├── Retrievers
    ├── Scrapers
    └── LangGraph workflow
```

### 4. Factory Pattern (Agent Creation)
```
ResearchSystem.initialize()
    → creates all agents
    → builds workflow graph
    → returns configured system
```

## 🛠️ Technology Stack

```
Backend Framework:
└── LangChain + LangGraph

Language Model:
└── GROQ (llama-3.3-70b-versatile)

Document Processing:
├── PyPDF / PyPDF2 (PDF parsing)
└── LangChain (text splitting)

Search & Retrieval:
└── BM25Okapi (lexical search)

Web Scraping:
├── BeautifulSoup4 (HTML parsing)
└── Requests (HTTP client)

Development:
├── Python 3.10+
└── Type Hints (typing module)
```

## 📦 Package Dependencies

See `requirements.txt` for versions:
- langchain
- langchain-community
- langchain-groq
- langchain-text-splitters
- langgraph
- rank-bm25
- requests
- beautifulsoup4
- pypdf
- lxml

## 🎨 Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Abstraction**: Base classes for extensibility
3. **Modularity**: Components can be used independently
4. **Type Safety**: Type hints throughout
5. **Documentation**: Docstrings for all public APIs
6. **Configuration**: Centralized in `config.py`
7. **Error Handling**: Graceful degradation
8. **Extensibility**: Easy to add new agents/scrapers

---

This structure provides a clean, maintainable, and extensible codebase for multi-agent research!
