"""LangGraph workflow implementation."""

from typing import Literal, TypedDict
from langgraph.graph import StateGraph, END
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.observability.tracing import setup_tracing


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph using LangGraph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def __init__(self):
        self.llm_client = LLMClient()
        self.supervisor = SupervisorAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()

        # Inject LLM client into agents
        self.supervisor.llm_client = self.llm_client
        self.researcher.llm_client = self.llm_client
        self.analyst.llm_client = self.llm_client
        self.writer.llm_client = self.llm_client

    def build(self) -> object:
        """Create a LangGraph graph with proper nodes and edges."""
        # Create the graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("analyst", self._analyst_node)
        workflow.add_node("writer", self._writer_node)
        
        # Add edges
        workflow.set_entry_point("supervisor")
        workflow.add_edge("supervisor", "researcher")
        workflow.add_edge("researcher", "analyst")
        workflow.add_edge("analyst", "writer")
        workflow.add_edge("writer", END)
        
        # Compile the graph
        return workflow.compile()

    def _supervisor_node(self, state: ResearchState) -> ResearchState:
        """Supervisor node that determines the next step."""
        return self.supervisor.run(state)

    def _researcher_node(self, state: ResearchState) -> ResearchState:
        """Researcher node that performs research."""
        return self.researcher.run(state)

    def _analyst_node(self, state: ResearchState) -> ResearchState:
        """Analyst node that analyzes findings."""
        return self.analyst.run(state)

    def _writer_node(self, state: ResearchState) -> ResearchState:
        """Writer node that produces final answer."""
        return self.writer.run(state)

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        # Build the graph
        graph = self.build()
        
        # Run the graph
        result = graph.invoke(state)
        return result
