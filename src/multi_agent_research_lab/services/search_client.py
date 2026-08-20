"""Search client abstraction.

Production note: agents should depend on this interface instead of importing search SDKs directly.
"""

import random

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def __init__(self):
        # Mock implementation for demonstration purposes
        self.mock_sources = [
            {
                "url": "https://example.com/graphrag-intro",
                "title": "Introduction to GraphRAG",
                "content": (
                    "GraphRAG is a retrieval-augmented generation technique that uses graph "
                    "structures to enhance information retrieval and generation. It combines "
                    "traditional RAG with graph-based approaches to improve the quality and "
                    "relevance of generated responses."
                ),
            },
            {
                "url": "https://example.com/graphrag-techniques",
                "title": "Advanced GraphRAG Techniques",
                "content": (
                    "Modern GraphRAG implementations use techniques like graph neural networks, "
                    "entity linking, and semantic similarity to create more robust knowledge "
                    "graphs for retrieval."
                ),
            },
            {
                "url": "https://example.com/graphrag-benchmarks",
                "title": "GraphRAG Performance Benchmarks",
                "content": (
                    "Studies show that GraphRAG outperforms traditional RAG systems in terms of "
                    "factual accuracy and contextual understanding, especially for complex "
                    "queries requiring multi-hop reasoning."
                ),
            },
            {
                "url": "https://example.com/graphrag-applications",
                "title": "Real-world Applications of GraphRAG",
                "content": (
                    "GraphRAG has been successfully applied in domains such as scientific "
                    "literature analysis, legal document processing, and enterprise knowledge "
                    "management systems."
                ),
            },
        ]

    def search(self, query: str, num_results: int = 3) -> list[SourceDocument]:
        """Return search results for the given query.

        Implement with Tavily, Bing, SerpAPI, internal docs, or a local mock.
        """
        # Mock search - return random sources for demonstration
        selected_sources = random.sample(
            self.mock_sources, min(num_results, len(self.mock_sources))
        )

        return [
            SourceDocument(url=source["url"], title=source["title"], snippet=source["content"])
            for source in selected_sources
        ]
