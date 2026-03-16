from utils.file_utils import write_file, ensure_dir


def build_tournament_path():

    print("Building tournament path engine...")

    ensure_dir("services/simulation_worker/tournament")

    write_file("services/simulation_worker/tournament/__init__.py", "")

    bracket_structure = """
PLAY_IN_GAMES = [
    ("PlayIn_A", "PlayIn_B"),
    ("PlayIn_C", "PlayIn_D"),
]

ROUND_OF_64 = [
    ("Team1", "Team16"),
    ("Team8", "Team9"),
    ("Team5", "Team12"),
    ("Team4", "Team13"),
]
"""

    game_simulator = """
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
"""

    round_engine = """
from services.simulation_worker.tournament.game_simulator import simulate_game


def simulate_round(matchups):

    winners = []
    game_results = []

    for team_a, team_b in matchups:

        winner, result = simulate_game(team_a, team_b)

        winners.append(winner)
        game_results.append(result)

    return winners, game_results
"""

    tournament_engine = """
from services.simulation_worker.tournament.bracket_structure import PLAY_IN_GAMES
from services.simulation_worker.tournament.round_engine import simulate_round


def simulate_tournament():

    print("Simulating play-in round")

    playin_winners, playin_results = simulate_round(PLAY_IN_GAMES)

    print("Play-in winners:", playin_winners)

    return {
        "playin_winners": playin_winners,
        "playin_results": playin_results,
    }
"""

    probability_engine = """
from collections import Counter


def compute_advancement_probabilities(results):

    counter = Counter()

    for r in results:
        counter[r["projected_winner"]] += 1

    total = sum(counter.values())

    probabilities = {}

    for team, wins in counter.items():
        probabilities[team] = wins / total

    return probabilities
"""

    runner = """
from services.simulation_worker.tournament.tournament_engine import simulate_tournament


def run_full_tournament():

    results = simulate_tournament()

    print("Tournament simulation results")
    print(results)


if __name__ == "__main__":
    run_full_tournament()
"""

    write_file(
        "services/simulation_worker/tournament/bracket_structure.py",
        bracket_structure
    )

    write_file(
        "services/simulation_worker/tournament/game_simulator.py",
        game_simulator
    )

    write_file(
        "services/simulation_worker/tournament/round_engine.py",
        round_engine
    )

    write_file(
        "services/simulation_worker/tournament/tournament_engine.py",
        tournament_engine
    )

    write_file(
        "services/simulation_worker/tournament/probability_engine.py",
        probability_engine
    )

    write_file(
        "services/simulation_worker/run_full_tournament_simulation.py",
        runner
    )