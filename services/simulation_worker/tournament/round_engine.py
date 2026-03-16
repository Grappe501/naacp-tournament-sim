from services.simulation_worker.tournament.game_simulator import simulate_game


def simulate_round(matchups):

    winners = []
    game_results = []

    for team_a, team_b in matchups:

        winner, result = simulate_game(team_a, team_b)

        winners.append(winner)
        game_results.append(result)

    return winners, game_results
