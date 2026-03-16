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
