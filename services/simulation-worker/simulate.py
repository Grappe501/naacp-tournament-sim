import random


def simulate_game(team_a_rating: float, team_b_rating: float) -> str:
    total = team_a_rating + team_b_rating
    roll = random.random() * total
    return "team_a" if roll < team_a_rating else "team_b"


def run_simulation() -> None:
    winner = simulate_game(80.0, 75.0)
    print(f"Simulation complete. Winner: {winner}")


if __name__ == "__main__":
    run_simulation()
