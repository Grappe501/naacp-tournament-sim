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
