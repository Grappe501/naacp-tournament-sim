from services.simulation_worker.data.data_loader import fetch_teams, fetch_recent_games
from services.simulation_worker.data.team_feature_builder import build_team_features
from services.simulation_worker.engines.game_engine import TeamGameInput


def build_matchup(team_a_id, team_b_id):

    teams = fetch_teams()

    team_a = next(t for t in teams if t["team_id"] == team_a_id)
    team_b = next(t for t in teams if t["team_id"] == team_b_id)

    recent_a = fetch_recent_games(team_a_id)
    recent_b = fetch_recent_games(team_b_id)

    features_a = build_team_features(team_a, recent_a)
    features_b = build_team_features(team_b, recent_b)

    team_a_input = TeamGameInput(**features_a)
    team_b_input = TeamGameInput(**features_b)

    return team_a_input, team_b_input
