"""Memory is read directly from Supabase; no unsafe all-user disk mirror is required."""

from memory.memory_store import get_supabase


def sync_memory_to_remote() -> bool:
    """Compatibility health check for the former sync entrypoint."""
    return get_supabase() is not None
