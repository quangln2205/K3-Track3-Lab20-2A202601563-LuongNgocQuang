#!/usr/bin/env python3
"""Test script to verify the multi-agent system works."""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.graph.workflow_mock import MultiAgentWorkflowMock

def test_multi_agent_workflow():
    """Test the multi-agent workflow with a sample query."""
    
    # Create a test query
    query = "Research GraphRAG state-of-the-art and write a 500-word summary"
    research_query = ResearchQuery(query=query)
    
    # Create initial state
    state = ResearchState(request=research_query)
    
    # Create workflow
    workflow = MultiAgentWorkflowMock()
    
    # Run the workflow
    print("Starting multi-agent research workflow...")
    final_state = workflow.run(state)
    
    # Print results
    print("\n=== WORKFLOW RESULTS ===")
    print(f"Iterations: {final_state.iteration}")
    print(f"Route history: {final_state.route_history}")
    print(f"Research notes length: {len(final_state.research_notes) if final_state.research_notes else 0}")
    print(f"Analysis notes length: {len(final_state.analysis_notes) if final_state.analysis_notes else 0}")
    print(f"Final answer length: {len(final_state.final_answer) if final_state.final_answer else 0}")
    print(f"Errors: {final_state.errors}")
    
    if final_state.final_answer:
        print("\n=== FINAL ANSWER ===")
        print(final_state.final_answer[:500] + "..." if len(final_state.final_answer) > 500 else final_state.final_answer)
    
    return final_state

if __name__ == "__main__":
    try:
        test_multi_agent_workflow()
        print("\n✅ Multi-agent workflow test completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()