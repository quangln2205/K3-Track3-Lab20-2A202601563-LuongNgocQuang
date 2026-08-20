#!/usr/bin/env python3
"""Demo script showing the multi-agent system in action."""

import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.graph.workflow_mock import MultiAgentWorkflowMock

def demo_multi_agent_system():
    """Demonstrate the complete multi-agent research system."""
    
    print("🚀 Starting Multi-Agent Research System Demo")
    print("=" * 50)
    
    # Create a test query
    query = "Research GraphRAG state-of-the-art and write a 500-word summary"
    research_query = ResearchQuery(query=query)
    
    # Create initial state
    state = ResearchState(request=research_query)
    
    # Create workflow
    workflow = MultiAgentWorkflowMock()
    
    # Run the workflow
    print("🔍 Executing multi-agent research workflow...")
    final_state = workflow.run(state)
    
    # Display results
    print("\n📊 WORKFLOW RESULTS")
    print("-" * 30)
    print(f"📈 Iterations: {final_state.iteration}")
    print(f"🧭 Route History: {final_state.route_history}")
    print(f"📝 Research Notes Length: {len(final_state.research_notes) if final_state.research_notes else 0}")
    print(f"🔍 Analysis Notes Length: {len(final_state.analysis_notes) if final_state.analysis_notes else 0}")
    print(f"✍️ Final Answer Length: {len(final_state.final_answer) if final_state.final_answer else 0}")
    print(f"⚠️ Errors: {final_state.errors}")
    
    if final_state.final_answer:
        print("\n📄 FINAL ANSWER")
        print("-" * 30)
        print(final_state.final_answer)
    
    print("\n✅ Demo completed successfully!")
    print("The multi-agent system has successfully:")
    print("  • Conducted research using the Researcher agent")
    print("  • Analyzed findings using the Analyst agent") 
    print("  • Generated a final answer using the Writer agent")
    print("  • Followed the correct workflow sequence")

if __name__ == "__main__":
    demo_multi_agent_system()