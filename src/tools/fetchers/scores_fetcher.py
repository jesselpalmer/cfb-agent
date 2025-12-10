import json
from pathlib import Path
from typing import Optional, List, Dict
from langchain_core.tools import StructuredTool


def _load_scores_data() -> List[Dict]:
    """
    Load scores data from JSON file.

    Returns:
        List of score dictionaries
    """
    # Get the directory where this file is located
    current_dir = Path(__file__).parent
    json_file = current_dir / "scores_data.json"
    
    with open(json_file, "r") as f:
        return json.load(f)


# Load scores data at module level
_all_scores = _load_scores_data()


def get_scores(
    team: Optional[str] = None,
    date: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
) -> List[Dict]:
    """
    Get a list of scores with optional filtering.

    Args:
      team: Filter by team name (matches home or away team). Case-insensitive partial match.
      date: Filter by date in YYYY-MM-DD format.
      status: Filter by game status (e.g., "final", "live", "upcoming").
      location: Filter by location/stadium name. Case-insensitive partial match.

    Returns:
      list: A list of dictionaries containing the scores matching the filters.
    """
    all_scores = _all_scores

    # Apply filters
    filtered_scores = all_scores

    if team:
        filtered_scores = [
            score
            for score in filtered_scores
            if team.lower() in score["game"]["homeTeam"].lower()
            or team.lower() in score["game"]["awayTeam"].lower()
        ]

    if date:
        filtered_scores = [score for score in filtered_scores if score["date"] == date]

    if status:
        filtered_scores = [
            score
            for score in filtered_scores
            if score["status"].lower() == status.lower()
        ]

    if location:
        filtered_scores = [
            score
            for score in filtered_scores
            if location.lower() in score["location"].lower()
        ]

    return filtered_scores


# Create tool wrapper
get_scores_tool = StructuredTool.from_function(
    func=get_scores,
    name="get_scores",
    description="Get college football game scores with optional filtering by team, date, status, or location. Returns a list of game results with scores, teams, dates, and game status.",
)
