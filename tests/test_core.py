import logging

import pytest

from src.core import parse_args, setup_logging


def test_parse_args_defaults_to_normal():
    assert parse_args([]).log_level == "normal"


@pytest.mark.parametrize("level", ["quiet", "normal", "debug", "verbose"])
def test_parse_args_accepts_each_level(level):
    assert parse_args(["--log-level", level]).log_level == level


def test_parse_args_rejects_unknown_level():
    with pytest.raises(SystemExit):
        parse_args(["--log-level", "loud"])


def test_setup_logging_quiets_third_party_loggers():
    setup_logging("debug")
    assert logging.getLogger("httpx").level == logging.WARNING
