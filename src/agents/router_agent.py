from src.agents.base import BaseAgent
from src.agents.scores.scores_workflow import scores_workflow
from langchain_core.messages import SystemMessage, HumanMessage


class RouterAgent(BaseAgent):
    """
    Router agent that analyzes user queries and routes them to the
    appropriate workflow.

    This agent determines user intent and selects the best workflow to handle the
    request. It is used internally by CfbAgent to route queries to feature-specific
    workflows.
    """

    def __init__(self, model: str = "openai:gpt-5-nano"):
        """
        Initialize the router agent.

        Args:
            model: The model to use for chat completions
        """
        super().__init__(model=model, tools=[])

    def route(self, user_message: str) -> str:
        """
        Analyze the user's query and route it to the appropriate workflow.

        Args:
            user_message: The user's query

        Returns:
            Response from the selected workflow
        """
        # Available workflows
        workflows = {
            "scores": {
                "name": "scores_workflow",
                "function": scores_workflow,
                "description": "Handles queries about game scores, results, and score-related information",
                "keywords": [
                    "score",
                    "scores",
                    "result",
                    "results",
                    "game",
                    "games",
                    "won",
                    "lost",
                    "beat",
                    "defeated",
                ],
            },
            # Future workflows can be added here:
            # "standings": {...},
            # "schedule": {...},
            # "stats": {...},
        }

        # Create the routing prompt
        workflow_list = "\n".join(
            [f"- {name}: {info['description']}" for name, info in workflows.items()]
        )

        routing_prompt = f"""You are a routing agent that analyzes user queries and determines which workflow should handle them.

        Available workflows:
        {workflow_list}

        User query: "{user_message}"

        Respond with ONLY the workflow name (e.g., "scores") that best matches the user's intent. If no workflow matches, respond with "unknown"."""

        messages = [
            SystemMessage(
                content="You are a routing agent that analyzes user queries and determines which workflow should handle them. Respond with only the workflow name."
            ),
            HumanMessage(content=routing_prompt),
        ]

        # Get the routing decision
        response = self.chat(messages)
        selected_workflow = response.content.strip().lower()

        # Route to the appropriate workflow
        if selected_workflow in workflows:
            workflow_func = workflows[selected_workflow]["function"]
            return workflow_func(user_message)
        else:
            # Handle unknown queries
            return f"I'm not sure how to help with that query. Currently, I can help with: {', '.join([w['description'] for w in workflows.values()])}."
