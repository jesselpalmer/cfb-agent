import logging
from collections.abc import Callable
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.agents.base import BaseAgent
from src.agents.scores.scores_workflow import scores_workflow

logger = logging.getLogger(__name__)

UNKNOWN_WORKFLOW = "unknown"

WorkflowName = Literal["scores", "unknown"]
"""Every value the router may return. Keep in sync with ``WORKFLOWS``."""

WORKFLOWS: dict[str, tuple[Callable[[str], str], str]] = {
    "scores": (
        scores_workflow,
        "Handles queries about game scores, results, and score-related information",
    ),
    # Future workflows can be added here (and to WorkflowName):
    # "standings": (...),
    # "schedule": (...),
    # "stats": (...),
}


class RouteDecision(BaseModel):
    """The workflow that should handle a user's query."""

    workflow: WorkflowName = Field(
        description=(
            "Name of the workflow that best matches the user's intent, or "
            f"'{UNKNOWN_WORKFLOW}' if none of them fit."
        )
    )


class RouterAgent(BaseAgent):
    """
    Router agent that analyzes user queries and routes them to the
    appropriate workflow.

    The model returns a ``RouteDecision`` through LangChain structured output,
    so the choice is always one of the known workflow names instead of free
    text that has to be parsed. It is used internally by CfbAgent.
    """

    def __init__(self, model: str | None = None):
        """
        Initialize the router agent.

        Args:
            model: The model to use for chat completions. Defaults to the
                configured model in src/config.py.
        """
        super().__init__(model=model, tools=[])
        # include_raw keeps a malformed reply from raising; it shows up as
        # parsing_error and the router falls back to "unknown".
        self.router_llm = self.llm.with_structured_output(
            RouteDecision, include_raw=True
        )

    def decide(self, user_message: str) -> WorkflowName:
        """
        Ask the model which workflow should handle the query.

        Args:
            user_message: The user's query

        Returns:
            The selected workflow name, or "unknown"
        """
        workflow_list = "\n".join(
            f"- {name}: {description}" for name, (_, description) in WORKFLOWS.items()
        )
        messages = [
            SystemMessage(
                content=(
                    "You are a routing agent that decides which workflow should "
                    "handle a user's query about college football.\n\n"
                    f"Available workflows:\n{workflow_list}\n\n"
                    f"If no workflow matches, choose '{UNKNOWN_WORKFLOW}'."
                )
            ),
            HumanMessage(content=user_message),
        ]

        result = self.router_llm.invoke(messages)
        decision = result.get("parsed")
        if decision is None:
            logger.warning(
                "Router reply did not match RouteDecision: %s",
                result.get("parsing_error"),
            )
            return UNKNOWN_WORKFLOW
        return decision.workflow

    def route(self, user_message: str) -> str:
        """
        Analyze the user's query and route it to the appropriate workflow.

        Args:
            user_message: The user's query

        Returns:
            Response from the selected workflow
        """
        selected = self.decide(user_message)
        if selected in WORKFLOWS:
            workflow, _ = WORKFLOWS[selected]
            return workflow(user_message)

        descriptions = ", ".join(description for _, description in WORKFLOWS.values())
        return (
            "I'm not sure how to help with that query. "
            f"Currently, I can help with: {descriptions}."
        )
