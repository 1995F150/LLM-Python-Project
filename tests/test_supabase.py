import pytest
import os
from memory.memory_store import supabase, init_supabase
from memory.memory_loader import (
    get_ai_memory, get_writing_samples, get_training_corpus,
    get_profiles, get_chat_history
)

def test_supabase_initialization():
    """Verifies that the Supabase client handles missing keys gracefully."""
    client = init_supabase()
    assert client is None or hasattr(client, "table")

def test_graceful_degradation_ai_memory():
    """Verifies that get_ai_memory returns a list (empty if no connection)."""
    data = get_ai_memory()
    assert isinstance(data, list)

def test_graceful_degradation_writing_samples():
    """Verifies that get_writing_samples returns a list."""
    data = get_writing_samples()
    assert isinstance(data, list)

def test_graceful_degradation_training_corpus():
    """Verifies that get_training_corpus returns a list."""
    data = get_training_corpus()
    assert isinstance(data, list)

def test_graceful_degradation_profiles():
    """Verifies that get_profiles returns a list."""
    data = get_profiles()
    assert isinstance(data, list)

def test_graceful_degradation_chat_history():
    """Verifies that get_chat_history returns a list."""
    data = get_chat_history()
    assert isinstance(data, list)

@pytest.mark.skipif(not os.getenv("SUPABASE_URL"), reason="Supabase credentials not in environment")
def test_active_supabase_connection():
    """Verifies actual connection if environment variables are set."""
    if supabase:
        try:
            res = supabase.table("ai_memory").select("*").limit(1).execute()
            assert hasattr(res, 'data')
        except Exception as e:
            pytest.fail(f"Supabase connection test failed: {e}")
