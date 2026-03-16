from services.ingestion_worker.utils.http import get_json


def fetch_espn_teams() -> dict:
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"
    return get_json(url)
