from services.ingestion-worker.sources.espn.schedule_adapter import ESPNScheduleAdapter
from services.ingestion-worker.normalizers.schedule_normalizer import normalize_espn_schedule
from services.ingestion-worker.loaders.game_loader import upsert_games

def run_schedule_pipeline(team_external_id: str, season: int):
    adapter = ESPNScheduleAdapter()
    raw = adapter.fetch(team_id=team_external_id, season=season)
    games = normalize_espn_schedule(raw, season=season)
    upsert_games(games)
    print(f"Schedule pipeline complete for team {team_external_id}: {len(games)} games")
