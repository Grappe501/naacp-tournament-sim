from services.ingestion_worker.utils.http import get_json


def fetch_player_game_log(player_id: str, season: int):

    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/athletes/{player_id}/gamelog?season={season}"
    )

    return get_json(url)
