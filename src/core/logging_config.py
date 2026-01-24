"""
Logging configuration for the CFB Agent system.

This module provides a centralized logging setup with multiple verbosity levels.
"""

import logging
from typing import Literal

LogLevel = Literal["quiet", "normal", "debug", "verbose"]

# Third-party loggers that are noisy at DEBUG level
_NOISY_LOGGERS = [
    "httpcore",
    "httpx",
    "urllib3",
    "openai",
    "sentence_transformers",
    "transformers",
    "huggingface_hub",
]


def setup_logging(level: LogLevel = "normal") -> None:
    """
    Configure logging for the application.

    Args:
        level: The logging verbosity level:
            - "quiet": Only errors (minimal output)
            - "normal": Only warnings and errors (default, no INFO logs)
            - "debug": Debug logs from application, suppresses third-party noise
            - "verbose": Full debug output including third-party libraries
    """
    level_map = {
        "quiet": logging.ERROR,
        "normal": logging.WARNING,
        "debug": logging.DEBUG,
        "verbose": logging.DEBUG,
    }

    log_level = level_map.get(level, logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="[%(levelname)s] %(name)s: %(message)s",
    )

    # Suppress noisy third-party loggers unless verbose mode
    if level != "verbose":
        for logger_name in _NOISY_LOGGERS:
            logging.getLogger(logger_name).setLevel(logging.WARNING)
