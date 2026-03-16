from typing import List
from services.ingestion-worker.models.records import PlayerRecord

def normalize_espn_roster(payload: dict, team_external_id: str) -> List[PlayerRecord]:
    athletes = payload.get("athletes", [])
    players = []

    for athlete_group in athletes:
        for athlete in athlete_group.get("items", []):
            players.append(
                PlayerRecord(
                    external_id=str(athlete.get("id")),
                    team_external_id=team_external_id,
                    full_name=athlete.get("displayName", ""),
                    position=(athlete.get("position") or {}).get("abbreviation"),
                )
            )

    return players
