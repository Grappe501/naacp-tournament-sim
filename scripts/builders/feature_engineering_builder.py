from utils.file_utils import write_file, ensure_dir


def build_feature_engineering():

    print("Building feature engineering engine...")

    ensure_dir("services/simulation_worker/features")

    write_file("services/simulation_worker/features/__init__.py", "")

    team_features = """
from packages.db.connection import get_connection


def calculate_team_features():

    sql = '''

    SELECT
        t.id,
        t.name,
        COUNT(g.id) as games_played
    FROM teams t
    LEFT JOIN games g
        ON g.home_team_id = t.id
        OR g.away_team_id = t.id
    GROUP BY t.id, t.name

    '''

    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()

    features = []

    for r in rows:

        games_played = r[2] if r[2] else 1

        offense = 100 + (games_played * 0.1)
        defense = 100 - (games_played * 0.1)

        features.append({
            "team_id": r[0],
            "team_name": r[1],
            "offense_rating": offense,
            "defense_rating": defense,
            "net_rating": offense - defense
        })

    return features
"""

    player_features = """
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
"""

    game_features = """
def calculate_game_features(team_a, team_b):

    pace = (team_a["offense_rating"] + team_b["offense_rating"]) / 3

    variance = abs(team_a["net_rating"] - team_b["net_rating"]) * 0.5

    return {
        "expected_pace": pace,
        "variance_profile": variance
    }
"""

    feature_pipeline = """
from services.simulation_worker.features.team_features import calculate_team_features


def build_feature_table():

    features = calculate_team_features()

    print("Feature table built:", len(features))

    return features
"""

    write_file("services/simulation_worker/features/team_features.py", team_features)
    write_file("services/simulation_worker/features/player_features.py", player_features)
    write_file("services/simulation_worker/features/game_features.py", game_features)
    write_file("services/simulation_worker/features/feature_pipeline.py", feature_pipeline)