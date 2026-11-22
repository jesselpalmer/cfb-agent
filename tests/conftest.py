"""
Shared pytest fixtures.

Tests must never reach a real model provider. Every test gets a dummy OpenAI
key and an unreachable base URL, so a request that slips past the mocks fails
fast instead of calling the API. Tests that need model output use the
``fake_chat_model`` fixture, which swaps ``init_chat_model`` for LangChain's
fake chat model.
"""

from unittest.mock import patch

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from src.config import MODEL_ENV_VAR


@pytest.fixture(autouse=True)
def offline_openai(monkeypatch):
    """Point the OpenAI client at nothing so no test can call the real API."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-real")
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:9/v1")
    monkeypatch.delenv(MODEL_ENV_VAR, raising=False)


@pytest.fixture
def fake_chat_model():
    """
    Replace the chat model every agent builds with a fake one.

    Call the fixture with the replies the model should give, in order. It
    returns the mock for ``init_chat_model`` so tests can check which model
    an agent asked for.
    """
    patchers = []

    def _install(*responses: str):
        fake = FakeListChatModel(responses=list(responses) or ["ok"])
        patcher = patch("src.agents.base.init_chat_model", return_value=fake)
        patchers.append(patcher)
        return patcher.start()

    yield _install

    for patcher in patchers:
        patcher.stop()
