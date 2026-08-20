"""Analyst agent implementation."""
 
from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.observability.tracing import trace_agent
 
 
class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""
 
    name = "analyst"
 
    @trace_agent
    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`.
 
        Extract key claims, compare viewpoints, and flag weak evidence.
        """
        if not state.research_notes:
            state.errors.append("Analyst agent requires research notes to analyze")
            return state
             
        # Analyze the research notes using LLM
        system_prompt = (
            "You are a research analyst specializing in evaluating and synthesizing "
            "technical information. Please provide a structured analysis of the key "
            "findings, identify main claims, compare different viewpoints, and highlight "
            "any weaknesses in the evidence."
        )
        user_prompt = (
            f"Analyze the following research notes and provide structured insights: "
            f"{state.research_notes}\n\nPlease provide a comprehensive analysis with "
            f"clear headings and bullet points."
        )
         
        # Get LLM response
        try:
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.analysis_notes = response.content
        except Exception as e:
            state.errors.append(f"Analyst agent failed: {str(e)}")
            state.analysis_notes = "Failed to generate analysis due to an error."
             
        return state
