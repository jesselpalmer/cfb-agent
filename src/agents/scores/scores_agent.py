from src.agents.base import BaseAgent
from src.tools.fetchers.scores_fetcher import get_scores_tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.stdout import StdOutCallbackHandler
from typing import List, Dict, Union, Any, Optional


class SafeStdOutCallbackHandler(StdOutCallbackHandler):
    """A callback handler that extends StdOutCallbackHandler and safely handles None values."""

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: str,
        parent_run_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Handle chain start, safely handling None metadata."""
        try:
            # Ensure metadata is a dict before calling parent
            safe_metadata = metadata if metadata is not None else {}
            super().on_chain_start(
                serialized,
                inputs,
                run_id=run_id,
                parent_run_id=parent_run_id,
                tags=tags,
                metadata=safe_metadata,
                **kwargs,
            )
        except (AttributeError, TypeError) as e:
            # Silently ignore callback errors - they're non-critical
            # The error is usually "'NoneType' object has no attribute 'get'"
            pass


class ScoresAgent(BaseAgent):
    """
    Agent for handling score-related queries.

    This agent can answer questions about game scores, filter scores by team,
    date, status, or location using the get_scores tool.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the score agent with the get_scores tool.

        Args:
            model: The model to use for chat completions
        """
        super().__init__(model=model, tools=[get_scores_tool])

        # Create the prompt template for the agent
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful assistant that answers questions about college football game scores.
            You have access to a tool that can fetch game scores with various filters.
            Use the tool when you need to look up scores, then provide a clear and helpful answer to the user.
            Always be accurate and concise.""",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create the agent with tools
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)

        # Create the agent executor with a safe callback handler
        # Use custom callback handler to avoid NoneType errors while keeping verbose output
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,  # Keep verbose for debugging
            callbacks=[SafeStdOutCallbackHandler()],  # Use safe callback handler
        )

    def handle(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
    ) -> str:
        """
        Handle score-related queries.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Optional model override (not used in agent executor)

        Returns:
            String response from the agent
        """
        # Extract the user's input from messages
        # Find the last user message
        user_input = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_input = msg.get("content", "")
                break

        if not user_input:
            return "I didn't receive a valid user message."

        # Run the agent with chat_history (empty for now, but required by prompt)
        result = self.agent_executor.invoke({"input": user_input, "chat_history": []})
        return result.get("output", "I couldn't generate a response.")
