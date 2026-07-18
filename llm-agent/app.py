"""Legacy ASGI entrypoint that re-exports the production application."""

from app import app

__all__ = ["app"]
