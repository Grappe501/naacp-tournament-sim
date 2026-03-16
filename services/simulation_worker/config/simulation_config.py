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
