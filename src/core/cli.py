"""
Command-line argument parsing for the CFB Agent application.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from typing import get_args

from src.core.logging_config import LogLevel


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        argv: Arguments to parse. Defaults to sys.argv[1:].

    Returns:
        The parsed arguments, with a ``log_level`` attribute.
    """
    parser = argparse.ArgumentParser(
        description="A multi-agent AI system for college football information."
    )
    parser.add_argument(
        "--log-level",
        choices=get_args(LogLevel),
        default="normal",
        help="Logging verbosity (default: normal).",
    )
    return parser.parse_args(argv)
