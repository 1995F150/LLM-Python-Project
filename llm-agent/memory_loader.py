"""Legacy compatibility exports."""

from memory.memory_loader import get_ai_memory


def load_memory_from_supabase(user_id: str):
    return get_ai_memory(user_id, limit=500)
