from utils.file_utils import write_file, ensure_dir


def build_simulation():
    print("Building simulation lab...")

    ensure_dir("services/simulation_worker")
    ensure_dir("services/simulation_worker/models")
    ensure_dir("services/simulation_worker/engines")
    ensure_dir("services/simulation_worker/scenarios")
    ensure_dir("services/simulation_worker/exports")
    ensure_dir("services/simulation_worker/config")

    write_file("services/simulation_worker/__init__.py", "")
    write_file("services/simulation_worker/models/__init__.py", "")
    write_file("services/simulation_worker/engines/__init__.py", "")
    write_file("services/simulation_worker/scenarios/__init__.py", "")
    write_file("services/simulation_worker/exports/__init__.py", "")
    write_file("services/simulation_worker/config/__init__.py", "")

    simulation_config = """
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    season: int = 2026
    iterations: int = 100000
    score_std_dev: float = 11.5
    recency_weight: float = 0.35
    injury_variance_weight: float = 0.10
    upset_noise_weight: float = 0.08
    player_minutes_recency_weight: float = 0.40
    player_form_recency_weight: float = 0.50
    home_court_advantage: float = 3.2
    neutral_court: bool = True
"""

    player_model = """
from dataclasses import dataclass
import random


@dataclass
class PlayerProjectionInput:
    player_id: int
    player_name: str
    avg_points: float
    avg_rebounds: float
    avg_assists: float
    avg_minutes: float
    recent_points: float
    recent_rebounds: float
    recent_assists: float
    injury_risk: float = 0.0


def weighted_stat(season_avg: float, recent_avg: float, recency_weight: float) -> float:
    return ((1 - recency_weight) * season_avg) + (recency_weight * recent_avg)


def sample_player_stat(mean_value: float, volatility: float = 0.18) -> float:
    floor = max(0.0, mean_value * (1 - volatility))
    ceiling = mean_value * (1 + volatility)
    return random.uniform(floor, ceiling)


def simulate_player_projection(player: PlayerProjectionInput, recency_weight: float) -> dict:
    available = random.random() > player.injury_risk

    if not available:
        return {
            "player_id": player.player_id,
            "player_name": player.player_name,
            "available": False,
            "minutes": 0.0,
            "points": 0.0,
            "rebounds": 0.0,
            "assists": 0.0,
        }

    exp_points = weighted_stat(player.avg_points, player.recent_points, recency_weight)
    exp_rebounds = weighted_stat(player.avg_rebounds, player.recent_rebounds, recency_weight)
    exp_assists = weighted_stat(player.avg_assists, player.recent_assists, recency_weight)
    exp_minutes = weighted_stat(player.avg_minutes, player.avg_minutes, 0.0)

    return {
        "player_id": player.player_id,
        "player_name": player.player_name,
        "available": True,
        "minutes": round(sample_player_stat(exp_minutes, 0.10), 1),
        "points": round(sample_player_stat(exp_points, 0.22), 1),
        "rebounds": round(sample_player_stat(exp_rebounds, 0.20), 1),
        "assists": round(sample_player_stat(exp_assists, 0.20), 1),
    }
"""

    injury_model = """
import random


def simulate_team_injury_adjustment(base_team_rating: float, aggregated_injury_risk: float) -> float:
    injury_hit = random.random() < aggregated_injury_risk
    if not injury_hit:
        return base_team_rating

    penalty = random.uniform(1.5, 6.0)
    return max(0.0, base_team_rating - penalty)
"""

    game_engine = """
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
"""

    scenario_engine = """
def build_scenarios(base_record: dict) -> list[dict]:
    return [
        {
            "scenario_key": "baseline",
            "label": "Baseline",
            "injury_multiplier": 1.0,
            "variance_multiplier": 1.0,
        },
        {
            "scenario_key": "high_variance",
            "label": "High Variance",
            "injury_multiplier": 1.0,
            "variance_multiplier": 1.25,
        },
        {
            "scenario_key": "injury_stress",
            "label": "Injury Stress",
            "injury_multiplier": 1.5,
            "variance_multiplier": 1.0,
        },
        {
            "scenario_key": "chaos_mode",
            "label": "Chaos Mode",
            "injury_multiplier": 1.35,
            "variance_multiplier": 1.35,
        },
    ]
"""

    bracket_engine = """
from collections import Counter
from services.simulation_worker.engines.game_engine import simulate_game


def simulate_matchup_many(team_a, team_b, iterations=100000, neutral_court=True, score_std_dev=11.5):
    wins = Counter()
    margins = []
    scores = []

    for _ in range(iterations):
        result = simulate_game(team_a, team_b, neutral_court=neutral_court, score_std_dev=score_std_dev)
        wins[result["winner_team_name"]] += 1
        margins.append(result["margin"])
        scores.append((result["team_a_score"], result["team_b_score"]))

    total = max(1, iterations)

    team_a_avg = round(sum(s[0] for s in scores) / total, 2)
    team_b_avg = round(sum(s[1] for s in scores) / total, 2)

    return {
        "iterations": iterations,
        "team_a_win_pct": round((wins[team_a.team_name] / total) * 100, 2),
        "team_b_win_pct": round((wins[team_b.team_name] / total) * 100, 2),
        "avg_team_a_score": team_a_avg,
        "avg_team_b_score": team_b_avg,
        "avg_margin": round(sum(margins) / total, 2),
        "projected_winner": team_a.team_name if wins[team_a.team_name] >= wins[team_b.team_name] else team_b.team_name,
    }
"""

    export_engine = """
import json
from pathlib import Path


def export_matchup_result(payload: dict, slug: str) -> None:
    output_dir = Path("data/simulation-outputs/matchups")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / f"{slug}.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_bracket_top_10(payload: dict) -> None:
    output_dir = Path("data/simulation-outputs/brackets")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / "top_10_brackets.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
"""

    runner = """
from services.simulation_worker.config.simulation_config import SimulationConfig
from services.simulation_worker.engines.game_engine import TeamGameInput
from services.simulation_worker.engines.bracket_engine import simulate_matchup_many
from services.simulation_worker.exports.export_results import export_matchup_result


def run_demo_simulation():
    config = SimulationConfig(iterations=100000)

    team_a = TeamGameInput(
        team_id=1,
        team_name="Play-In Team A",
        offense_rating=111.5,
        defense_rating=91.2,
        pace=69.5,
        recent_form=4.3,
        injury_adjusted_rating=108.0,
    )

    team_b = TeamGameInput(
        team_id=2,
        team_name="Play-In Team B",
        offense_rating=108.1,
        defense_rating=93.8,
        pace=67.8,
        recent_form=2.1,
        injury_adjusted_rating=104.7,
    )

    result = simulate_matchup_many(
        team_a,
        team_b,
        iterations=config.iterations,
        neutral_court=config.neutral_court,
        score_std_dev=config.score_std_dev,
    )

    payload = {
        "matchup": {
            "team_a": team_a.team_name,
            "team_b": team_b.team_name,
        },
        "simulation": result,
        "reasoning": {
            "summary": "Projected winner is based on offense, defense, pace, recent form, variance, and repeated Monte Carlo simulation."
        }
    }

    export_matchup_result(payload, "play-in-team-a-vs-play-in-team-b")
    print("Demo simulation exported.")


if __name__ == "__main__":
    run_demo_simulation()
"""

    write_file("services/simulation_worker/config/simulation_config.py", simulation_config)
    write_file("services/simulation_worker/models/player_model.py", player_model)
    write_file("services/simulation_worker/scenarios/injury_model.py", injury_model)
    write_file("services/simulation_worker/engines/game_engine.py", game_engine)
    write_file("services/simulation_worker/scenarios/scenario_engine.py", scenario_engine)
    write_file("services/simulation_worker/engines/bracket_engine.py", bracket_engine)
    write_file("services/simulation_worker/exports/export_results.py", export_engine)
    write_file("services/simulation_worker/run_simulations.py", runner)