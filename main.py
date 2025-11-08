#!/usr/bin/env python3
"""
Multi-Agent Research Assistant

A sophisticated research system that combines BM25 document retrieval,
Wikipedia scraping, and multi-agent debate for comprehensive topic analysis.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.research_system import ResearchSystem
from src.config import Config


def main():
    """Main entry point for the research assistant"""
    print("=" * 80)
    print("🤖 Multi-Agent Research Assistant")
    print("=" * 80)
    print("\nCombining BM25 retrieval + Wikipedia scraping + LangGraph agents")
    print("Debate Pattern: Researcher → Reviewer A & B → Synthesizer\n")
    
    # Ensure files directory exists
    Config.ensure_files_dir()
    
    # Initialize research system
    system = ResearchSystem()
    system.initialize()
    
    if not system.retriever:
        print("\n⚠️  Warning: No PDFs indexed.")
        print(f"   Add PDF files to '{Config.FILES_DIR}' for document retrieval.\n")
    
    # Interactive loop
    print("\n" + "=" * 80)
    print("Ready for research! Enter a topic to begin.")
    print("=" * 80)
    
    try:
        while True:
            topic = input("\n🔍 Enter a research topic (or 'exit' to quit): ").strip()
            
            if topic.lower() in ("exit", "quit", "q"):
                print("\n👋 Goodbye!")
                break
            
            if not topic:
                print("⚠️  Please enter a topic.")
                continue
            
            try:
                # Run research
                result = system.research(topic)
                
                # Display results
                system.display_results(result)
                
            except Exception as e:
                print(f"\n❌ Error during research: {e}")
                import traceback
                traceback.print_exc()
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
