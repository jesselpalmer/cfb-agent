"""
Test suite for CfbAgent class.

Tests the main College Football Agent interface that coordinates
the agent system. All model calls are faked, so these run offline.
"""

from unittest.mock import Mock, patch

from src.agents.cfb_agent import CfbAgent
from src.agents.router_agent import RouterAgent
from src.config import DEFAULT_MODEL


class TestCfbAgent:
    """Test suite for CfbAgent functionality."""

    def test_init(self, fake_chat_model):
        """CfbAgent uses the configured model as-is, with no silent swap."""
        fake_chat_model()
        agent = CfbAgent()
        assert isinstance(agent.router, RouterAgent)
        assert agent.router.model == DEFAULT_MODEL

    def test_init_custom_router_model(self, fake_chat_model):
        """Test CfbAgent initialization with custom router model."""
        fake_chat_model()
        agent = CfbAgent(router_model="openai:gpt-5-mini")
        assert isinstance(agent.router, RouterAgent)
        assert agent.router.model == "openai:gpt-5-mini"

    @patch("src.agents.cfb_agent.RouterAgent")
    def test_chat(self, mock_router_class):
        """Test chat method routes to router."""
        mock_router_instance = Mock()
        mock_router_instance.route.return_value = "Test response"
        mock_router_class.return_value = mock_router_instance

        agent = CfbAgent()
        result = agent.chat("What are the scores?")

        assert result == "Test response"
        mock_router_instance.route.assert_called_once_with("What are the scores?")


class TestRouterAgent:
    """Routing decisions with a fake model."""

    @patch("src.agents.router_agent.scores_workflow", return_value="scores!")
    def test_routes_to_scores(self, mock_workflow, fake_chat_model):
        fake_chat_model("scores")
        result = RouterAgent().route("Who won the Hokies game?")
        assert result == "scores!"
        mock_workflow.assert_called_once_with("Who won the Hokies game?")

    @patch("src.agents.router_agent.scores_workflow")
    def test_unknown_intent(self, mock_workflow, fake_chat_model):
        fake_chat_model("unknown")
        result = RouterAgent().route("What's the weather?")
        assert result.startswith("I'm not sure how to help")
        mock_workflow.assert_not_called()
