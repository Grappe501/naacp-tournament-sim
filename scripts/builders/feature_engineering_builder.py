from utils.file_utils import write_file, ensure_dir


def build_feature_engineering():

    print("Building feature engineering engine...")

    ensure_dir("services/simulation_worker/features")

    write_file("services/simulation_worker/features/__init__.py", "")

    # --------------------------------------------------
    # TEAM FEATURES
    # --------------------------------------------------

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

    # --------------------------------------------------
    # PLAYER FEATURES
    # --------------------------------------------------

    player_features = """
from packages.db.connection import get_connection


def calculate_player_features():

    sql = '''

    SELECT
        p.id,
        p.full_name,
        AVG(l.points) as avg_points,
        AVG(l.rebounds) as avg_rebounds,
        AVG(l.assists) as avg_assists
    FROM players p
    LEFT JOIN player_game_logs l
        ON l.player_id = p.id
    GROUP BY p.id, p.full_name

    '''

    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()

    features = []

    for r in rows:

        features.append({
            "player_id": r[0],
            "player_name": r[1],
            "avg_points": float(r[2]) if r[2] else 0,
            "avg_rebounds": float(r[3]) if r[3] else 0,
            "avg_assists": float(r[4]) if r[4] else 0
        })

    return features
"""

    # --------------------------------------------------
    # MATCHUP FEATURES
    # --------------------------------------------------

    matchup_features = """
def calculate_matchup_features(team_a, team_b):

    pace = (team_a["offense_rating"] + team_b["offense_rating"]) / 3

    strength_gap = team_a["net_rating"] - team_b["net_rating"]

    variance = abs(strength_gap) * 0.5

    return {
        "expected_pace": pace,
        "strength_gap": strength_gap,
        "variance_profile": variance
    }
"""

    # --------------------------------------------------
    # INJURY MODEL
    # --------------------------------------------------

    injury_model = """
import random


def simulate_injury_risk(player_features):

    risk = random.uniform(0, 1)

    if risk < 0.01:
        return "season_ending"

    if risk < 0.05:
        return "multi_game"

    if risk < 0.10:
        return "limited_minutes"

    return "healthy"
"""

    # --------------------------------------------------
    # FEATURE PIPELINE
    # --------------------------------------------------

    feature_pipeline = """
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
"""

    write_file("services/simulation_worker/features/team_features.py", team_features)
    write_file("services/simulation_worker/features/player_features.py", player_features)
    write_file("services/simulation_worker/features/matchup_features.py", matchup_features)
    write_file("services/simulation_worker/features/injury_model.py", injury_model)
    write_file("services/simulation_worker/features/feature_pipeline.py", feature_pipeline)