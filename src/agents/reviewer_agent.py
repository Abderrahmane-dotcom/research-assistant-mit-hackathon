"""
Reviewer agents for critical analysis of research summaries
"""

from typing import Dict, Any
from langchain_groq import ChatGroq

from .base_agent import BaseAgent
from .state import ResearchState


class ReviewerAgent(BaseAgent):
    """Base class for reviewer agents"""
    
    def __init__(self, llm: ChatGroq, name: str, focus: str):
        """
        Initialize reviewer agent.
        
        Args:
            llm: Language model instance
            name: Reviewer name/identifier
            focus: Review focus description
        """
        super().__init__(llm)
        self.name = name
        self.focus = focus
    
    def process(self, state: ResearchState) -> Dict[str, Any]:
        """
        Review and critique a research summary.
        
        Args:
            state: Current research state
            
        Returns:
            Dictionary with critique
        """
        topic = state.get("topic", "")
        summary = state.get("summary", "")
        
        if not summary:
            return {f"critique_{self.name}": "No summary to review."}
        
        prompt = (
            f"You are Reviewer {self.name}. User asked about: '{topic}'. "
            f"Critically assess the summary.\n"
            f"{self.focus}\n\n"
            f"SUMMARY:\n\n{summary}\n\n"
            "Provide bullet points."
        )
        
        critique_text = self.invoke_llm(prompt)
        
        return {f"critique_{self.name}": critique_text}


class ReviewerAgentA(ReviewerAgent):
    """First reviewer focusing on support and logical issues"""
    
    def __init__(self, llm: ChatGroq):
        super().__init__(
            llm,
            name="A",
            focus="Focus on statements that lack support, missing considerations, or logical issues."
        )


class ReviewerAgentB(ReviewerAgent):
    """Second reviewer focusing on gaps and alternative interpretations"""
    
    def __init__(self, llm: ChatGroq):
        super().__init__(
            llm,
            name="B",
            focus="Focus on possible gaps, biases, or alternative interpretations."
        )
