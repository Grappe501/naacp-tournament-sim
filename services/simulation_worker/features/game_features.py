def calculate_game_features(team_a, team_b):

    pace = (team_a["offense_rating"] + team_b["offense_rating"]) / 3

    variance = abs(team_a["net_rating"] - team_b["net_rating"]) * 0.5

    return {
        "expected_pace": pace,
        "variance_profile": variance
    }
