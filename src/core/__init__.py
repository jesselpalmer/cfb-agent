"""Core application setup: CLI argument parsing and logging configuration."""

from src.core.cli import parse_args
from src.core.logging_config import LogLevel, setup_logging

__all__ = ["LogLevel", "parse_args", "setup_logging"]
