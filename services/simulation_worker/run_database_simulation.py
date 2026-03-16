from services.simulation_worker.data.matchup_builder import build_matchup
from services.simulation_worker.engines.bracket_engine import simulate_matchup_many
from services.simulation_worker.exports.export_results import export_matchup_result


def run_database_simulation(team_a_id, team_b_id):

    team_a, team_b = build_matchup(team_a_id, team_b_id)

    result = simulate_matchup_many(team_a, team_b, iterations=100000)

    payload = {
        "matchup": {
            "team_a": team_a.team_name,
            "team_b": team_b.team_name
        },
        "simulation": result
    }

    slug = f"{team_a.team_name.lower().replace(' ','-')}-vs-{team_b.team_name.lower().replace(' ','-')}"

    export_matchup_result(payload, slug)

    print("Simulation complete and exported.")


if __name__ == "__main__":
    run_database_simulation(1, 2)
