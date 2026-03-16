import random


def build_team_features(team_record, recent_games):

    base_offense = random.uniform(102, 118)
    base_defense = random.uniform(88, 105)

    form_boost = len(recent_games) * random.uniform(0.05, 0.3)

    pace = random.uniform(65, 72)

    return {
        "team_id": team_record["team_id"],
        "team_name": team_record["team_name"],
        "offense_rating": base_offense + form_boost,
        "defense_rating": base_defense - form_boost,
        "pace": pace,
        "recent_form": form_boost,
        "injury_adjusted_rating": base_offense - random.uniform(0, 4)
    }
