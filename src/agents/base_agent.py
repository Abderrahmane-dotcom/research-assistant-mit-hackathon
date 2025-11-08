"""
Base agent class for all research agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain_groq import ChatGroq

from .state import ResearchState
from ..config import Config


class BaseAgent(ABC):
    """Abstract base class for research agents"""
    
    def __init__(self, llm: ChatGroq):
        """
        Initialize base agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
    
    @abstractmethod
    def process(self, state: ResearchState) -> Dict[str, Any]:
        """
        Process the research state and return updates.
        
        Args:
            state: Current research state
            
        Returns:
            Dictionary with state updates
        """
        pass
    
    def invoke_llm(self, prompt: str) -> str:
        """
        Invoke the language model with a prompt.
        
        Args:
            prompt: Prompt text
            
        Returns:
            Model response text
        """
        resp = self.llm.invoke(prompt)
        return getattr(resp, "content", None) or str(resp)
