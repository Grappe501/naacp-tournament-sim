from dataclasses import dataclass
import random


@dataclass
class TeamGameInput:
    team_id: int
    team_name: str
    offense_rating: float
    defense_rating: float
    pace: float
    recent_form: float
    injury_adjusted_rating: float


def expected_score(team: TeamGameInput, opponent: TeamGameInput, neutral_court: bool = True) -> float:
    base = (team.offense_rating + (100 - opponent.defense_rating) + team.recent_form + team.injury_adjusted_rating) / 2
    pace_factor = team.pace / 70.0
    location_bonus = 0.0 if neutral_court else 3.2
    return (base * pace_factor) + location_bonus


def simulate_game(team_a: TeamGameInput, team_b: TeamGameInput, neutral_court: bool = True, score_std_dev: float = 11.5) -> dict:
    a_mean = expected_score(team_a, team_b, neutral_court=neutral_court)
    b_mean = expected_score(team_b, team_a, neutral_court=neutral_court)

    a_score = round(max(40, random.gauss(a_mean, score_std_dev)))
    b_score = round(max(40, random.gauss(b_mean, score_std_dev)))

    if a_score == b_score:
        if random.random() >= 0.5:
            a_score += 1
        else:
            b_score += 1

    winner = team_a if a_score > b_score else team_b

    return {
        "team_a_id": team_a.team_id,
        "team_a_name": team_a.team_name,
        "team_b_id": team_b.team_id,
        "team_b_name": team_b.team_name,
        "team_a_score": a_score,
        "team_b_score": b_score,
        "winner_team_id": winner.team_id,
        "winner_team_name": winner.team_name,
        "margin": abs(a_score - b_score),
    }
