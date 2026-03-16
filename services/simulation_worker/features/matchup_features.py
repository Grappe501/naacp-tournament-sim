def calculate_matchup_features(team_a, team_b):

    pace = (team_a["offense_rating"] + team_b["offense_rating"]) / 3

    strength_gap = team_a["net_rating"] - team_b["net_rating"]

    variance = abs(strength_gap) * 0.5

    return {
        "expected_pace": pace,
        "strength_gap": strength_gap,
        "variance_profile": variance
    }
