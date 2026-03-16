from utils.file_utils import write_file

def build_roster_ingestion():
    print("Building roster ingestion...")

    adapter = """
import requests
from services.ingestion-worker.sources.base import BaseSourceAdapter

class ESPNRosterAdapter(BaseSourceAdapter):
    source_name = "espn_rosters"

    def fetch(self, team_id: str, **kwargs):
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/roster"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
"""

    normalizer = """
from typing import List
from services.ingestion-worker.models.records import PlayerRecord

def normalize_espn_roster(payload: dict, team_external_id: str) -> List[PlayerRecord]:
    athletes = payload.get("athletes", [])
    players = []

    for athlete_group in athletes:
        for athlete in athlete_group.get("items", []):
            players.append(
                PlayerRecord(
                    external_id=str(athlete.get("id")),
                    team_external_id=team_external_id,
                    full_name=athlete.get("displayName", ""),
                    position=(athlete.get("position") or {}).get("abbreviation"),
                )
            )

    return players
"""

    pipeline = """
from services.ingestion-worker.sources.espn.roster_adapter import ESPNRosterAdapter
from services.ingestion-worker.normalizers.roster_normalizer import normalize_espn_roster
from services.ingestion-worker.loaders.player_loader import upsert_players

def run_roster_pipeline(team_external_id: str):
    adapter = ESPNRosterAdapter()
    raw = adapter.fetch(team_id=team_external_id)
    players = normalize_espn_roster(raw, team_external_id=team_external_id)
    upsert_players(players)
    print(f"Roster pipeline complete for team {team_external_id}: {len(players)} players")
"""

    write_file("services/ingestion-worker/sources/espn/roster_adapter.py", adapter)
    write_file("services/ingestion-worker/normalizers/roster_normalizer.py", normalizer)
    write_file("services/ingestion-worker/pipelines/rosters_pipeline.py", pipeline)