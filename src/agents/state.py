"""
State definition for the research workflow
"""

from typing import TypedDict, Optional, List


class ResearchState(TypedDict):
    """Shared state for the multi-agent research system"""
    topic: str
    summary: Optional[str]
    critique_A: Optional[str]
    critique_B: Optional[str]
    insight: Optional[str]
    sources: Optional[List[str]]
    snippets: Optional[List[str]]
