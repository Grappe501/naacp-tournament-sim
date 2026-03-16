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
