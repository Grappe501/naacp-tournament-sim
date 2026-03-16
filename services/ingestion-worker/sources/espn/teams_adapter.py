import requests
from services.ingestion-worker.sources.base import BaseSourceAdapter

class ESPNTeamsAdapter(BaseSourceAdapter):
    source_name = "espn_teams"

    def fetch(self, **kwargs):
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
