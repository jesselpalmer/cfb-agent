from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Optional, List, Union

# Load environment variables (API keys, etc.) from .env file
load_dotenv()


class BaseAgent:
    """
    Base class for all agents.

    Handles common initialization and provides a chat method for making
    API requests. All agents should inherit from this class.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 1.0,
        tools: Optional[List] = None,
    ):
        """
        Initialize the base agent.

        Args:
            model: The OpenAI model to use (e.g., "gpt-4o-mini", "gpt-4o")
            temperature: Controls randomness (0-2, higher = more random)
            tools: List of tools the agent can use
        """
        # Map aisuite model format to OpenAI model names
        model_mapping = {
            "openai:gpt-5-nano": "gpt-4o-mini",  # Fallback to closest available
        }
        actual_model = model_mapping.get(model, model)
        self.model = actual_model  # Store model name for later use

        self.llm = ChatOpenAI(
            model=actual_model,
            temperature=temperature,
        )
        self.tools = tools or []

    def chat(
        self,
        messages: List[Union[dict, HumanMessage, SystemMessage, AIMessage]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        """
        Make a chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content',
                     or message objects
            model: Override the default model for this request
            temperature: Override the default temperature for this request

        Returns:
            AIMessage object
        """
        # Convert dict messages to message objects if needed
        langchain_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
                else:
                    langchain_messages.append(HumanMessage(content=content))
            else:
                langchain_messages.append(msg)

        # Create LLM instance with optional overrides
        llm = self.llm
        if model or temperature is not None:
            llm = ChatOpenAI(
                model=model or self.model,
                temperature=(
                    temperature if temperature is not None else self.llm.temperature
                ),
            )

        # Bind tools if available
        if self.tools:
            llm = llm.bind_tools(self.tools)

        return llm.invoke(langchain_messages)
