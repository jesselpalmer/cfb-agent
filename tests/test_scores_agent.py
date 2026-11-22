"""Tests for ScoresAgent running on LangChain's create_agent."""

from typing import Any

import pytest
from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from src.agents.scores.scores_agent import ScoresAgent


class FakeToolCallingModel(GenericFakeChatModel):
    """Fake chat model that accepts bound tools and replays scripted replies."""

    def bind_tools(self, tools: Any, **kwargs: Any) -> "FakeToolCallingModel":
        return self


@pytest.fixture
def agent():
    return ScoresAgent()


def _use_replies(agent: ScoresAgent, replies: list) -> None:
    """Rebuild the agent graph around a fake model that returns `replies`."""
    agent.agent = create_agent(
        model=FakeToolCallingModel(messages=iter(replies)),
        tools=agent.tools,
        system_prompt="test",
    )


def test_calls_scores_tool_and_returns_final_answer(agent):
    _use_replies(
        agent,
        [
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "get_scores", "args": {"team": "Georgia"}, "id": "c1"}
                ],
            ),
            AIMessage(content="Georgia won."),
        ],
    )

    result = agent.handle([{"role": "user", "content": "How did Georgia do?"}])

    assert result == "Georgia won."


def test_tool_result_is_passed_back_to_model(agent):
    model = FakeToolCallingModel(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[
                        {"name": "get_scores", "args": {"team": "Georgia"}, "id": "c1"}
                    ],
                ),
                AIMessage(content="done"),
            ]
        )
    )
    agent.agent = create_agent(model=model, tools=agent.tools)
    result = agent.agent.invoke(
        {"messages": [{"role": "user", "content": "Georgia scores"}]}
    )

    tool_messages = [m for m in result["messages"] if m.type == "tool"]
    assert len(tool_messages) == 1
    assert "Georgia" in tool_messages[0].content


def test_returns_fallback_without_user_message(agent):
    assert agent.handle([{"role": "system", "content": "hi"}]) == (
        "I didn't receive a valid user message."
    )


def test_forwards_conversation_history(agent):
    _use_replies(agent, [AIMessage(content="ok")])
    captured = {}
    original_invoke = agent.agent.invoke

    def spy(payload, *args, **kwargs):
        captured.update(payload)
        return original_invoke(payload, *args, **kwargs)

    agent.agent.invoke = spy
    agent.handle(
        [
            {"role": "system", "content": "ignored"},
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "reply"},
            {"role": "user", "content": "second"},
        ]
    )

    assert [m["role"] for m in captured["messages"]] == ["user", "assistant", "user"]
