"""Explicit, user-scoped diagnostic memory export (not exposed over HTTP)."""

from __future__ import annotations

import json
from pathlib import Path

from memory.memory_loader import get_ai_memory


def export_memory(user_id: str, output_dir: str = "data") -> str:
    if not user_id:
        raise ValueError("user_id is required; bulk private-memory export is forbidden")
    destination = Path(output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    file_path = destination / f"ai_memory_{user_id}.json"
    file_path.write_text(
        json.dumps(get_ai_memory(user_id, limit=500), indent=2), encoding="utf-8"
    )
    return str(file_path)
