from utils.file_utils import write_file

def build_schedule_ingestion():
    print("Building schedule ingestion...")

    adapter = """
import requests
from services.ingestion-worker.sources.base import BaseSourceAdapter

class ESPNScheduleAdapter(BaseSourceAdapter):
    source_name = "espn_schedules"

    def fetch(self, team_id: str, season: int, **kwargs):
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule?season={season}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
"""

    normalizer = """
from typing import List
from services.ingestion-worker.models.records import GameRecord

def normalize_espn_schedule(payload: dict, season: int) -> List[GameRecord]:
    events = payload.get("events", [])
    games = []

    for event in events:
        competitions = event.get("competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = comp.get("competitors", [])
        if len(competitors) != 2:
            continue

        home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])

        games.append(
            GameRecord(
                external_id=str(event.get("id")),
                season=season,
                game_date=event.get("date", ""),
                home_team_external_id=str(home.get("team", {}).get("id")),
                away_team_external_id=str(away.get("team", {}).get("id")),
                neutral_site=bool(comp.get("neutralSite", False)),
            )
        )

    return games
"""

    pipeline = """
from services.ingestion-worker.sources.espn.schedule_adapter import ESPNScheduleAdapter
from services.ingestion-worker.normalizers.schedule_normalizer import normalize_espn_schedule
from services.ingestion-worker.loaders.game_loader import upsert_games

def run_schedule_pipeline(team_external_id: str, season: int):
    adapter = ESPNScheduleAdapter()
    raw = adapter.fetch(team_id=team_external_id, season=season)
    games = normalize_espn_schedule(raw, season=season)
    upsert_games(games)
    print(f"Schedule pipeline complete for team {team_external_id}: {len(games)} games")
"""

    write_file("services/ingestion-worker/sources/espn/schedule_adapter.py", adapter)
    write_file("services/ingestion-worker/normalizers/schedule_normalizer.py", normalizer)
    write_file("services/ingestion-worker/pipelines/schedules_pipeline.py", pipeline)