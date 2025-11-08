"""
Synthesizer agent for combining research and critiques
"""

from typing import Dict, Any
from langchain_groq import ChatGroq

from .base_agent import BaseAgent
from .state import ResearchState


class SynthesizerAgent(BaseAgent):
    """Agent responsible for synthesizing research and critiques into insights"""
    
    def __init__(self, llm: ChatGroq):
        """
        Initialize synthesizer agent.
        
        Args:
            llm: Language model instance
        """
        super().__init__(llm)
    
    def process(self, state: ResearchState) -> Dict[str, Any]:
        """
        Synthesize summary and critiques into a collective insight.
        
        Args:
            state: Current research state
            
        Returns:
            Dictionary with collective insight
        """
        topic = state.get("topic", "")
        summary = state.get("summary", "")
        critique_A = state.get("critique_A", "")
        critique_B = state.get("critique_B", "")
        sources = state.get("sources", [])
        
        prompt = (
            f"You are a synthesizer. User asked about: '{topic}'.\n"
            "Combine the summary and two independent critiques into a 'Collective Insight Report'. Include:\n"
            "- 2-3 sentence actionable insight\n"
            "- 2 testable hypotheses or follow-up experiments\n"
            "- References to relevant sources or snippets supporting each hypothesis\n\n"
            f"SUMMARY:\n{summary}\n\n"
            f"CRITIQUE A:\n{critique_A}\n\n"
            f"CRITIQUE B:\n{critique_B}\n\n"
            f"SOURCES:\n{', '.join(sources)}"
        )
        
        insight_text = self.invoke_llm(prompt)
        
        return {"insight": insight_text}
