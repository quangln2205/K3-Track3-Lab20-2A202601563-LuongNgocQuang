"""Supervisor / router implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.observability.tracing import trace_agent


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    @trace_agent
    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route.

        Implements routing policy for the multi-agent workflow.
        - Start with researcher if no research has been done
        - Then analyst if research is complete
        - Then writer if analysis is complete
        - Finally done when final answer is produced
        - Enforce max iterations and failure fallback.
        """
        # Check for maximum iterations to prevent infinite loops
        if state.iteration >= 10:
            # Even though we're done, we still need to increment the iteration
            # to match the expected behavior in tests
            state.record_route("done")
            return state
            
        # Check if we're starting the workflow
        if not state.route_history:
            state.record_route("researcher")
            return state
            
        # Determine next step based on current state
        last_route = state.route_history[-1]
        
        if last_route == "researcher":
            # If research is complete (sources and research notes exist), move to analyst
            if state.sources and state.research_notes:
                state.record_route("analyst")
            else:
                # If research failed or didn't complete, try again or move to done
                state.record_route("researcher")
                
        elif last_route == "analyst":
            # If analysis is complete (analysis notes exist), move to writer
            if state.analysis_notes:
                state.record_route("writer")
            else:
                # If analysis failed, try again or move to done
                state.record_route("analyst")
                
        elif last_route == "writer":
            # If final answer is produced, we're done
            if state.final_answer:
                state.record_route("done")
            else:
                # If writing failed, try again or move to done
                state.record_route("writer")
                
        else:
            # Default case - move to researcher if unknown state
            state.record_route("researcher")
            
        return state
