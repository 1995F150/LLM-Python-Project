from memory import memory_loader


def test_private_memory_requires_user_id():
    assert memory_loader.get_ai_memory(None) == []
    assert memory_loader.get_conversation_history(None) == []
    assert memory_loader.get_user_preferences(None) == []


def test_context_loader_is_bounded_without_supabase(monkeypatch):
    monkeypatch.setattr(memory_loader, "get_supabase", lambda: None)
    context, rows = memory_loader.build_context(None, None, "hello")
    assert context == ""
    assert rows == 0
