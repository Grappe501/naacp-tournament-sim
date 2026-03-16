from services.ingestion_worker.sources.espn.rosters import fetch_espn_roster
from services.ingestion_worker.normalizers.rosters import normalize_roster
from services.ingestion_worker.loaders.player_loader import upsert_players


def run_roster_pipeline(team_external_id: str) -> list[dict]:
    raw = fetch_espn_roster(team_external_id)
    records = normalize_roster(raw, team_external_id=team_external_id)
    upsert_players(records)
    print(f"Roster pipeline complete for team {team_external_id}: {len(records)} players")
    return records
