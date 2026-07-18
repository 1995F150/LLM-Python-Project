from __future__ import annotations

from typing import Any

from engine.inference import InferenceResult, generate


def get_agent_response(
    user_input: str,
    *,
    user_id: str | None = None,
    conversation_id: str | None = None,
    system_prompt: str | None = None,
    conversation_history: list[dict[str, Any]] | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> InferenceResult:
    return generate(
        user_input,
        user_id=user_id,
        conversation_id=conversation_id,
        system_prompt=system_prompt,
        conversation_history=conversation_history,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
