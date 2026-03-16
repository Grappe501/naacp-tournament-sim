import random


def simulate_team_injury_adjustment(base_team_rating: float, aggregated_injury_risk: float) -> float:
    injury_hit = random.random() < aggregated_injury_risk
    if not injury_hit:
        return base_team_rating

    penalty = random.uniform(1.5, 6.0)
    return max(0.0, base_team_rating - penalty)
