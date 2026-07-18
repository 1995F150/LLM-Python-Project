from __future__ import annotations

import re
from collections import Counter


def index_memory_content(content: str) -> dict[str, int]:
    """Return a deterministic token-frequency index for local diagnostics."""
    return dict(Counter(re.findall(r"[a-z0-9]+", content.lower())))
