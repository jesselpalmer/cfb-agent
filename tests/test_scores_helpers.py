"""Offline tests for the analyzer and QA agents using a fake chat model."""

from src.agents.scores.scores_analyzer_agent import ScoresAnalyzerAgent
from src.agents.scores.scores_qa_agent import ScoresQAAgent
from src.config import DEFAULT_MODEL


def test_analyzer_returns_model_reply(fake_chat_model):
    init = fake_chat_model("Hokies roll.")
    agent = ScoresAnalyzerAgent()
    assert agent.analyze("Virginia Tech 31, Clemson 14") == "Hokies roll."
    init.assert_called_once_with(DEFAULT_MODEL, temperature=1.0)


def test_qa_returns_model_reply(fake_chat_model):
    fake_chat_model("Reviewed.")
    agent = ScoresQAAgent()
    assert agent.review("draft", original_request="Who won?") == "Reviewed."
