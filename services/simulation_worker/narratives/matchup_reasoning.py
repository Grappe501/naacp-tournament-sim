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
