from src.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage


class ScoresAnalyzerAgent(BaseAgent):
    """
    Agent that adds color and analysis to responses.

    Takes raw content and enhances it with analysis, context, and insights.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the analyzer agent.

        Args:
            model: The model to use for chat completions
        """
        super().__init__(model=model, tools=[])

    def analyze(self, content: str) -> str:
        """
        Add color and analysis to raw content.

        Args:
            content: The raw content to analyze and enhance

        Returns:
            Enhanced content with analysis and color
        """
        messages = [
            SystemMessage(
                content="You are a sports analyst. Add color, context, and interesting insights to sports information. Make it engaging and informative. Keep it less than 200 characters and it must be factual."
            ),
            HumanMessage(
                content=f"Add color and analysis to this sports information: {content}"
            ),
        ]
        response = self.chat(messages)
        return response.content
