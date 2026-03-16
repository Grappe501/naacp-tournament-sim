from __future__ import annotations


def normalize_teams(payload: dict) -> list[dict]:
    teams = []

    sports = payload.get("sports", [])
    if not sports:
        return teams

    leagues = sports[0].get("leagues", [])
    if not leagues:
        return teams

    for row in leagues[0].get("teams", []):
        team = row.get("team", {})
        teams.append(
            {
                "external_source": "espn",
                "external_id": str(team.get("id")),
                "name": team.get("displayName", ""),
                "short_name": team.get("shortDisplayName"),
                "abbreviation": team.get("abbreviation"),
                "slug": f"espn-{team.get('id')}",
            }
        )

    return teams
