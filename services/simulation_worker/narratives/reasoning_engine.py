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
