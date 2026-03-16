from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from math import ceil

from services.simulation_worker.monte_carlo.vector_engine import simulate_matchup_vectorized


def _run_chunk(team_a_name, team_b_name, team_a_mean, team_b_mean, iterations, score_std_dev):
    return simulate_matchup_vectorized(
        team_a_name=team_a_name,
        team_b_name=team_b_name,
        team_a_mean=team_a_mean,
        team_b_mean=team_b_mean,
        iterations=iterations,
        score_std_dev=score_std_dev,
    )


def simulate_matchup_parallel(
    team_a_name: str,
    team_b_name: str,
    team_a_mean: float,
    team_b_mean: float,
    iterations: int = 500000,
    score_std_dev: float = 11.5,
    workers: int = 4,
) -> dict:
    if workers <= 1:
        return simulate_matchup_vectorized(
            team_a_name=team_a_name,
            team_b_name=team_b_name,
            team_a_mean=team_a_mean,
            team_b_mean=team_b_mean,
            iterations=iterations,
            score_std_dev=score_std_dev,
        )

    chunk_size = ceil(iterations / workers)
    futures = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for _ in range(workers):
            futures.append(
                executor.submit(
                    _run_chunk,
                    team_a_name,
                    team_b_name,
                    team_a_mean,
                    team_b_mean,
                    chunk_size,
                    score_std_dev,
                )
            )

    results = [f.result() for f in futures]

    total_iterations = sum(r["iterations"] for r in results)
    if total_iterations == 0:
        raise ValueError("No iterations were completed")

    team_a_weighted_win = sum(r["team_a_win_pct"] * r["iterations"] for r in results) / total_iterations
    team_b_weighted_win = sum(r["team_b_win_pct"] * r["iterations"] for r in results) / total_iterations
    avg_team_a_score = sum(r["avg_team_a_score"] * r["iterations"] for r in results) / total_iterations
    avg_team_b_score = sum(r["avg_team_b_score"] * r["iterations"] for r in results) / total_iterations
    avg_margin = sum(r["avg_margin"] * r["iterations"] for r in results) / total_iterations

    projected_winner = team_a_name if team_a_weighted_win >= team_b_weighted_win else team_b_name

    return {
        "iterations": int(total_iterations),
        "team_a_name": team_a_name,
        "team_b_name": team_b_name,
        "team_a_win_pct": round(team_a_weighted_win, 2),
        "team_b_win_pct": round(team_b_weighted_win, 2),
        "avg_team_a_score": round(avg_team_a_score, 2),
        "avg_team_b_score": round(avg_team_b_score, 2),
        "avg_margin": round(avg_margin, 2),
        "projected_winner": projected_winner,
        "workers_used": workers,
    }
