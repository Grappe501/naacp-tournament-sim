import random


def simulate_injury_risk(player_features):

    risk = random.uniform(0, 1)

    if risk < 0.01:
        return "season_ending"

    if risk < 0.05:
        return "multi_game"

    if risk < 0.10:
        return "limited_minutes"

    return "healthy"
