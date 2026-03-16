from services.ingestion-worker.sources.espn.teams_adapter import ESPNTeamsAdapter
from services.ingestion-worker.normalizers.teams_normalizer import normalize_espn_teams
from services.ingestion-worker.loaders.team_loader import upsert_teams

def run_teams_pipeline():
    adapter = ESPNTeamsAdapter()
    raw = adapter.fetch()
    records = normalize_espn_teams(raw)
    upsert_teams(records)
    print(f"Teams pipeline complete: {len(records)} records")
