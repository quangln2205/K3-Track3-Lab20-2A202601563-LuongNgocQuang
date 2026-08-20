"""Tracing integration for the multi-agent system."""

import os
from typing import Optional
from langsmith import traceable
from langsmith.client import Client


class TracingManager:
    """Manages tracing integration for the multi-agent system."""
    
    def __init__(self):
        # Check if LangSmith is enabled
        self.langsmith_enabled = bool(os.getenv("LANGSMITH_API_KEY"))
        self.client = Client() if self.langsmith_enabled else None
        
    def is_tracing_enabled(self) -> bool:
        """Check if tracing is enabled."""
        return self.langsmith_enabled
    
    def get_trace_url(self, run_id: str) -> Optional[str]:
        """Get the URL for a specific trace."""
        if not self.langsmith_enabled:
            return None
        try:
            return f"https://smith.langchain.com/public/{run_id}/f"
        except Exception:
            return None


def setup_tracing():
    """Setup tracing for the multi-agent system."""
    return TracingManager()


# Decorator for tracing agent functions
def trace_agent(func):
    """Decorator to add tracing to agent functions."""
    if os.getenv("LANGSMITH_API_KEY"):
        return traceable(name=func.__name__)
    return func