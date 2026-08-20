"""LangGraph workflow with mock client for testing."""

from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.mock_llm_client import MockLLMClient


class MultiAgentWorkflowMock:
    """Builds and runs the multi-agent graph with mock client.
    
    This version uses mock LLM client for testing without external API dependencies.
    """

    def __init__(self):
        self.llm_client = MockLLMClient()
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
        """Create a LangGraph graph.
        
        Implement nodes, edges, conditional routing, and stop condition.
        Suggested nodes: supervisor, researcher, analyst, writer, optional critic.
        """
        # This is a simplified representation of what a LangGraph workflow would look like
        # In a real implementation, this would use LangGraph library
        return self

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state.
        
        Compile graph, invoke it, and convert result back to ResearchState.
        """
        # Simple sequential execution for demonstration
        # In a real implementation, this would use LangGraph to handle the workflow
        max_iterations = 10
        iteration = 0

        # Initialize with a default route if none exists
        if not state.route_history:
            state.record_route("supervisor")

        while iteration < max_iterations and (
            not state.route_history or state.route_history[-1] != "done"
        ):
            # Run supervisor to determine next step
            state = self.supervisor.run(state)

            # Execute the appropriate agent based on the route
            if state.route_history[-1] == "researcher":
                state = self.researcher.run(state)
            elif state.route_history[-1] == "analyst":
                state = self.analyst.run(state)
            elif state.route_history[-1] == "writer":
                state = self.writer.run(state)
            elif state.route_history[-1] == "done":
                break

            iteration += 1

        return state