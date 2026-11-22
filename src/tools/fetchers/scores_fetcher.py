import datetime as dt
from pathlib import Path

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, TypeAdapter

from src.models.score import GameStatus, Score

SCORES_FILE = Path(__file__).parent / "scores_data.json"

_scores_adapter = TypeAdapter(list[Score])


def load_scores(path: Path = SCORES_FILE) -> list[Score]:
    """
    Load and validate score records from a JSON file.

    Raises:
        pydantic.ValidationError: If any record doesn't match ``Score``.
    """
    return _scores_adapter.validate_json(path.read_bytes())


# Load and validate scores data once, at import time.
_all_scores = load_scores()


class GetScoresInput(BaseModel):
    """Filters the get_scores tool accepts. Every filter is optional."""

    team: str | None = Field(
        default=None,
        description="Team name, matched against home or away team. "
        "Case-insensitive partial match.",
    )
    date: dt.date | None = Field(
        default=None, description="Game date in YYYY-MM-DD format."
    )
    status: GameStatus | None = Field(default=None, description="Game status.")
    location: str | None = Field(
        default=None,
        description="Stadium or location name. Case-insensitive partial match.",
    )


def get_scores(
    team: str | None = None,
    date: dt.date | str | None = None,
    status: str | None = None,
    location: str | None = None,
) -> list[Score]:
    """
    Get a list of scores with optional filtering.

    Args:
      team: Filter by team name (matches home or away team). Case-insensitive
        partial match.
      date: Filter by date, as a ``date`` or a YYYY-MM-DD string.
      status: Filter by game status ("final", "live", "upcoming").
        Case-insensitive.
      location: Filter by location/stadium name. Case-insensitive partial match.

    Returns:
      The ``Score`` records matching every filter given.
    """
    if isinstance(date, str):
        date = dt.date.fromisoformat(date)

    def matches(score: Score) -> bool:
        teams = f"{score.game.home_team}\n{score.game.away_team}".lower()
        return (
            (not team or team.lower() in teams)
            and (not date or score.date == date)
            and (not status or score.status == status.lower())
            and (not location or location.lower() in score.location.lower())
        )

    return [score for score in _all_scores if matches(score)]


def _get_scores_for_tool(**filters) -> list[dict]:
    """Run get_scores and serialize the results as camelCase JSON for the model."""
    return [
        score.model_dump(mode="json", by_alias=True) for score in get_scores(**filters)
    ]


get_scores_tool = StructuredTool.from_function(
    func=_get_scores_for_tool,
    name="get_scores",
    description="Get college football game scores with optional filtering by team, date, status, or location. Returns a list of game results with scores, teams, dates, and game status.",
    args_schema=GetScoresInput,
)
