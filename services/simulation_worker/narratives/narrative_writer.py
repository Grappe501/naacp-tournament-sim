from services.simulation_worker.narratives.reasoning_engine import summarize_win_probability
from services.simulation_worker.narratives.matchup_reasoning import explain_matchup


def build_matchup_narrative(team_a_features, team_b_features, simulation_result):

    summary = summarize_win_probability(
        team_a_features["team_name"],
        team_b_features["team_name"],
        simulation_result["team_a_win_pct"]
    )

    details = explain_matchup(team_a_features, team_b_features, simulation_result)

    return {
        "summary": summary,
        "details": details
    }
