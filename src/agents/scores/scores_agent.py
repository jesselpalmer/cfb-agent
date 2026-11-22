import logging

from langchain.agents import create_agent
from langchain_core.messages import AIMessage

from src.agents.base import BaseAgent
from src.tools.fetchers.scores_fetcher import get_scores_tool

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about college football game scores.
You have access to a tool that can fetch game scores with various filters.
Use the tool when you need to look up scores, then provide a clear and helpful answer to the user.
Always be accurate and concise."""

# Roles from the incoming conversation that are forwarded to the agent.
_CONVERSATION_ROLES = {"user", "assistant"}


class ScoresAgent(BaseAgent):
    """
    Agent for handling score-related queries.

    This agent can answer questions about game scores, filter scores by team,
    date, status, or location using the get_scores tool. It runs on LangChain's
    ``create_agent``, which builds a LangGraph tool-calling loop.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the score agent with the get_scores tool.

        Args:
            model: The model to use for chat completions
        """
        super().__init__(model=model, tools=[get_scores_tool])
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            name="scores_agent",
        )

    def handle(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
    ) -> str:
        """
        Handle score-related queries.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Unused; kept for interface compatibility. Pass a model to the
                constructor instead.

        Returns:
            String response from the agent
        """
        conversation = [
            {"role": msg["role"], "content": msg.get("content", "")}
            for msg in messages
            if msg.get("role") in _CONVERSATION_ROLES
        ]
        if not any(m["role"] == "user" and m["content"] for m in conversation):
            return "I didn't receive a valid user message."

        result = self.agent.invoke({"messages": conversation})

        for msg in result["messages"]:
            for call in getattr(msg, "tool_calls", None) or []:
                logger.debug("Tool call %s(%s)", call["name"], call["args"])

        final = result["messages"][-1]
        if isinstance(final, AIMessage) and final.text:
            return str(final.text)
        return "I couldn't generate a response."
