from services.ingestion_worker.utils.http import get_json


def fetch_espn_schedule(team_id: str, season: int) -> dict:
    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/teams/{team_id}/schedule?season={season}"
    )
    return get_json(url)
