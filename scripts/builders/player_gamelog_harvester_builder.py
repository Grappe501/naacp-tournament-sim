from utils.file_utils import write_file, ensure_dir


def build_player_gamelog_harvester():

    print("Building Player Game Log Harvester...")

    ensure_dir("services/ingestion_worker/sources/espn")
    ensure_dir("services/ingestion_worker/normalizers")
    ensure_dir("services/ingestion_worker/loaders")
    ensure_dir("services/ingestion_worker/pipelines")

    # ---------------------------------------------------
    # ESPN PLAYER GAME LOG SOURCE
    # ---------------------------------------------------

    espn_player_logs = """
from services.ingestion_worker.utils.http import get_json


def fetch_player_game_log(player_id: str, season: int):

    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/athletes/{player_id}/gamelog?season={season}"
    )

    return get_json(url)
"""

    write_file(
        "services/ingestion_worker/sources/espn/player_logs.py",
        espn_player_logs,
    )

    # ---------------------------------------------------
    # NORMALIZER
    # ---------------------------------------------------

    normalizer = """
from __future__ import annotations


def normalize_player_logs(payload: dict, player_external_id: str):

    games = []

    events = payload.get("events", [])

    for event in events:

        stats = event.get("stats", [])

        row = {
            "external_player_id": player_external_id,
            "game_id": event.get("eventId"),
            "minutes": stats[0] if len(stats) > 0 else None,
            "points": stats[1] if len(stats) > 1 else None,
            "rebounds": stats[2] if len(stats) > 2 else None,
            "assists": stats[3] if len(stats) > 3 else None,
            "steals": stats[4] if len(stats) > 4 else None,
            "blocks": stats[5] if len(stats) > 5 else None,
            "turnovers": stats[6] if len(stats) > 6 else None,
            "fouls": stats[7] if len(stats) > 7 else None,
        }

        games.append(row)

    return games
"""

    write_file(
        "services/ingestion_worker/normalizers/player_logs.py",
        normalizer,
    )

    # ---------------------------------------------------
    # DATABASE LOADER
    # ---------------------------------------------------

    loader = """
from sqlalchemy import text
from packages.db.engine import engine


def upsert_player_game_logs(records):

    sql = text(
        '''
        INSERT INTO player_game_logs (
            player_id,
            game_id,
            minutes,
            points,
            rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            fouls
        )
        SELECT
            p.id,
            :game_id,
            :minutes,
            :points,
            :rebounds,
            :assists,
            :steals,
            :blocks,
            :turnovers,
            :fouls
        FROM players p
        WHERE p.external_id = :external_player_id
        ON CONFLICT DO NOTHING
        '''
    )

    with engine.begin() as conn:

        for record in records:

            conn.execute(sql, record)
"""

    write_file(
        "services/ingestion_worker/loaders/player_gamelog_loader.py",
        loader,
    )

    # ---------------------------------------------------
    # PIPELINE
    # ---------------------------------------------------

    pipeline = """
from services.ingestion_worker.sources.espn.player_logs import fetch_player_game_log
from services.ingestion_worker.normalizers.player_logs import normalize_player_logs
from services.ingestion_worker.loaders.player_gamelog_loader import upsert_player_game_logs


def run_player_log_pipeline(player_external_id: str, season: int):

    raw = fetch_player_game_log(player_external_id, season)

    records = normalize_player_logs(
        raw,
        player_external_id=player_external_id
    )

    upsert_player_game_logs(records)

    print(f"Loaded {len(records)} player game logs for {player_external_id}")

    return records
"""

    write_file(
        "services/ingestion_worker/pipelines/player_logs_pipeline.py",
        pipeline,
    )

    # ---------------------------------------------------
    # MASS HARVEST PIPELINE
    # ---------------------------------------------------

    harvest = """
from packages.db.engine import engine
from sqlalchemy import text

from services.ingestion_worker.pipelines.player_logs_pipeline import run_player_log_pipeline


def harvest_all_player_logs(season: int = 2026):

    sql = text("SELECT external_id FROM players")

    with engine.begin() as conn:

        players = conn.execute(sql).fetchall()

    for p in players:

        player_id = p[0]

        try:
            run_player_log_pipeline(player_id, season)
        except Exception:
            print(f"Failed player {player_id}")

    print("Player game log harvest complete.")
"""

    write_file(
        "services/ingestion_worker/pipelines/player_log_harvest.py",
        harvest,
    )

    print("Player Game Log Harvester Built")