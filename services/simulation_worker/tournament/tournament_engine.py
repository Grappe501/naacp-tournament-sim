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
