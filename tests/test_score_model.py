"""Validation rules for the Score model and the scores data file."""

import datetime as dt
import json

import pytest
from pydantic import ValidationError

from src.models.score import Score
from src.tools.fetchers.scores_fetcher import SCORES_FILE, load_scores

VALID_RECORD = {
    "game": {"homeTeam": "Virginia Tech", "awayTeam": "Clemson"},
    "score": {"homeScore": 17, "awayScore": 10},
    "date": "2025-01-01",
    "time": "12:00:00",
    "location": "Lane Stadium",
    "status": "final",
    "quarter": 4,
    "timeRemaining": "00:00",
}


def _with(**changes) -> dict:
    return {**VALID_RECORD, **changes}


def test_parses_camel_case_record():
    score = Score.model_validate(VALID_RECORD)
    assert score.game.home_team == "Virginia Tech"
    assert score.score.away_score == 10
    assert score.date == dt.date(2025, 1, 1)
    assert score.time == dt.time(12, 0)
    assert score.time_remaining == "00:00"


def test_round_trips_to_camel_case_json():
    score = Score.model_validate(VALID_RECORD)
    assert score.model_dump(mode="json", by_alias=True) == VALID_RECORD


@pytest.mark.parametrize(
    "record",
    [
        _with(status="halftime"),
        _with(date="01/01/2025"),
        _with(quarter=-1),
        _with(timeRemaining="soon"),
        _with(score={"homeScore": -3, "awayScore": 10}),
        _with(game={"homeTeam": "", "awayTeam": "Clemson"}),
        _with(extraField="oops"),
        {k: v for k, v in VALID_RECORD.items() if k != "location"},
    ],
    ids=[
        "bad-status",
        "bad-date",
        "negative-quarter",
        "bad-clock",
        "negative-score",
        "empty-team",
        "unknown-field",
        "missing-field",
    ],
)
def test_rejects_invalid_records(record):
    with pytest.raises(ValidationError):
        Score.model_validate(record)


def test_bundled_data_is_valid():
    assert len(load_scores()) == 3


def test_load_scores_rejects_bad_file(tmp_path):
    bad = tmp_path / "scores.json"
    bad.write_text(json.dumps([_with(status="halftime")]))
    with pytest.raises(ValidationError):
        load_scores(bad)


def test_default_path_is_bundled_file():
    assert SCORES_FILE.name == "scores_data.json"
    assert SCORES_FILE.exists()
