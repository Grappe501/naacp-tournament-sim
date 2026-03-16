from services.simulation_worker.config.simulation_config import SimulationConfig
from services.simulation_worker.engines.game_engine import TeamGameInput
from services.simulation_worker.engines.bracket_engine import simulate_matchup_many
from services.simulation_worker.exports.export_results import export_matchup_result


def run_demo_simulation():
    config = SimulationConfig(iterations=100000)

    team_a = TeamGameInput(
        team_id=1,
        team_name="Play-In Team A",
        offense_rating=111.5,
        defense_rating=91.2,
        pace=69.5,
        recent_form=4.3,
        injury_adjusted_rating=108.0,
    )

    team_b = TeamGameInput(
        team_id=2,
        team_name="Play-In Team B",
        offense_rating=108.1,
        defense_rating=93.8,
        pace=67.8,
        recent_form=2.1,
        injury_adjusted_rating=104.7,
    )

    result = simulate_matchup_many(
        team_a,
        team_b,
        iterations=config.iterations,
        neutral_court=config.neutral_court,
        score_std_dev=config.score_std_dev,
    )

    payload = {
        "matchup": {
            "team_a": team_a.team_name,
            "team_b": team_b.team_name,
        },
        "simulation": result,
        "reasoning": {
            "summary": "Projected winner is based on offense, defense, pace, recent form, variance, and repeated Monte Carlo simulation."
        }
    }

    export_matchup_result(payload, "play-in-team-a-vs-play-in-team-b")
    print("Demo simulation exported.")


if __name__ == "__main__":
    run_demo_simulation()
