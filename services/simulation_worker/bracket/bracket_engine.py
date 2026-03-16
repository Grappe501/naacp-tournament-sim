from collections import defaultdict
from services.simulation_worker.engines.bracket_engine import simulate_matchup_many
from services.simulation_worker.data.matchup_builder import build_matchup


def simulate_bracket(bracket_games, iterations=100000):

    results = defaultdict(int)

    for _ in range(iterations):

        winners = {}

        for game in bracket_games:

            team_a, team_b = build_matchup(game.team_a_id, game.team_b_id)

            result = simulate_matchup_many(team_a, team_b, iterations=1)

            winner = result["projected_winner"]

            winners[game.game_id] = winner

        champion = winners[max(winners.keys())]

        results[champion] += 1

    total = max(1, iterations)

    probabilities = {
        team: round((count / total) * 100, 2)
        for team, count in results.items()
    }

    return probabilities
