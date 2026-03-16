import random


def calculate_player_features(players):

    projections = []

    for p in players:

        projections.append({
            "player_id": p["player_id"],
            "player_name": p["player_name"],
            "impact_score": random.uniform(0, 10)
        })

    return projections
