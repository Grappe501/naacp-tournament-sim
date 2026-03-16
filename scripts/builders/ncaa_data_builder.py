from utils.file_utils import write_file

def build_ncaa_data():
    print("Building team ingestion...")

    adapter = """
import requests
from services.ingestion-worker.sources.base import BaseSourceAdapter

class ESPNTeamsAdapter(BaseSourceAdapter):
    source_name = "espn_teams"

    def fetch(self, **kwargs):
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
"""

    normalizer = """
from typing import List
from services.ingestion-worker.models.records import TeamRecord

def normalize_espn_teams(payload: dict) -> List[TeamRecord]:
    teams = []
    sports = payload.get("sports", [])
    if not sports:
        return teams

    leagues = sports[0].get("leagues", [])
    if not leagues:
        return teams

    raw_teams = leagues[0].get("teams", [])
    for row in raw_teams:
        team = row.get("team", {})
        teams.append(
            TeamRecord(
                external_id=str(team.get("id")),
                name=team.get("displayName", ""),
                short_name=team.get("shortDisplayName"),
                abbreviation=team.get("abbreviation"),
            )
        )
    return teams
"""

    pipeline = """
from services.ingestion-worker.sources.espn.teams_adapter import ESPNTeamsAdapter
from services.ingestion-worker.normalizers.teams_normalizer import normalize_espn_teams
from services.ingestion-worker.loaders.team_loader import upsert_teams

def run_teams_pipeline():
    adapter = ESPNTeamsAdapter()
    raw = adapter.fetch()
    records = normalize_espn_teams(raw)
    upsert_teams(records)
    print(f"Teams pipeline complete: {len(records)} records")
"""

    write_file("services/ingestion-worker/sources/espn/teams_adapter.py", adapter)
    write_file("services/ingestion-worker/normalizers/teams_normalizer.py", normalizer)
    write_file("services/ingestion-worker/pipelines/teams_pipeline.py", pipeline)