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
