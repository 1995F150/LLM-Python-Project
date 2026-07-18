"""Legacy wrapper. New integrations should import engine.agent."""

from engine.agent import get_agent_response

__all__ = ["get_agent_response"]
