"""Tests for the single model configuration in src/config.py."""

from src.agents.base import BaseAgent
from src.config import DEFAULT_MODEL, MODEL_ENV_VAR, get_default_model


class TestConfig:
    def test_default_model(self):
        assert get_default_model() == DEFAULT_MODEL

    def test_env_var_overrides_default(self, monkeypatch):
        monkeypatch.setenv(MODEL_ENV_VAR, "openai:gpt-5-mini")
        assert get_default_model() == "openai:gpt-5-mini"

    def test_empty_env_var_falls_back_to_default(self, monkeypatch):
        monkeypatch.setenv(MODEL_ENV_VAR, "")
        assert get_default_model() == DEFAULT_MODEL


class TestBaseAgentModel:
    def test_uses_configured_model_unchanged(self, fake_chat_model):
        init = fake_chat_model()
        agent = BaseAgent()
        assert agent.model == DEFAULT_MODEL
        init.assert_called_once_with(DEFAULT_MODEL, temperature=1.0)

    def test_env_override_reaches_agent(self, monkeypatch, fake_chat_model):
        monkeypatch.setenv(MODEL_ENV_VAR, "openai:gpt-5-mini")
        fake_chat_model()
        assert BaseAgent().model == "openai:gpt-5-mini"

    def test_explicit_model_wins(self, monkeypatch, fake_chat_model):
        monkeypatch.setenv(MODEL_ENV_VAR, "openai:gpt-5-mini")
        fake_chat_model()
        assert BaseAgent(model="openai:gpt-5").model == "openai:gpt-5"

    def test_builds_real_openai_client_offline(self):
        """The real client can be built with the dummy key and no network."""
        agent = BaseAgent()
        assert agent.llm.model_name == DEFAULT_MODEL.split(":", 1)[1]

    def test_chat_converts_dict_messages(self, fake_chat_model):
        fake_chat_model("hello there")
        reply = BaseAgent().chat([{"role": "user", "content": "hi"}])
        assert reply.content == "hello there"
