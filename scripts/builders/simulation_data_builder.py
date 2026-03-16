from utils.file_utils import write_file, ensure_dir


def build_simulation_data():

    print("Building simulation data layer...")

    ensure_dir("services/simulation_worker/data")

    write_file("services/simulation_worker/data/__init__.py", "")

    data_loader = """
from packages.db.connection import get_connection


def fetch_teams():

    sql = '''
    SELECT
        id,
        name
    FROM teams
    '''

    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()

    return [
        {
            "team_id": r[0],
            "team_name": r[1]
        }
        for r in rows
    ]


def fetch_team_players(team_id):

    sql = '''
    SELECT
        id,
        full_name,
        position
    FROM players
    WHERE team_id = :team_id
    '''

    with get_connection() as conn:
        rows = conn.execute(sql, {"team_id": team_id}).fetchall()

    return [
        {
            "player_id": r[0],
            "player_name": r[1],
            "position": r[2]
        }
        for r in rows
    ]


def fetch_recent_games(team_id):

    sql = '''
    SELECT
        season,
        game_date
    FROM games
    WHERE home_team_id = :team_id
       OR away_team_id = :team_id
    ORDER BY game_date DESC
    LIMIT 10
    '''

    with get_connection() as conn:
        rows = conn.execute(sql, {"team_id": team_id}).fetchall()

    return rows
"""

    team_feature_builder = """
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
"""

    matchup_builder = """
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
"""

    runner = """
from services.simulation_worker.data.matchup_builder import build_matchup
from services.simulation_worker.engines.bracket_engine import simulate_matchup_many
from services.simulation_worker.exports.export_results import export_matchup_result


def run_database_simulation(team_a_id, team_b_id):

    team_a, team_b = build_matchup(team_a_id, team_b_id)

    result = simulate_matchup_many(team_a, team_b, iterations=100000)

    payload = {
        "matchup": {
            "team_a": team_a.team_name,
            "team_b": team_b.team_name
        },
        "simulation": result
    }

    slug = f"{team_a.team_name.lower().replace(' ','-')}-vs-{team_b.team_name.lower().replace(' ','-')}"

    export_matchup_result(payload, slug)

    print("Simulation complete and exported.")


if __name__ == "__main__":
    run_database_simulation(1, 2)
"""

    write_file("services/simulation_worker/data/data_loader.py", data_loader)
    write_file("services/simulation_worker/data/team_feature_builder.py", team_feature_builder)
    write_file("services/simulation_worker/data/matchup_builder.py", matchup_builder)
    write_file("services/simulation_worker/run_database_simulation.py", runner)