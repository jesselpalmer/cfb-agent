from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.config import DEFAULT_TEMPERATURE, get_default_model

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
        model: str | None = None,
        temperature: float = DEFAULT_TEMPERATURE,
        tools: list | None = None,
    ):
        """
        Initialize the base agent.

        Args:
            model: Model in LangChain's "provider:model" format
                (e.g., "openai:gpt-5-nano"). Defaults to the configured model
                in src/config.py.
            temperature: Controls randomness (0-2, higher = more random)
            tools: List of tools the agent can use
        """
        self.model = model or get_default_model()
        self.temperature = temperature
        self.llm = init_chat_model(self.model, temperature=temperature)
        self.tools = tools or []

    def chat(
        self,
        messages: list[dict | HumanMessage | SystemMessage | AIMessage],
        model: str | None = None,
        temperature: float | None = None,
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
            llm = init_chat_model(
                model or self.model,
                temperature=(
                    temperature if temperature is not None else self.temperature
                ),
            )

        # Bind tools if available
        if self.tools:
            llm = llm.bind_tools(self.tools)

        return llm.invoke(langchain_messages)
