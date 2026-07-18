"""Header authentication shared by protected engine routes."""

from __future__ import annotations

import hmac
import logging

from fastapi import Header, HTTPException, status

from config import settings

logger = logging.getLogger(__name__)


async def validate_api_key(x_api_key: str | None = Header(default=None)) -> str:
    if not settings.api_keys:
        logger.error("No engine API key is configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Engine authentication is not configured",
        )
    if not x_api_key or not any(
        hmac.compare_digest(x_api_key, key) for key in settings.api_keys
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key
