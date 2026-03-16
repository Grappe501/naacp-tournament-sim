from services.ingestion_worker.sources.espn.schedules import fetch_espn_schedule
from services.ingestion_worker.normalizers.schedules import normalize_schedule
from services.ingestion_worker.loaders.game_loader import upsert_games


def run_schedule_pipeline(team_external_id: str, season: int) -> list[dict]:
    raw = fetch_espn_schedule(team_external_id, season)
    records = normalize_schedule(raw, season=season)
    upsert_games(records)
    print(f"Schedule pipeline complete for team {team_external_id}: {len(records)} games")
    return records
