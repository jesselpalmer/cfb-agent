"""
Test suite for CfbAgent class.

Tests the main College Football Agent interface that coordinates
the agent system.
"""

from unittest.mock import Mock, patch
from src.agents.cfb_agent import CfbAgent
from src.agents.router_agent import RouterAgent
from src.config import DEFAULT_MODEL, MODEL_MAPPING


class TestCfbAgent:
    """Test suite for CfbAgent functionality."""

    def test_init(self):
        """Test CfbAgent initialization."""
        agent = CfbAgent()
        assert isinstance(agent.router, RouterAgent)
        assert agent.router.model == MODEL_MAPPING.get(DEFAULT_MODEL, DEFAULT_MODEL)

    def test_init_custom_router_model(self):
        """Test CfbAgent initialization with custom router model."""
        agent = CfbAgent(router_model="gpt-4o")
        assert isinstance(agent.router, RouterAgent)
        assert agent.router.model == "gpt-4o"

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
