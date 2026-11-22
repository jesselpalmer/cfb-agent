"""
Test suite for CfbAgent class.

Tests the main College Football Agent interface that coordinates
the agent system. All model calls are faked, so these run offline.
"""

from typing import get_args
from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from src.agents.cfb_agent import CfbAgent
from src.agents.router_agent import (
    UNKNOWN_WORKFLOW,
    WORKFLOWS,
    RouteDecision,
    RouterAgent,
    WorkflowName,
)
from src.config import DEFAULT_MODEL


class TestCfbAgent:
    """Test suite for CfbAgent functionality."""

    def test_init(self, fake_structured_model):
        """CfbAgent uses the configured model as-is, with no silent swap."""
        fake_structured_model(RouteDecision)
        agent = CfbAgent()
        assert isinstance(agent.router, RouterAgent)
        assert agent.router.model == DEFAULT_MODEL

    def test_init_custom_router_model(self, fake_structured_model):
        """Test CfbAgent initialization with custom router model."""
        fake_structured_model(RouteDecision)
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
    """Routing decisions with a fake model that returns structured output."""

    def test_routes_to_scores(self, fake_structured_model):
        fake_structured_model(RouteDecision, {"workflow": "scores"})
        workflow = Mock(return_value="scores!")
        with patch.dict(WORKFLOWS, {"scores": (workflow, "scores")}):
            result = RouterAgent().route("Who won the Hokies game?")
        assert result == "scores!"
        workflow.assert_called_once_with("Who won the Hokies game?")

    def test_unknown_intent(self, fake_structured_model):
        fake_structured_model(RouteDecision, {"workflow": "unknown"})
        workflow = Mock()
        with patch.dict(WORKFLOWS, {"scores": (workflow, "scores")}):
            result = RouterAgent().route("What's the weather?")
        assert result.startswith("I'm not sure how to help")
        workflow.assert_not_called()

    def test_decide_returns_typed_choice(self, fake_structured_model):
        fake_structured_model(RouteDecision, {"workflow": "scores"})
        assert RouterAgent().decide("Score of the Iron Bowl?") == "scores"

    def test_invalid_choice_falls_back_to_unknown(self, fake_structured_model):
        """A workflow name outside the schema is rejected, not routed."""
        fake_structured_model(RouteDecision, {"workflow": "weather"})
        assert RouterAgent().decide("Will it rain Saturday?") == UNKNOWN_WORKFLOW

    def test_workflow_names_match_registry(self):
        """Every routable workflow is in the schema, and nothing else is."""
        assert set(get_args(WorkflowName)) == {*WORKFLOWS, UNKNOWN_WORKFLOW}

    def test_route_decision_rejects_unknown_names(self):
        with pytest.raises(ValidationError):
            RouteDecision(workflow="weather")
