"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

import os
from dataclasses import dataclass

from openai import OpenAI

from multi_agent_research_lab.core.errors import StudentTodoError


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion.

        Connect OpenAI, Azure OpenAI, or another provider.
        Keep retry, timeout, and token logging here rather than inside agents.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
            )

            return LLMResponse(
                content=response.choices[0].message.content,
                input_tokens=response.usage.prompt_tokens if response.usage else None,
                output_tokens=response.usage.completion_tokens if response.usage else None,
                cost_usd=self._calculate_cost(response.usage) if response.usage else None,
            )
        except Exception as e:
            raise StudentTodoError(f"Failed to complete LLM request: {str(e)}") from e

    def _calculate_cost(self, usage) -> float:
        """Calculate cost based on token usage."""
        # Pricing for gpt-4-turbo (as of 2024)
        input_cost_per_1k = 0.01
        output_cost_per_1k = 0.03
        return (
            (usage.prompt_tokens or 0) * input_cost_per_1k
            + (usage.completion_tokens or 0) * output_cost_per_1k
        ) / 1000
