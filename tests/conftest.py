import pytest


@pytest.fixture(autouse=True)
def _openai_api_key(monkeypatch):
    """ChatOpenAI requires a key at construction; tests never call the API."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
