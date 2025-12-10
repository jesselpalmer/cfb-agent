from src.tools.fetchers.scores_fetcher import get_scores


class TestGetScoresFiltering:
    """Test suite for get_scores filtering functionality."""

    def test_no_filters_returns_all_scores(self):
        """Test that without filters, all scores are returned."""
        results = get_scores()
        assert len(results) == 3
        assert all("game" in score for score in results)
        assert all("score" in score for score in results)

    def test_team_filter_home_team(self):
        """Test filtering by home team name."""
        results = get_scores(team="Virginia Tech")
        assert len(results) == 1
        assert results[0]["game"]["homeTeam"] == "Virginia Tech"

    def test_team_filter_away_team(self):
        """Test filtering by away team name."""
        results = get_scores(team="Clemson")
        assert len(results) == 1
        assert results[0]["game"]["awayTeam"] == "Clemson"

    def test_team_filter_case_insensitive(self):
        """Test that team filtering is case-insensitive."""
        results_lower = get_scores(team="alabama")
        results_upper = get_scores(team="ALABAMA")
        results_mixed = get_scores(team="AlAbAmA")

        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1
        assert results_lower[0]["game"]["homeTeam"] == "Alabama"

    def test_team_filter_partial_match(self):
        """Test that team filtering supports partial matches."""
        results = get_scores(team="Virginia")
        assert len(results) == 1
        assert "Virginia" in results[0]["game"]["homeTeam"]

    def test_team_filter_no_match(self):
        """Test that filtering by non-existent team returns empty list."""
        results = get_scores(team="NonExistent Team")
        assert len(results) == 0

    def test_date_filter_exact_match(self):
        """Test filtering by exact date match."""
        results = get_scores(date="2025-01-01")
        assert len(results) == 3
        assert all(score["date"] == "2025-01-01" for score in results)

    def test_date_filter_no_match(self):
        """Test that filtering by non-existent date returns empty list."""
        results = get_scores(date="2025-12-31")
        assert len(results) == 0

    def test_status_filter_exact_match(self):
        """Test filtering by status."""
        results = get_scores(status="final")
        assert len(results) == 3
        assert all(score["status"] == "final" for score in results)

    def test_status_filter_case_insensitive(self):
        """Test that status filtering is case-insensitive."""
        results_lower = get_scores(status="final")
        results_upper = get_scores(status="FINAL")
        results_mixed = get_scores(status="FiNaL")

        assert len(results_lower) == 3
        assert len(results_upper) == 3
        assert len(results_mixed) == 3

    def test_status_filter_no_match(self):
        """Test that filtering by non-existent status returns empty list."""
        results = get_scores(status="live")
        assert len(results) == 0

    def test_location_filter_exact_match(self):
        """Test filtering by location."""
        results = get_scores(location="Lane Stadium")
        assert len(results) == 1
        assert results[0]["location"] == "Lane Stadium"

    def test_location_filter_partial_match(self):
        """Test that location filtering supports partial matches."""
        results = get_scores(location="Stadium")
        assert len(results) == 3
        assert all("Stadium" in score["location"] for score in results)

    def test_location_filter_case_insensitive(self):
        """Test that location filtering is case-insensitive."""
        results_lower = get_scores(location="lane stadium")
        results_upper = get_scores(location="LANE STADIUM")
        results_mixed = get_scores(location="LaNe StAdIuM")

        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1
        assert results_lower[0]["location"] == "Lane Stadium"

    def test_location_filter_no_match(self):
        """Test that filtering by non-existent location returns empty list."""
        results = get_scores(location="NonExistent Stadium")
        assert len(results) == 0

    def test_multiple_filters_team_and_date(self):
        """Test combining multiple filters (team and date)."""
        results = get_scores(team="Virginia Tech", date="2025-01-01")
        assert len(results) == 1
        assert results[0]["game"]["homeTeam"] == "Virginia Tech"
        assert results[0]["date"] == "2025-01-01"

    def test_multiple_filters_team_and_location(self):
        """Test combining team and location filters."""
        results = get_scores(team="Alabama", location="Bryant-Denny")
        assert len(results) == 1
        assert results[0]["game"]["homeTeam"] == "Alabama"
        assert "Bryant-Denny" in results[0]["location"]

    def test_multiple_filters_all_parameters(self):
        """Test combining all filter parameters."""
        results = get_scores(
            team="Ohio State",
            date="2025-01-01",
            status="final",
            location="Ohio Stadium",
        )
        assert len(results) == 1
        assert results[0]["game"]["homeTeam"] == "Ohio State"
        assert results[0]["date"] == "2025-01-01"
        assert results[0]["status"] == "final"
        assert results[0]["location"] == "Ohio Stadium"

    def test_multiple_filters_no_match(self):
        """Test that multiple filters with no matching results return empty list."""
        results = get_scores(team="Virginia Tech", date="2025-12-31")  # Wrong date
        assert len(results) == 0
