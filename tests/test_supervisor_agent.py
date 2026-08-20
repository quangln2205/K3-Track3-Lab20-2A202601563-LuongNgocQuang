"""Unit tests for SupervisorAgent implementation."""

import pytest
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState


def test_supervisor_initial_state() -> None:
    """Test that supervisor correctly routes to researcher on initial state."""
    state = ResearchState(request=ResearchQuery(query="Test query"))
    supervisor = SupervisorAgent()
    
    # Should route to researcher when no route history exists
    result = supervisor.run(state)
    
    assert len(state.route_history) == 1
    assert state.route_history[0] == "researcher"
    assert state.iteration == 1


def test_supervisor_researcher_to_analyst() -> None:
    """Test that supervisor correctly routes from researcher to analyst."""
    state = ResearchState(request=ResearchQuery(query="Test query"))
    state.record_route("researcher")
    # Simulate research completion
    state.sources = ["source1", "source2"]
    state.research_notes = "Some research notes"
    
    supervisor = SupervisorAgent()
    result = supervisor.run(state)
    
    assert len(state.route_history) == 2
    assert state.route_history[1] == "analyst"
    assert state.iteration == 2


def test_supervisor_analyst_to_writer() -> None:
    """Test that supervisor correctly routes from analyst to writer."""
    state = ResearchState(request=ResearchQuery(query="Test query"))
    state.record_route("analyst")
    # Simulate analysis completion
    state.analysis_notes = "Some analysis notes"
    
    supervisor = SupervisorAgent()
    result = supervisor.run(state)
    
    assert len(state.route_history) == 2
    assert state.route_history[1] == "writer"
    assert state.iteration == 2


def test_supervisor_writer_to_done() -> None:
    """Test that supervisor correctly routes from writer to done."""
    state = ResearchState(request=ResearchQuery(query="Test query"))
    state.record_route("writer")
    # Simulate final answer completion
    state.final_answer = "Final answer"
    
    supervisor = SupervisorAgent()
    result = supervisor.run(state)
    
    assert len(state.route_history) == 2
    assert state.route_history[1] == "done"
    assert state.iteration == 2


def test_supervisor_max_iterations() -> None:
    """Test that supervisor enforces maximum iterations."""
    state = ResearchState(request=ResearchQuery(query="Test query"))
    # Set high iteration count to trigger max iterations
    state.iteration = 10
    
    supervisor = SupervisorAgent()
    result = supervisor.run(state)
    
    assert len(state.route_history) == 1
    assert state.route_history[0] == "done"
    assert state.iteration == 11


def test_supervisor_unknown_route() -> None:
    """Test that supervisor handles unknown routes gracefully."""
    state = ResearchState(request=ResearchQuery(query="Test query"))
    state.record_route("unknown_route")
    
    supervisor = SupervisorAgent()
    result = supervisor.run(state)
    
    # Should default to researcher for unknown routes
    assert len(state.route_history) == 2
    assert state.route_history[1] == "researcher"
    assert state.iteration == 2