"""Mock LLM client for testing purposes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class MockLLMClient:
    """Mock LLM client for testing without external API dependencies."""

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a mock model completion."""
        # Simple mock responses based on the prompt content
        if "research" in user_prompt.lower():
            return LLMResponse(
                content=f"Mock research response to: {user_prompt[:50]}...",
                input_tokens=50,
                output_tokens=100,
                cost_usd=0.0001,
            )
        elif "analyze" in user_prompt.lower():
            return LLMResponse(
                content=f"Mock analysis response to: {user_prompt[:50]}...",
                input_tokens=50,
                output_tokens=100,
                cost_usd=0.0001,
            )
        elif "write" in user_prompt.lower():
            return LLMResponse(
                content=f"Mock final answer to: {user_prompt[:50]}...",
                input_tokens=50,
                output_tokens=100,
                cost_usd=0.0001,
            )
        else:
            return LLMResponse(
                content="Mock response generated successfully.",
                input_tokens=50,
                output_tokens=100,
                cost_usd=0.0001,
            )
