from services.simulation_worker.tournament.tournament_engine import simulate_tournament


def run_full_tournament():

    results = simulate_tournament()

    print("Tournament simulation results")
    print(results)


if __name__ == "__main__":
    run_full_tournament()
