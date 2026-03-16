from __future__ import annotations


def normalize_roster(payload: dict, team_external_id: str) -> list[dict]:
    players = []

    for athlete_group in payload.get("athletes", []):
        for athlete in athlete_group.get("items", []):
            players.append(
                {
                    "external_source": "espn",
                    "external_id": str(athlete.get("id")),
                    "team_external_id": team_external_id,
                    "full_name": athlete.get("displayName", ""),
                    "position": (athlete.get("position") or {}).get("abbreviation"),
                    "class_year": (athlete.get("experience") or {}).get("name"),
                }
            )

    return players
