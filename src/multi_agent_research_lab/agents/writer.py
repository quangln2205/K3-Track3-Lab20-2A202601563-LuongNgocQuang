"""Writer agent implementation."""
 
from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.observability.tracing import trace_agent
 
 
class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""
 
    name = "writer"
 
    @trace_agent
    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`.
 
        Synthesize a clear response with citations or source references.
        """
        if not state.research_notes or not state.analysis_notes:
            state.errors.append("Writer agent requires both research and analysis notes")
            return state
             
        # Write the final answer using LLM
        system_prompt = (
            "You are a technical writer specializing in creating clear, well-structured "
            "reports. Please create a comprehensive, well-organized final answer that "
            "synthesizes the research and analysis. Include proper structure with "
            "headings, bullet points, and clear explanations. Make sure to cite sources "
            "where appropriate."
        )
        user_prompt = (
            f"Write a comprehensive answer based on the research and analysis provided: "
            f"{state.research_notes} and {state.analysis_notes}\n\n"
            f"Please structure your response with clear headings and subheadings, "
            f"and provide a well-supported conclusion."
        )
         
        # Get LLM response
        try:
            response = self.llm_client.complete(system_prompt, user_prompt)
            state.final_answer = response.content
        except Exception as e:
            state.errors.append(f"Writer agent failed: {str(e)}")
            state.final_answer = "Failed to generate final answer due to an error."
             
        return state
