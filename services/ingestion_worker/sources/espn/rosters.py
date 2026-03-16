from services.ingestion_worker.utils.http import get_json


def fetch_espn_roster(team_id: str) -> dict:
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/roster"
    return get_json(url)
