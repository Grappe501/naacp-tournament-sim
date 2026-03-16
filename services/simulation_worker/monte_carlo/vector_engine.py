from __future__ import annotations

import numpy as np


def simulate_matchup_vectorized(
    team_a_name: str,
    team_b_name: str,
    team_a_mean: float,
    team_b_mean: float,
    iterations: int = 100000,
    score_std_dev: float = 11.5,
) -> dict:
    if iterations <= 0:
        raise ValueError("iterations must be greater than 0")

    a_scores = np.random.normal(loc=team_a_mean, scale=score_std_dev, size=iterations)
    b_scores = np.random.normal(loc=team_b_mean, scale=score_std_dev, size=iterations)

    a_scores = np.maximum(np.rint(a_scores), 40).astype(int)
    b_scores = np.maximum(np.rint(b_scores), 40).astype(int)

    ties = a_scores == b_scores
    if np.any(ties):
        tiebreaks = np.random.randint(0, 2, size=ties.sum())
        a_scores[ties] += (tiebreaks == 1).astype(int)
        b_scores[ties] += (tiebreaks == 0).astype(int)

    team_a_wins = int(np.sum(a_scores > b_scores))
    team_b_wins = int(np.sum(b_scores > a_scores))

    margins = np.abs(a_scores - b_scores)

    projected_winner = team_a_name if team_a_wins >= team_b_wins else team_b_name

    return {
        "iterations": int(iterations),
        "team_a_name": team_a_name,
        "team_b_name": team_b_name,
        "team_a_win_pct": round((team_a_wins / iterations) * 100, 2),
        "team_b_win_pct": round((team_b_wins / iterations) * 100, 2),
        "avg_team_a_score": round(float(np.mean(a_scores)), 2),
        "avg_team_b_score": round(float(np.mean(b_scores)), 2),
        "avg_margin": round(float(np.mean(margins)), 2),
        "median_margin": round(float(np.median(margins)), 2),
        "team_a_90th_score": round(float(np.percentile(a_scores, 90)), 2),
        "team_b_90th_score": round(float(np.percentile(b_scores, 90)), 2),
        "projected_winner": projected_winner,
    }
