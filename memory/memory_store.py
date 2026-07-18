"""Supabase client lifecycle. The service-role key never leaves this process."""

from __future__ import annotations

import logging

from supabase import Client, create_client

from config import settings

logger = logging.getLogger(__name__)
_client: Client | None = None


def init_supabase() -> Client | None:
    global _client
    if _client is not None:
        return _client
    if not settings.supabase_url or not settings.supabase_service_role_key:
        logger.warning("Supabase is not configured; memory context is unavailable")
        return None
    try:
        _client = create_client(
            settings.supabase_url, settings.supabase_service_role_key
        )
    except Exception:
        logger.exception("Supabase client initialization failed")
        return None
    return _client


def get_supabase() -> Client | None:
    return init_supabase()


# Backward-compatible module attribute for older integrations.
supabase = init_supabase()
