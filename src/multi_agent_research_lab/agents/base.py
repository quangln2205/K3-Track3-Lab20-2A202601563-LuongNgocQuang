"""Base agent class."""

from abc import ABC, abstractmethod
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.observability.tracing import trace_agent


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    name: str
    llm_client: LLMClient

    @abstractmethod
    def run(self, state: ResearchState) -> ResearchState:
        """Execute the agent's logic and return updated state."""
        pass
        
    def __post_init__(self):
        """Initialize agent with tracing support."""
        pass