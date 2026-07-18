"""Legacy compatibility exports."""

from memory.memory_loader import build_context


def get_formatted_context(user_id: str, message: str = "") -> str:
    context, _ = build_context(user_id, None, message)
    return context
