"""Researcher agent implementation."""
 
from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.observability.tracing import trace_agent
 
 
class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""
 
    name = "researcher"
 
    @trace_agent
    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`.
 
        Implement search, source filtering, citation capture, and notes.
        """
        # Initialize search client
        search_client = SearchClient()
         
        # Perform search based on the research query
        sources = search_client.search(state.request.query, num_results=3)
         
        # Store sources in state
        state.sources = sources
         
        # Generate research notes using LLM
        system_prompt = (
            "You are a research assistant specialized in summarizing academic and technical "
            "content. Please provide a comprehensive summary of the key points from the "
            "sources provided."
        )
        user_prompt = (
            f"Based on the provided sources, please create comprehensive research notes "
            f"addressing: {state.request.query}\n\nSources:\n{sources}"
        )
         
        # Get LLM response
        try:
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.research_notes = response.content
        except Exception as e:
            state.errors.append(f"Researcher agent failed: {str(e)}")
            state.research_notes = "Failed to generate research notes due to an error."
             
        return state
