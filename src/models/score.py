"""Pydantic models for college football score records."""

import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

GameStatus = Literal["upcoming", "live", "final"]


class _CamelModel(BaseModel):
    """Reads and writes camelCase keys (as in scores_data.json)."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
        frozen=True,
    )


class Matchup(_CamelModel):
    """The two teams in a game."""

    home_team: str = Field(min_length=1)
    away_team: str = Field(min_length=1)


class ScoreLine(_CamelModel):
    """Points for each team."""

    home_score: int = Field(ge=0)
    away_score: int = Field(ge=0)


class Score(_CamelModel):
    """One game's score, schedule, and status."""

    game: Matchup
    score: ScoreLine
    date: dt.date
    time: dt.time
    location: str
    status: GameStatus
    quarter: int = Field(ge=0, description="0 before kickoff; above 4 is overtime")
    time_remaining: str = Field(pattern=r"^\d{1,2}:\d{2}$")
