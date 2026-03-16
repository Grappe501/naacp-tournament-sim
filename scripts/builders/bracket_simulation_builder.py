from utils.file_utils import write_file, ensure_dir


def build_bracket_simulation():

    print("Building bracket simulation engine...")

    ensure_dir("services/simulation_worker/bracket")

    write_file("services/simulation_worker/bracket/__init__.py", "")

    bracket_model = """
from dataclasses import dataclass


@dataclass
class BracketGame:
    game_id: int
    round_name: str
    team_a_id: int
    team_b_id: int
"""


    bracket_engine = """
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
"""

    bracket_runner = """
from services.simulation_worker.bracket.bracket_engine import simulate_bracket
from services.simulation_worker.bracket.bracket_model import BracketGame


def run_bracket_simulation():

    bracket_games = [

        BracketGame(1, "play-in", 1, 2),
        BracketGame(2, "play-in", 3, 4),
        BracketGame(3, "round64", 5, 6),

    ]

    probabilities = simulate_bracket(bracket_games, iterations=100000)

    print("Bracket simulation results:")

    for team, prob in probabilities.items():
        print(team, prob)


if __name__ == "__main__":
    run_bracket_simulation()
"""

    write_file("services/simulation_worker/bracket/bracket_model.py", bracket_model)
    write_file("services/simulation_worker/bracket/bracket_engine.py", bracket_engine)
    write_file("services/simulation_worker/run_bracket_simulation.py", bracket_runner)