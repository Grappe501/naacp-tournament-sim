from utils.file_utils import write_file, ensure_dir


def build_simulation_narrative():

    print("Building simulation narrative engine...")

    ensure_dir("services/simulation_worker/narratives")

    write_file("services/simulation_worker/narratives/__init__.py", "")

    reasoning_engine = """
def summarize_win_probability(team_a, team_b, win_pct):

    if win_pct > 70:
        confidence = "a dominant advantage"
    elif win_pct > 60:
        confidence = "a strong advantage"
    elif win_pct > 55:
        confidence = "a moderate edge"
    else:
        confidence = "a narrow edge"

    return f"{team_a} holds {confidence} over {team_b}, winning {win_pct:.1f}% of simulations."
"""

    matchup_reasoning = """
def explain_matchup(team_a_features, team_b_features, simulation_result):

    offense_gap = team_a_features["offense_rating"] - team_b_features["offense_rating"]
    defense_gap = team_a_features["defense_rating"] - team_b_features["defense_rating"]

    explanation = []

    explanation.append(
        f"{team_a_features['team_name']} offense rating: {team_a_features['offense_rating']:.1f}"
    )

    explanation.append(
        f"{team_b_features['team_name']} offense rating: {team_b_features['offense_rating']:.1f}"
    )

    explanation.append(
        f"Simulation projected score: {simulation_result['avg_team_a_score']} - {simulation_result['avg_team_b_score']}"
    )

    if offense_gap > 3:
        explanation.append("Offensive efficiency strongly favors Team A.")
    elif offense_gap < -3:
        explanation.append("Offensive efficiency strongly favors Team B.")

    if defense_gap < -3:
        explanation.append("Team B's defense creates additional pressure.")

    explanation.append(
        f"{simulation_result['projected_winner']} wins the majority of simulations."
    )

    return explanation
"""

    narrative_writer = """
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
"""

    export_narrative = """
import json
from pathlib import Path


def export_matchup_story(slug, narrative_payload):

    path = Path("data/simulation-outputs/narratives")

    path.mkdir(parents=True, exist_ok=True)

    file_path = path / f"{slug}.json"

    file_path.write_text(
        json.dumps(narrative_payload, indent=2),
        encoding="utf-8"
    )
"""

    write_file(
        "services/simulation_worker/narratives/reasoning_engine.py",
        reasoning_engine
    )

    write_file(
        "services/simulation_worker/narratives/matchup_reasoning.py",
        matchup_reasoning
    )

    write_file(
        "services/simulation_worker/narratives/narrative_writer.py",
        narrative_writer
    )

    write_file(
        "services/simulation_worker/narratives/export_narrative.py",
        export_narrative
    )