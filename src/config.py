"""
Configuration constants for the CFB Agent system.

This module contains default values and configuration constants that can be
easily modified in one location. All defaults can still be overridden via
parameters when instantiating classes.
"""

DEFAULT_MODEL = "openai:gpt-5-nano"

MODEL_MAPPING = {
    "openai:gpt-5-nano": "gpt-4o-mini",
}
