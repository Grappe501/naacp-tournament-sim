from services.simulation_worker.features.team_features import calculate_team_features
from services.simulation_worker.features.player_features import calculate_player_features


def build_feature_tables():

    team_features = calculate_team_features()

    player_features = calculate_player_features()

    print("Team features:", len(team_features))
    print("Player features:", len(player_features))

    return {
        "teams": team_features,
        "players": player_features
    }
