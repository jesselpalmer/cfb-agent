from src.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage


class ScoresQAAgent(BaseAgent):
    """
    Quality assurance agent that validates and improves responses.

    Reviews content for accuracy, clarity, and completeness.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the QA agent.

        Args:
            model: The model to use for chat completions
        """
        super().__init__(model=model, tools=[])

    def review(self, content: str, original_request: str = None) -> str:
        """
        Review and improve a response for quality.

        Args:
            content: The content to review and improve
            original_request: The original user request to verify the response matches

        Returns:
            Improved and validated content
        """
        system_prompt = """You are a quality assurance reviewer. Check the content for accuracy, clarity, and completeness. 
        Verify that the response actually answers the user's original question. Improve it if needed, but keep the core information intact."""

        if original_request:
            human_prompt = f"""Original user request: "{original_request}"

Response to review: {content}

Please review this response and ensure it accurately answers the user's original question. Improve it if needed."""
        else:
            human_prompt = f"Review and improve this response: {content}"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt),
        ]
        response = self.chat(messages)
        return response.content
