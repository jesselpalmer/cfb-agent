"""
Main College Football Agent module.

This module provides the primary interface (CfbAgent) for the application.
It acts as the entry point for user queries and coordinates the agent system.
"""

from src.agents.router_agent import RouterAgent
from src.config import DEFAULT_MODEL


class CfbAgent:
    """
    Main College Football Agent that handles user queries about college football.

    This is the primary interface for the application. It uses a RouterAgent
    internally to route queries to the appropriate workflow.
    """

    def __init__(self, router_model: str = DEFAULT_MODEL) -> None:
        """
        Initialize the College Football Agent.

        Args:
            router_model: The model to use for the router agent
        """
        self.router = RouterAgent(model=router_model)

    def chat(self, user_message: str) -> str:
        """
        Process a user message and return a response.

        Args:
            user_message: The user's query

        Returns:
            Response from the appropriate workflow
        """
        return self.router.route(user_message)
