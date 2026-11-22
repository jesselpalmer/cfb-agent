"""
Configuration for the CFB Agent system.

This is the single place where model settings live. Every agent defaults to
``get_default_model()``, and any agent can still be given an explicit model.

Models use LangChain's ``provider:model`` format (for example
``openai:gpt-5-nano``) so that ``init_chat_model`` can pick the right
integration. Set the ``CFB_AGENT_MODEL`` environment variable to change the
default without editing code.
"""

import os

DEFAULT_MODEL = "openai:gpt-5-nano"
"""Model used by every agent unless overridden."""

MODEL_ENV_VAR = "CFB_AGENT_MODEL"
"""Environment variable that overrides ``DEFAULT_MODEL``."""

DEFAULT_TEMPERATURE = 1.0
"""Default sampling temperature. GPT-5 models only accept 1.0."""


def get_default_model() -> str:
    """Return the model to use, honoring the ``CFB_AGENT_MODEL`` override."""
    return os.getenv(MODEL_ENV_VAR) or DEFAULT_MODEL
