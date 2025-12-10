from src.agents.router_agent import RouterAgent


class CfbAgent:
    """
    Main College Football Agent that handles user queries about college football.
    
    This is the primary interface for the application. It uses a RouterAgent
    internally to route queries to the appropriate workflow.
    """

    def __init__(self, router_model: str = "openai:gpt-5-nano"):
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
