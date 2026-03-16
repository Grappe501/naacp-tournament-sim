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
