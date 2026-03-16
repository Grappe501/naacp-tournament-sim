import requests
from services.ingestion-worker.sources.base import BaseSourceAdapter

class ESPNRosterAdapter(BaseSourceAdapter):
    source_name = "espn_rosters"

    def fetch(self, team_id: str, **kwargs):
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/roster"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
