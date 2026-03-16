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
