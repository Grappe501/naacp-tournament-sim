from services.simulation_worker.features.team_features import calculate_team_features


def build_feature_table():

    features = calculate_team_features()

    print("Feature table built:", len(features))

    return features
