from utils.file_utils import write_file, ensure_dir


def build_monte_carlo():

    print("Building massive Monte Carlo engine...")

    ensure_dir("services/simulation_worker/monte_carlo")

    write_file("services/simulation_worker/monte_carlo/__init__.py", "")

    vector_engine = """
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
"""

    parallel_engine = """
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
"""

    tournament_engine = """
from __future__ import annotations

from collections import Counter


def rank_top_brackets(bracket_results: list[dict], top_n: int = 10) -> list[dict]:
    counter = Counter()

    for bracket in bracket_results:
        key = tuple(bracket.get("picks", []))
        counter[key] += 1

    ranked = []
    total = max(1, sum(counter.values()))

    for picks, count in counter.most_common(top_n):
        ranked.append(
            {
                "picks": list(picks),
                "frequency": count,
                "probability_pct": round((count / total) * 100, 4),
            }
        )

    return ranked
"""

    runner = """
from services.simulation_worker.monte_carlo.parallel_engine import simulate_matchup_parallel
from services.simulation_worker.narratives.narrative_writer import build_matchup_narrative
from services.simulation_worker.narratives.export_narrative import export_matchup_story
from services.simulation_worker.exports.export_results import export_matchup_result


def run_massive_monte_carlo():
    team_a_features = {
        "team_name": "Play-In Team A",
        "offense_rating": 112.6,
        "defense_rating": 93.1,
        "net_rating": 19.5,
    }

    team_b_features = {
        "team_name": "Play-In Team B",
        "offense_rating": 108.3,
        "defense_rating": 95.7,
        "net_rating": 12.6,
    }

    simulation_result = simulate_matchup_parallel(
        team_a_name=team_a_features["team_name"],
        team_b_name=team_b_features["team_name"],
        team_a_mean=74.8,
        team_b_mean=69.9,
        iterations=500000,
        score_std_dev=11.5,
        workers=4,
    )

    narrative = build_matchup_narrative(
        team_a_features=team_a_features,
        team_b_features=team_b_features,
        simulation_result=simulation_result,
    )

    slug = "play-in-team-a-vs-play-in-team-b"

    export_matchup_result(
        {
            "matchup": {
                "team_a": team_a_features["team_name"],
                "team_b": team_b_features["team_name"],
            },
            "simulation": simulation_result,
        },
        slug,
    )

    export_matchup_story(slug, narrative)

    print("Massive Monte Carlo simulation complete and exported.")


if __name__ == "__main__":
    run_massive_monte_carlo()
"""

    write_file("services/simulation_worker/monte_carlo/vector_engine.py", vector_engine)
    write_file("services/simulation_worker/monte_carlo/parallel_engine.py", parallel_engine)
    write_file("services/simulation_worker/monte_carlo/tournament_engine.py", tournament_engine)
    write_file("services/simulation_worker/run_massive_monte_carlo.py", runner)