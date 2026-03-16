from services.ingestion_worker.utils.http import get_json


def fetch_espn_summary(event_id: str) -> dict:
    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/summary?event={event_id}"
    )
    return get_json(url)
