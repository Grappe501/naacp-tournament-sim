from services.simulation_worker.monte_carlo.vector_engine import simulate_matchup_vectorized


def simulate_game(team_a, team_b):

    result = simulate_matchup_vectorized(
        team_a_name=team_a,
        team_b_name=team_b,
        team_a_mean=72,
        team_b_mean=70,
        iterations=100000,
    )

    return result["projected_winner"], result
