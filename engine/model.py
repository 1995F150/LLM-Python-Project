from __future__ import annotations

import requests

from config import settings


def load_model(model_name: str | None = None) -> dict:
    """Ask Ollama to load/check a model without duplicating model state in Python."""
    selected = model_name or settings.ollama_model
    response = requests.post(
        f"{settings.ollama_base_url}/api/show",
        json={"model": selected},
        timeout=(5, 30),
    )
    response.raise_for_status()
    return response.json()
