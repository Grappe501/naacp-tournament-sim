from services.ingestion-worker.sources.espn.roster_adapter import ESPNRosterAdapter
from services.ingestion-worker.normalizers.roster_normalizer import normalize_espn_roster
from services.ingestion-worker.loaders.player_loader import upsert_players

def run_roster_pipeline(team_external_id: str):
    adapter = ESPNRosterAdapter()
    raw = adapter.fetch(team_id=team_external_id)
    players = normalize_espn_roster(raw, team_external_id=team_external_id)
    upsert_players(players)
    print(f"Roster pipeline complete for team {team_external_id}: {len(players)} players")
