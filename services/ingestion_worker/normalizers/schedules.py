from __future__ import annotations


def normalize_schedule(payload: dict, season: int) -> list[dict]:
    games = []

    for event in payload.get("events", []):
        competitions = event.get("competitions", [])
        if not competitions:
            continue

        competition = competitions[0]
        competitors = competition.get("competitors", [])
        if len(competitors) != 2:
            continue

        home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[-1])

        games.append(
            {
                "external_source": "espn",
                "external_id": str(event.get("id")),
                "season": season,
                "game_date": event.get("date"),
                "home_team_external_id": str(home.get("team", {}).get("id")),
                "away_team_external_id": str(away.get("team", {}).get("id")),
                "neutral_site": bool(competition.get("neutralSite", False)),
                "location": (competition.get("venue") or {}).get("fullName"),
            }
        )

    return games
