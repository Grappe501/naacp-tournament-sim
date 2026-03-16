from services.simulation_worker.monte_carlo.parallel_engine import simulate_matchup_parallel
from services.simulation_worker.narratives.narrative_writer import build_matchup_narrative
from services.simulation_worker.narratives.export_narrative import export_matchup_story
from services.simulation_worker.exports.export_results import export_matchup_result


def run_massive_monte_carlo():
    team_a_features = {
        "team_name": "Play-In Team A",
        "offense_rating": 112.6,
        "defense_rating": 93.1,
        "net_rating": 19.5,
    }

    team_b_features = {
        "team_name": "Play-In Team B",
        "offense_rating": 108.3,
        "defense_rating": 95.7,
        "net_rating": 12.6,
    }

    simulation_result = simulate_matchup_parallel(
        team_a_name=team_a_features["team_name"],
        team_b_name=team_b_features["team_name"],
        team_a_mean=74.8,
        team_b_mean=69.9,
        iterations=500000,
        score_std_dev=11.5,
        workers=4,
    )

    narrative = build_matchup_narrative(
        team_a_features=team_a_features,
        team_b_features=team_b_features,
        simulation_result=simulation_result,
    )

    slug = "play-in-team-a-vs-play-in-team-b"

    export_matchup_result(
        {
            "matchup": {
                "team_a": team_a_features["team_name"],
                "team_b": team_b_features["team_name"],
            },
            "simulation": simulation_result,
        },
        slug,
    )

    export_matchup_story(slug, narrative)

    print("Massive Monte Carlo simulation complete and exported.")


if __name__ == "__main__":
    run_massive_monte_carlo()
