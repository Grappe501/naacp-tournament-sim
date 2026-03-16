from services.ingestion_worker.sources.espn.teams import fetch_espn_teams
from services.ingestion_worker.normalizers.teams import normalize_teams
from services.ingestion_worker.loaders.team_loader import upsert_teams


def run_teams_pipeline() -> list[dict]:
    raw = fetch_espn_teams()
    records = normalize_teams(raw)
    upsert_teams(records)
    print(f"Teams pipeline complete: {len(records)} teams")
    return records
